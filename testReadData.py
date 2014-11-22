import contextlib # for urllib.urlopen()
import os

# from lecture notes
def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

# from lecture notes
def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

# read in color scheme files, return a 3d list
def getData(path="defaultData.txt"):
    s = readFile(path)
    sLine = s.splitlines()
    data = []
    # ignore first line, which is name
    for line in sLine[1:]:
        (x, y, myClass) = tuple( float(a) for a in line.split("\t"))
        data += [(x, y, myClass)]
    return data
    
data = getData()




