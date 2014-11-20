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
def getColorSchemes(path="ColorBrewerDivSchemes.csv"):
    s = readFile(path)
    sLine = s.splitlines()
    maxNum = 12
    colorSchemes = [0] * maxNum
    for i in xrange(maxNum):
        colorSchemes[i] = []
    # save line by line; ignore first line, which is column names
    for line in sLine[1:]: 
        sepLine = line.split(",")
        classNum = sepLine[1]
        colorIndex = int(sepLine[3])
        (r,g,b) = tuple(int(a) for a in sepLine[4:])
        # if a new scheme started
        if len(classNum)>0 and int(classNum)<maxNum:
            colorSchemes[int(classNum)] += [[(r,g,b)]]
            currentClass = int(classNum)
        else:
            colorSchemes[currentClass][-1] += [(r,g,b)]
    return colorSchemes

divSchemes = getColorSchemes()



