import pprint
import re
import xlwings as xw

def render_unified_data(obj, ignore_null=True):
    # print("render_unified_data is called")
    keys = set(obj.__dict__.keys())
    keys.remove('_type')
    # 如果数据类型是list，那么需要对key进行排序，按照数字大小排序输出为list
    if obj._type == 'list':
        # if ignore_null:
        #     sorted_keys = sorted([int(i) for i in keys if obj.__dict__[i] is not None])
        #     # print("ignore is True and sorted_keys is {0}".format(sorted_keys))
        # else:
        sorted_keys = sorted([int(i) for i in keys])
            # print("ignore is False and sorted_keys is {0}".format(sorted_keys))
        l = len(sorted_keys)
        remap_keys = range(l)
        m = {remap_keys[i]:str(sorted_keys[i]) for i in range(l)}
        rlt = [None for i in range(l)]
        for idx, attr in m.items():
            if type(obj.__dict__[attr]) is UnifiedData:
                rlt[idx] = render_unified_data(obj.__dict__[attr])
            else:
                rlt[idx] = obj[attr]
    # 如果数据类型是dict，那么直接输出为dict
    elif obj._type == 'dict':
        rlt = {}
        for i in keys:
            # print(obj.__dict__[i])
            if type(obj.__dict__[i]) is UnifiedData:
                rlt[i] = render_unified_data(obj.__dict__[i])
            else:
                # print(obj.__dict__[i])
                # if ignore_null and obj.__dict__[i] is None:
                #     print("found empty cell")
                #     continue
                # else:
                rlt[i] = obj[i]
    else:
        raise ValueError("obj._type error")
    return rlt

class UnifiedData:
    # 标记数据类型，把数据注册到这个类里面
    def __init__(self, t):
        if t in ('list', 'dict'):
            self._type = t
        else:
            # print(t)
            raise ValueError("type input error {0}".format(t))
    
    def __setitem__(self, index, value):
        self.__dict__[str(index)] = value
    def __getitem__(self, index):
        return self.__dict__[str(index)]
    def __setattr__(self, index, value):
        self.__dict__[str(index)] = value
    def __getattr__(self, index):
        return self.__dict__[str(index)]

def xw_open(wb_path, if_visible=True):
    apps = xw.apps
    if apps:
        for a in apps:
            if wb_path in [b.fullname for b in a.books]:
                app = a
                break
        else:
            app = list(apps)[0]
    else:
        app = xw.apps.add(visible=if_visible)
    # print(app)
    books = app.books
    # print(books)
    book_names = [b.fullname for b in books]
    if books and wb_path in book_names:
        book_idx = book_names.index(wb_path)
        wb = books[book_idx]
    else:
        wb = app.books.open(wb_path)
    return app, wb
# def print(obj):

def pretty_print(obj, pretty_dump=False):
    if pretty_dump:
        string = self_defined_dumps(obj)
        print(string)
        rlt = string
    else:
        hook = pprint.PrettyPrinter(indent=4)
        hook.pprint(obj)
        rlt = obj
    return rlt
    

# print return decorator
def deco_print_return(if_print=True, if_pretty=False):
    def deco(func):
        def wrapper(*args, **kwargs):
            rlt = func(*args, **kwargs)
            if if_print :
                if if_pretty:
                    pretty_print(rlt)
                else:
                    print(rlt)
            return rlt
        return wrapper
    return deco
        
# if try decorator
def deco_try(if_try=True):
    def deco(func):
        def wrapper(*args, **kwargs):
            if if_try:
                try:
                    rlt = func(*args, **kwargs)
                except Exception as e:
                    print(e)
            else:
                rlt = func(*args, **kwargs)
            return rlt
        return wrapper
    return deco

# @print_return(pr=True, pretty=True)
def convert_xlsx_addr(addr):
    def col_to_num(col_str):
        """ Convert base26 column string to number. """
        expn = 0
        col_num = 0
        for char in reversed(col_str):
            col_num += (ord(char) - ord('A') + 1) * (26 ** expn)
            expn += 1
        return col_num
    reg = re.compile(r"([a-zA-Z]+|[0-9]+)")
    # reg_num = re.compile(r"[0-9]+")
    strs = reg.findall(addr)
    # print(strs)
    rlts = []
    for s in strs:
        if s.isdigit():
            rlts.append(int(s))
        else:
            rlts.append(col_to_num(s.upper()))
    # print(rlts)
    if len(rlts) == 1:
        result = rlts[0]
    elif len(rlts) == 2:
        result = tuple([(rlts[1], rlts[0])])
    elif len(rlts) == 4:
        result = ((rlts[1], rlts[0]), (rlts[3], rlts[2]))
    else:
        raise ValueError("address format error")

    return result

# 将json按照自定义的深度、缩进、排序方式输出
def self_defined_dumps(obj, depth=2, indent=4, sort_dict=True):
    from io import StringIO
    output = StringIO()
    dump_obj(obj, output, depth, indent, type(obj), sort_dict)            
    # print(len(output))
    contents = output.getvalue()[:-2]
    output.close()
    return contents

def dump_obj(obj, output, depth, indent, f_type, sort_dict=True, level=0, is_key=False, is_value=False):
    m = 1 if level <= depth+1 else 0
    n = 1 if level <= depth else 0
    next_level = level + 1
    ## process dict
    if isinstance(obj, dict):
        output.write("{")
        ## sort dict by key
        if sort_dict:
            obj = dict(sorted(obj.items(), key=lambda item: item[0]))
        for k, v in obj.items():
            dump_obj(k, output, depth, indent, dict, sort_dict=sort_dict, level=next_level, is_key=True)
            dump_obj(v, output, depth, indent, dict, sort_dict=sort_dict, level=next_level, is_value=True)
        output.write(("\n" + " "*level*indent)*n + "}, ")
    ## process list
    elif isinstance(obj, list):
        output.write("[")
        for v in obj:
            dump_obj(v, output, depth, indent, list, sort_dict=sort_dict, level=next_level, is_key=False)
        output.write("], ")
    else:
        ## process keys
        if is_key:
            output.write(("\n" + " "*level*indent)*m + obj +": ")
        ## process non keys
        else:
            if type(obj) is str:
                output.write('"' + str(obj) + '", ')
            else:
                if str(obj) == "True":
                    output.write("true, ")
                elif str(obj) == "False":
                    output.write("false, ")
                elif str(obj) == "None":
                    output.write("null, ")
                else:
                    output.write(str(obj) + ', ')

if __name__ == "__main__":

    # a = "$A$1:$J$1"
    # b = "A1"
    # c = "a12"
    # print(a)
    # print(b)
    # print(c)
    d = {"a": 1, "b": 2, "c": 3}
    print(self_defined_dumps(d))

    # print(convert_address(a))
    # print(convert_address(b))
    # print("12".isdigit())
    # is_digit("12")
    
    # convert_xlsx_addr(a)
    # convert_xlsx_addr(b)
    # convert_xlsx_addr(c)
    pass