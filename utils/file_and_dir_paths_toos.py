import os

def find_file(start, name):
    for rel_path, dirs, files in os.walk(start):
        if name in files:
            full_path = os.path.join(start, rel_path, name)
            print(os.path.normpath(os.path.abspath(full_path)))

if __name__ == '__main__':
    import glob
    import os
    print("glob.glob", glob.glob("test_text.txt"))
    print("cwd", os.getcwd())
    print("abspath", os.path.abspath('/data'))
    # print('os.path.dirname(os.path.realpath("test_text.txt")):  ', os.path.dirname(os.path.realpath("test_text.txt")))
    print('os.path.dirname(os.path.realpath("test_text.txt")):  ', os.path.dirname(os.path.realpath("data/test_text.txt")))
    # C:\Users\XGOBY\noname2\data
    # C:\Users\XGOBY\noname2
    # print("findfile func:  ", find_file())
    print(os.path.abspath('../data'))
    # cwd C:\Users\XGOBY\noname2\utils
    # print(os.path.join(os.path.abspath('../data'), "Semiconductors_stocks_data_01-06-2014_05-16-2019"))

