import os
import re
import json5
import json
# import pprint
import sys
# import argparse
# import xlwings as xw
from xlwings import Sheet as Sheet_
from .utils import *

# print = pretty_print
# pr = False


json_str_reg = re.compile(r"^\[[\s\S]*\]$|^\{[\s\S]*\}$")
wrap_list_reg = re.compile(r"^\{[\w]+:\[\]\}$")
wrap_key_reg = re.compile(r"[\w]+")
null_tags = ['null', 'Null', 'NULL', 'none', 'None', 'NONE']
header_split_char = "-"

def check_any_text_in_str(src, text_list):
    b = False
    for i in text_list:
        if i in src:
            b = True
            break
    return b

def special_dumps(obj, dump_format=None):
    if dump_format == 'json5':
        return json5.dumps(obj, ensure_ascii=False, indent=4, \
            trailing_commas=False, quote_keys=False)
    elif dump_format == 'self_defined':
        return self_defined_dumps(obj)
    else:
        return json.dumps(obj, ensure_ascii=False, indent=4)

class Headers:

    def __init__(self, ws, content_row, header_start_row, \
        header_next_col, headers_end_col, data, next_idx=0):
        ## sheet info
        self._ws = ws
        self._content_row = content_row
    

        self._row = header_start_row
        self._header_next_col = header_next_col
        self._headers_end_col = headers_end_col

        self._data = data
        self._next_idx = next_idx

        # info updated by update_header_info
        self._col = header_next_col
        self._range = None
        self._content = None
        self._width = None
        self._end_col = None
        self._idx = None
        self._name = None
        self._type = None
        self._index = None
        
        
    def __iter__(self):
        return self


    def __next__(self):
        rlt = self
        self.update_header_info()
        if self._header_next_col > self._headers_end_col:
            raise StopIteration
        # 跳过以#开头的非空header
        if type(self._name) is str and self._name.startswith('#'):
            self._header_next_col = self._end_col + 1
            rlt = self.__next__()
        self._header_next_col = self._end_col + 1
        self._next_idx += 1
        return rlt

    def check_header_v_end(self):
        b = False
        if self._row == self._ws.headers_end_row:
            b = True
        else:
            b = True
            for col in range(self._col, self._end_col+1):
                cell_below = self._ws.range((self._row + 1, col))
                if cell_below.value and \
                    not check_any_text_in_str(cell_below.value, null_tags):
                    b = False
                    break
        return b
    
    def update_header_info(self):
        # 将col和idx更新为下一个header的col和排序
        self._col = self._header_next_col
        self._idx = self._next_idx

        # 获取header的_range、_content、_content_range、_width、_end_col
        cell = self._ws.range(self._row, self._col)
        address = cell.merge_area.address
        self._range = convert_xlsx_addr(address)
        self._content_range = tuple((self._content_row, self._range[i][1]) \
            for i in range(len(self._range)))
        self._content = str(cell.value)

        range_len = len(self._range)
        if range_len == 1:
            self._width = 1
            self._end_col = self._range[0][1]
        elif range_len == 2:
            self._width = self._range[1][1] - self._range[0][1] + 1
            self._end_col = self._range[1][1]
        else:
            raise ValueError("header range error")

        # _name: 如果header的内容中包含%，则取%前面的内容作为name
        # 如果%拆分后得到name==’’，或者content包含null_tags，则name为None
        ss = [i.strip() for i in re.split(header_split_char, self._content)]
        if ss:
            self._name = ss[0] if not check_any_text_in_str(ss[0], null_tags) else None
            for i in ('int', 'float', 'str'):
                if i in ss:
                    self._convert_type = i
                    break
                else:
                    self._convert_type = None
        else:
            self._name = None
            self._convert_type = None

        # 获取header的_type，如果有'list'，则为list，否则为dict。空的Cell默认为dict
        self._type = 'list' if 'list' in ss else 'dict'
        
        # 根据传入的data的_type（也就是父节点的_type，f_type），决定header的_index
        # 如果f_type是dict，那么index就是name，如果是list，那么index就是idx
        if self._data._type == 'list':
            self._index = str(self._idx)
        elif self._data._type == 'dict':
            self._index = str(self._name) if self._name else None
        else:
            print(self._data._type)
            raise ValueError("data type must be 'list' or 'dict'")

        self.is_header_v_end = self.check_header_v_end()
    

