import sys
from .excel2json import excel2json



def main(wb_path):
    excel2json(wb_path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide an Excel file as an argument")