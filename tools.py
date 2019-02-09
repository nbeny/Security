import os

def create_directory(data="data"):
    path = os.getcwd()
    path += "/" + data + "/"

    try:
        os.mkdir(path)
    except OSError:
        print("[-] Creation of the directory %s failed" % path)
    else:
        print("[+] Successfully created the directory %s" % path)


def add_in_file(data=None, file="None"):
    if data is None:
        return None
    
    path = os.getcwd()
    path += "/data/%s_spoof.txt" % file

    try:
        file = open(path, "a+")
        file.write(data)
        file.close()
    except OSError:
        print("[-] Creation of the file %s failed" % path)