class Sheet(Sheet_):
    def __init__(self, ws, json_folder=None, OneFilePerLine=None, Dumpformat=None, \
        impl=None):
        super().__init__(ws)
        self._ws = ws
        self.json_folder = json_folder
        self.OneFilePerLine = OneFilePerLine
        self.Dumpformat = Dumpformat
        self.update_sheet_info()

    def update_sheet_info(self):
        # 获取headers的起始行、终止行
        self.headers_start_row = 1
        self.content_end_row = self._ws.range('1:1').end('down').row
        vertical_notes = self._ws.range(1, 1).expand('down').value
        self.headers_end_row =\
            next(idx+1 for idx, i in enumerate(reversed(vertical_notes)) if i == 'h')
        self.content_start_row = self.headers_end_row + 1

        # 获取headers的起始列、终止列
        col = 1
        first_headers = []
        while self._ws.range(1, col).value or self._ws.range(1, col).merge_cells:
            first_headers.append(self._ws.range(1, col).value)
            col += 1
            
        self.headers_end_col = len(first_headers)
        self.id_col = next(iter(idx+1 for idx, i in enumerate(first_headers) \
            if str(i).upper() == 'ID'))
        self.headers_start_col = self.id_col + 1
        # print(self.__dict__)
    
    def process_content_rows(self):
        ids = [str(x) for x in self._ws.range((1, self.id_col), \
            (self.content_end_row, self.id_col)).value[self.content_start_row-1:]]
        seen = set()
        dupes = [x for x in ids if x in seen or seen.add(x)]
        dupes_dict = {d:0 for d in dupes}
        if not os.path.exists(self.json_folder):
            os.mkdir(self.json_folder)

        if self.OneFilePerLine:
            self.json_folder = os.path.join(self.json_folder, self._ws.name)
            if not os.path.exists(self.json_folder):
                os.mkdir(self.json_folder)
            if dupes:
                print("!!!! Dupes found. Previous lines will be overwritten.")
            for content_row in range(self.content_start_row, self.content_end_row+1):
                if str(self._ws.range(content_row, 1).value).startswith('#'):
                    continue
                else:
                    data = UnifiedData('dict')
                    idd = ids[content_row-self.content_start_row]

                    headers = Headers(self, content_row, self.headers_start_row, \
                        self.headers_start_col, self.headers_end_col, data, next_idx=0)
                    fill_data(headers)
                    rendered_data = render_unified_data(data)

                    f_path = os.path.join(self.json_folder, idd + '.json')
                    print("exported: {0}".format(f_path))
                    with open(f_path, 'w', encoding='utf-8') as f:
                        f.write(special_dumps(rendered_data, self.Dumpformat))

        else:
            init_cell_value = self._ws.range(1, 1).value
            if wrap_list_reg.match(init_cell_value):
                print("wrap detect")
                data = UnifiedData('list')
                for content_row in range(self.content_start_row, self.content_end_row+1):
                    if str(self._ws.range(content_row, 1).value).startswith('#'):
                        continue
                    else:
                        row_idx = str(content_row)
                        idd = ids[content_row-self.content_start_row]
                        if idd in dupes:
                            print("!!!! duplicate id: {0} in row: {1}".format(idd, content_row))
                        data[row_idx] = UnifiedData('dict')
                        headers = Headers(self, content_row, self.headers_start_row, \
                            self.headers_start_col, self.headers_end_col, data[row_idx], next_idx=0)
                        fill_data(headers)
                output = UnifiedData('dict')
                key = wrap_key_reg.findall(init_cell_value)[0]
                output[key] = data
                data = output
            else:
                for content_row in range(self.content_start_row, self.content_end_row+1):
                    if str(self._ws.range(content_row, 1).value).startswith('#'):
                        continue
                    else:
                        idd = ids[content_row-self.content_start_row]
                        if idd in dupes:
                            print("!!!! duplicate id: {0} in row: {1}".format(idd, content_row))
                            if dupes_dict[idd] == 0:
                                data[idd] = UnifiedData('list')
                            dup_idx = str(dupes_dict[idd])
                            data[idd][dup_idx] = UnifiedData('dict')
                            headers = Headers(self, content_row, self.headers_start_row, \
                                self.headers_start_col, self.headers_end_col, \
                                    data[idd][dup_idx], next_idx=0)
                            fill_data(headers)
                            dupes_dict[idd] += 1
                        else:
                            data[idd] = UnifiedData('dict')
                            headers = Headers(self, content_row, self.headers_start_row, \
                                self.headers_start_col, self.headers_end_col, data[idd], next_idx=0)
                            fill_data(headers)
            rendered_data = render_unified_data(data)
            f_path = os.path.join(self.json_folder, self._ws.name + '.json')
            print("exported: {0}".format(f_path))
            with open(f_path, 'w', encoding='utf-8') as f:
                f.write(special_dumps(rendered_data, self.Dumpformat))

def excel2json(wb_path):
    if len(sys.argv) > 1:
        wb_path = sys.argv[1]
    app, wb = xw_open(wb_path)
    cmd_ws = wb.sheets['cmd']
    
    parent_folder = os.path.dirname(wb_path)
    task_end_row = cmd_ws.range('1:1').end('down').row
    header_end_col = cmd_ws.range('1:1').end('right').column
    header_cols = {h: idx for idx, h in enumerate(cmd_ws.range(1, 1).expand('right').value)}
    # cmds = {}
    for row in range(2, task_end_row+1):
        if str(cmd_ws.range(row, 1).value).startswith('#'):
            continue
        else:
            row_content = cmd_ws.range((row, 1), (row, header_end_col)).value
            Task = row_content[header_cols['Task']]
            print("\n>>> Task: {0}".format(Task))
            SheetName = row_content[header_cols['SheetName']]
            Export = row_content[header_cols['Export']]
            # Rewrite = row_content[header_cols['Rewrite']]
            OneFilePerLine = True if row_content[header_cols['OneFilePerLine']] else False
            # IgnoreNull = True if row_content[header_cols['IgnoreNull']] else False

            OutputFolder = os.path.join(parent_folder, \
                row_content[header_cols['OutputFolder']])
            DumpFormat = row_content[header_cols['DumpFormat']]
            if Export:
                ws = wb.sheets[SheetName]
                sh = Sheet(ws, OutputFolder, OneFilePerLine, DumpFormat)
                sh.process_content_rows()
    wb.close()
    app.kill()
            
    

def convert_cell_value(src, convert_type=None):
    if json_str_reg.match(str(src)):
        rlt = json5.loads(src)
    elif src:
        if convert_type == 'int':
            try:
                rlt = int(src)
            except:
                raise ValueError("cannot convert to int")
        elif convert_type == 'str':
            try:
                rlt = str(src)
            except:
                raise ValueError("cannot convert to str")
        elif convert_type == 'float':
            try:
                rlt = float(src)
            except:
                raise ValueError("cannot convert to float")
        elif convert_type is None:
            rlt = src
        else:
            rlt = src
    else:
        rlt = src
    return rlt

def convert_cell_values(srcs, convert_type):
    if type(srcs) is list:
        rlt = [convert_cell_value(src, convert_type) for src in srcs]
    else:
        rlt = convert_cell_value(srcs, convert_type)
    return rlt


def fill_data(headers):
    for h in headers:
        # print(h.__dict__)
        f_type = h._data._type
        if h.is_header_v_end: # 已经到达Header的垂直结束位置，分情况进行数据填充
            if f_type == "dict":
                if h._type == "dict":
                    h._data[h._index] = \
                        convert_cell_values(h._ws.range(*h._content_range).value, h._convert_type)
                elif h._type == "list":
                    if h._width == 1:
                        h._data[h._index] = \
                            [convert_cell_values(h._ws.range(*h._content_range).value, h._convert_type)]
                    else:
                        h._data[h._index] = \
                            convert_cell_values(h._ws.range(*h._content_range).value, h._convert_type)
                        
            elif f_type == "list":
                if h._type == "dict":
                    if h._name:
                        h._data[h._index] = \
                            {h._name: convert_cell_values(h._ws.range(*h._content_range).value, h._convert_type)}

                    else: # 如果list下边是空Cell或者标注null_tags的Cell，直接把数据注册到list下
                        h._data[h._index] = \
                            convert_cell_values(h._ws.range(*h._content_range).value, h._convert_type)
                        
                elif h._type == "list":
                    h._data[h._index] = convert_cell_values(h._ws.range(*h._content_range).value, h._convert_type)

        else: # 如果未到达header的垂直末尾，则进行递归
            h._data[h._index] = UnifiedData(h._type)
            sub_headers = Headers(h._ws, h._content_row, h._row+1, h._col, \
                h._end_col, h._data[h._index], next_idx=0)
            fill_data(sub_headers)


def main():
    TestHeader = True
    if TestHeader:
        wb_path = r".\xlsx\test.xlsx"
        if len(sys.argv) > 1:
            wb_path = sys.argv[1]
        excel2json(wb_path)
        

if __name__ == "__main__":
    main()