# termProjectPython2.py
# name: Lingxue Zhu
# andrewId: lzhu1
# section: L
# Cited 3 functions from lecture notes and 1 from stackoverflow.com

import copy
import colorsys
import os
import math
import numpy as np
import cv2

from Tkinter import *
import ttk
import Tkconstants, tkFileDialog
from eventBasedAnimationClass2 import EventBasedAnimationClass

# turn rgb into hex strings; from lecture notes
def rgbString( red, green, blue ):
        return "#%02x%02x%02x" % (red, green, blue)

# read files; from lecture notes
def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

# write files: from lecture notes
def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

# a class to read-in and handle data
class Data(object):
    # constructor
    def __init__(self, canvas, filePath):
        self.canvas = canvas
        self.lineCol = rgbString(98,98,98)
        self.fontSize = 15
        self.filePath = filePath
        self.getData()

    # read in data from a file, save as a 1d list with tuples (x,y,class)
    def getData(self, isAutoClust=False, clusterNum = 2):
        s = readFile(self.filePath)
        sLine = s.splitlines()
        data = []
        # get data from file; ignore first line, which is name
        for line in sLine[1:]:
            (x, y, myClass) = tuple( float(a) for a in line.split("\t"))
            myClass = int(myClass)
            data += [(x, y, myClass)]
        self.originalData = data
        # k-means if needed
        if isAutoClust:
            self.data = self.kMeans(clusterNum)
        else: 
            self.data = self.originalData
        # get frequency
        self.getFreq()

    # k-means clustering; modified from http://docs.opencv.org/...
    # ...trunk/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/...
    # ...py_kmeans_opencv.html
    def kMeans(self, clusterNum):
        # turn to numpy array
        npData = np.array(self.originalData)
        Z = np.float32(npData[npData[:,2]<=clusterNum,:])
        Z = Z[:, [0,1]]
        # define criteria and apply kmeans()
        maxIter, eps, attempts = 10, 1.0, 10
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                            maxIter, eps)
        ret,label,center=cv2.kmeans(Z,clusterNum,criteria,attempts,
                            cv2.KMEANS_PP_CENTERS)
        return np.hstack((Z, label+1)).tolist()
        
    # get frequency of each class
    def getFreq(self):
        freq = [0]
        for (x, y, myClass) in self.data:
            myClass = int(myClass)
            # new class
            if myClass> len(freq):
                freq += [0]*(myClass - len(freq))
            # add count
            freq[myClass-1] += 1
        self.freq = freq
        self.totalClass = len(freq)

    # get the minX, minY, maxX, maxY for plot
    def getRange(self, classNum):
        xRange = [None, None]
        yRange = [None, None]
        for (x, y, myClass) in self.data:
            if myClass <= classNum:
                if xRange[0]==None or x<xRange[0]: xRange[0] = x
                if xRange[1]==None or x>xRange[1]: xRange[1] = x
                if yRange[0]==None or y<yRange[0]: yRange[0] = y
                if yRange[1]==None or y>yRange[1]: yRange[1] = y
        self.xRange = xRange
        self.yRange = yRange

    # plot data
    def plotData(self, viewType, x, y, w, h, classNum, colSchm):
        if viewType == "barPlot": 
            self.drawBarPlot(x, y, w, h, classNum, colSchm)
        elif viewType == "pieChart": 
            self.drawPieChart(x, y, w, h, classNum, colSchm)
        elif viewType == "scatPlot": 
            self.drawScatPlot(x, y, w, h, classNum, colSchm)

    # bar plot
    def drawBarPlot(self, x, y, w, h, classNum, colSchm):
        lineCol, fontSize = self.lineCol, self.fontSize
        # x, y axes
        self.canvas.create_line(x, y+h, x+w, y+h, arrow=LAST, fill=lineCol)
        self.canvas.create_line(x, y+h, x, y, arrow=LAST, fill=lineCol)
        # frequences
        barWidth, maxFreq = w/(classNum+2), max(self.freq[0:classNum])
        margin = barWidth
        for i in xrange(classNum):
            (r,g,b), prop = colSchm[i], self.freq[i]/float(maxFreq)
            self.canvas.create_rectangle(x+margin+barWidth*i, 
                            y+h-prop*(h-margin), x+margin+barWidth*(i+1), y+h,
                            fill=rgbString(r,g,b))
            self.canvas.create_text(x+margin+barWidth*i+barWidth/2, 
                            y+h+fontSize/2, anchor = N, text=str(i+1), 
                            fill=lineCol, font=("Arial",fontSize,"bold"))
        # x, y labels
        self.canvas.create_text(x+w/2, y+h+fontSize*1.5, anchor=N,
                            text="Class", fill=lineCol,
                            font=("Arial",fontSize,"bold"))
        self.canvas.create_text(x+fontSize/2, y, anchor=NW, text="Frequency",
                            fill=lineCol, font=("Arial",fontSize,"bold"))

    # pie chart
    def drawPieChart(self, x, y, w, h, classNum, colSchm):
        margin, fontSize = w/20, self.fontSize
        cx, cy = x+margin+(w-margin*2)/2.0, y+margin+(h-margin*2)/2.0
        radius = (w - margin*2)/2.5
        totalFreq, totalDeg = sum(self.freq[0:classNum]), 360
        # draw chart
        for i in xrange(classNum):
            (r,g,b) = colSchm[i]
            startDeg = (sum(self.freq[0:i])/float(totalFreq)) * totalDeg
            extentDeg = (self.freq[i]/float(totalFreq))*totalDeg
            self.canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                            start = startDeg, extent = extentDeg,
                            fill = rgbString(r,g,b), outline = self.lineCol)
            # class label
            radian = math.radians(startDeg+extentDeg/2)
            self.canvas.create_text(cx+radius*math.cos(radian)*2/3, 
                            cy-radius*math.sin(radian)*2/3, 
                            anchor=N, text=str(i+1), fill = self.lineCol,
                            font=("Arial",fontSize,"bold"))

    # scatter plot
    def drawScatPlot(self, x, y, w, h, classNum, colSchm):
        self.getRange(classNum)
        lineCol, fontSize = self.lineCol, self.fontSize
        dotR, margin = 3, w/20
        # x, y axes
        self.canvas.create_line(x, y+h, x+w, y+h, arrow=LAST, fill=lineCol)
        self.canvas.create_line(x, y+h, x, y, arrow=LAST, fill=lineCol)
        self.canvas.create_text(x+w/2, y+h+fontSize/2, anchor=N, text="X",
                            fill=lineCol, font=("Arial",fontSize,"bold"))
        self.canvas.create_text(x-fontSize/2, y+h/2, anchor=E, text="Y",
                            fill=lineCol, font=("Arial",fontSize,"bold"))
        for (myX, myY, myClass) in self.data:
            myClass = int(myClass)
            if myClass <= classNum:
                (r,g,b) = colSchm[myClass-1]
                # calculate screen location
                xProp = (myX-self.xRange[0])/(self.xRange[1]-self.xRange[0])
                yProp = (myY-self.yRange[0])/(self.yRange[1]-self.yRange[0])
                screenX = x+margin+xProp*(w-margin*2)
                screenY = y+h-margin-yProp*(h-margin*2)
                self.canvas.create_oval(screenX-dotR, screenY-dotR,
                            screenX+dotR, screenY+dotR,
                            fill=rgbString(r,g,b), outline=self.lineCol)

# a class to read-in and draw default color schemes
class DefaultColorSchemes(object):
    # constructor
    def __init__(self, canvas, filePath):
        self.canvas = canvas
        self.schmWidth, self.schmHeight, self.margin = 19, 19, 15
        self.textMargin, self.maxLen, self.maxPerLine = 5, 4, 9
        self.minClassNum, self.maxClassNum = 3, 11
        self.lwd, self.hCol = 7, rgbString(178, 178, 178)
        self.colorSchemes = self.getColorSchemes(filePath)

    # read in color scheme files, return a 3d list
    def getColorSchemes(self, path):
        s = readFile(path)
        sLine = s.splitlines()
        maxClassNum = self.maxClassNum
        colorSchemes = [0] * (maxClassNum+1)
        for i in xrange(maxClassNum+1):
            colorSchemes[i] = []
        # save line by line; ignore first line, which is column names
        for line in sLine[1:]: 
            sepLine = line.split(",")
            classNum = sepLine[1]
            (r,g,b) = tuple(int(a) for a in sepLine[4:])
            # if a new scheme started
            if len(classNum)>0 and int(classNum)<=maxClassNum:
                colorSchemes[int(classNum)] += [[(r,g,b)]]
                currentClass = int(classNum)
            else:
                colorSchemes[currentClass][-1] += [(r,g,b)]
        return colorSchemes

    # draw one scheme at given location
    def drawSingleScheme(self, x, y, scheme, detail=False, truncate=False,
                        compress=False, highlight=None):
        tMargin, maxLen, topY, lwd = self.textMargin, self.maxLen, y, 3
        # compress height
        if compress:
            schmHeight=self.schmHeight*(self.minClassNum+1)/float(len(scheme))
        else: schmHeight = self.schmHeight
        # only show selected 5 colors 
        if truncate and len(scheme)>maxLen:
            step = len(scheme)/ (maxLen-1)
            selectI = [0, step,len(scheme)-1-step ,len(scheme)-1]
            scheme = [ scheme[i] for i in selectI ]
        # colors
        for (r,g,b) in scheme:
            self.canvas.create_rectangle(x, y, x+self.schmWidth, y+schmHeight,
                            fill=rgbString(r, g, b), 
                            outline=rgbString(128, 128, 128), width=2)
            # information
            if detail: self.canvas.create_text( x+self.schmWidth+tMargin, 
                            y+schmHeight/2, anchor=W, text=rgbString(r,g,b), 
                            font=("Arial", 10), fill=rgbString(90,90,90))
            y += schmHeight 
        # highlight if specified
        if highlight != None: 
            self.canvas.create_rectangle(x-lwd/2, 
                            topY+schmHeight*highlight-lwd/2,
                            x+self.schmWidth, topY+schmHeight*(highlight+1),
                            outline=rgbString(120,120,120), width=lwd+1)

    # given start (x,y), get the leftX and topY position for i-th scheme 
    def getLeftTop(self, x, y, classNum, i):
        left = x + (self.schmWidth+self.margin)*(i % self.maxPerLine)
        top = y
        if i >= self.maxPerLine:
            top += self.schmHeight*self.maxLen + self.margin
        return (left, top)        

    # draw color schemes at given location on canvas
    def drawSchemes(self, x, y, classNum, curSchm):
        schemes = self.colorSchemes[classNum]
        lwd, hCol = self.lwd, self.hCol
        # highlight current scheme
        (left, top) = self.getLeftTop(x, y, classNum, curSchm)
        self.canvas.create_rectangle( left-lwd/2, top-lwd/2, 
                    left+self.schmWidth+lwd/2, 
                    top+self.schmHeight*min(classNum, self.maxLen)+lwd/2,
                    outline=hCol, width=lwd)
        # draw all schemes
        for i in xrange(len(schemes)):
            scheme = schemes[i]
            (left, top) = self.getLeftTop(x, y, classNum, i)
            self.drawSingleScheme(left, top, scheme, truncate=True)

    # get which color scheme did (newX, newY) fell into
    def getCurrentScheme(self, x, y, newX, newY, classNum):
        schemes = self.colorSchemes[classNum]
        for i in xrange(len(schemes)):
            (left, top) = self.getLeftTop(x, y, classNum, i)
            right = left+self.schmWidth
            bottom = top+self.schmHeight*min(classNum, self.maxLen)
            if (left<=newX and newX<=right and top<=newY and newY<=bottom):
                return i
        return None

    # get which color within scheme did (newX, newY) fell into
    def getWorkingColor(self, (left, top), newX, newY, classNum):
        right = left+self.schmWidth
        for i in xrange(classNum):
            bottom = top+self.schmHeight
            if (left<=newX and newX<=right and top<=newY and newY<=bottom):
                return i
            top += self.schmHeight
        return None

# class to generate and draw color wheel
class ColorWheel(object):
    # constructor
    def __init__(self, canvas, cx, cy, r, startColor=(255,0,0)):
        self.cx, self.cy, self.r = cx, cy, r
        self.startColor = startColor
        self.canvas = canvas

    # return left and right adjacency colors; from online:
    # stackoverflow.com/questions/14095849/...
    # ...calculating-the-analogous-color-with-python
    def adjacent_colors(self, r, g, b, deg=30): 
        d = deg/360.
        r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
        h, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
        h = [(h+d) % 1 for d in (-d, d)]           # Rotation by d
        l = 0.8*l
        adjacent = []
        for hi in h:
            r, g, b = colorsys.hls_to_rgb(hi, l, s)
            r, g, b = int(round(r*255)), int(round(g*255)), int(round(b*255)),
            adjacent += [(r,g,b)] # H'LS -> new RGB
        return adjacent

    # draw color wheel
    def drawColorWheel(self):
        cx, cy, r = self.cx, self.cy, self.r
        startColor = self.startColor
        degStep, startDeg, fullDeg = 2, 0, 360
        # color wheel
        for i in xrange(int(fullDeg/degStep)+1):
            currentColor = self.adjacent_colors(*startColor, deg=i*degStep)[1]
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                            start = startDeg + i*degStep*360/fullDeg,
                            extent = degStep*360/fullDeg,
                            fill = rgbString(*currentColor), 
                            outline = rgbString(*currentColor))

# the main app
class ColorYourData(EventBasedAnimationClass):
    # constructor
    def __init__(self, width=900, height=650, dataFile="defaultData.txt"):
        super(ColorYourData, self).__init__(width, height)
        self.dataFile = dataFile

    # init
    def initAnimation(self):
        # layout set up
        self.titleSize, self.subtitleSize, self.textSize =30, 14, 12 
        self.subFont = ("Arial",self.subtitleSize,"bold")
        self.subCol  = rgbString(90,90,90) 
        self.backCol = "white"
        self.lZoneWidth = self.width*2/5
        self.bMargin, self.cMargin, self.margin = 30, 5, 5
        # initialization
        self.initZoneLoc()
        self.initData()
        self.initDefaultSchemes()
        self.initYourSchemes()
        self.initFavorites()
        self.initWidgets()       
        self.initView()
        self.timerDelay = None

    # initialize toplelf (x,y), width, height of all zones
    def initZoneLoc(self):
        self.zoneLoc = []
        # zone 0: title
        (x, y) = (self.cMargin+self.lZoneWidth, self.cMargin)
        (w, h) = (self.width-2*self.cMargin-self.lZoneWidth, 
                    self.titleSize*2+self.subtitleSize)
        self.zoneLoc += [(x,y,w,h)]
        # zone 1: view plots
        (x, y) = (self.zoneLoc[0][0], self.zoneLoc[0][1]+self.zoneLoc[0][3])
        (w, h) = (self.zoneLoc[0][2], self.height*3/5)
        self.zoneLoc += [(x,y,w,h)]
        # zone 2: favorites
        (x, y) = (self.zoneLoc[0][0], self.zoneLoc[1][1]+self.zoneLoc[1][3])
        (w, h) = (self.zoneLoc[1][2], self.height-self.bMargin-y)
        self.zoneLoc += [(x,y,w,h)]
        # zone 3: #of classes
        (x, y) = (self.cMargin, self.cMargin)
        (w, h) = (self.lZoneWidth, self.subtitleSize*2)
        self.zoneLoc += [(x,y,w,h)]
        # zone 4: default color scheme
        (x, y) = (self.cMargin, self.zoneLoc[3][1]+self.zoneLoc[3][3])
        (w, h) = (self.lZoneWidth, self.height/2.5)
        self.zoneLoc += [(x,y,w,h)]
        # zone 5: design your color
        (x, y) = (self.cMargin, self.zoneLoc[4][1]+self.zoneLoc[4][3])
        (w, h) = (self.lZoneWidth, self.height-self.bMargin-y)
        self.zoneLoc += [(x,y,w,h)]

    # initialize favorite schemes
    def initFavorites(self):
        self.favSchm = []
        self.favMargin = self.defSchm.margin*2/3
        self.favDelCol = rgbString(168,168,168)
        self.favDelWidth = self.defSchm.schmWidth*2/3
        
    # initialize all buttons, combo boxes
    def initWidgets(self):
        self.radiobutton()
        self.checkbutton()
        self.combobox()
        self.root.bind("<<ComboboxSelected>>", 
                        lambda event: self.onComboboxSelection(event))
        self.saveButton()
        self.exportButton()
        self.importButton()
        self.clearButton()

    # initialize default color schemes
    def initDefaultSchemes(self):
        self.classNum, self.minClass = 3, 3
        self.maxClass = min(10, self.data.totalClass)
        path = "ColorBrewerSchemes.csv"
        self.defSchm = DefaultColorSchemes(self.canvas, path)
        self.curDefSchm = 0
        self.curSchm=self.defSchm.colorSchemes[self.classNum][self.curDefSchm]
        # location
        (x, y, w, h) = self.zoneLoc[4]
        self.defSchmLoc = (x+self.margin*3, y+self.subtitleSize*2.5)
        # working scheme
        self.workZone = 4

    # intialize user-select color schemes: all white (0,0,0)
    def initYourSchemes(self):
    	self.yourSchm, fullRGB = [], 255
    	for i in xrange(self.classNum):
    		self.yourSchm += [(fullRGB, fullRGB, fullRGB)]
    	# wheel location
    	(x, y, w, h) = self.zoneLoc[5]
        self.cx, self.cy, self.r = x+w/3, y+h/2, w/4
        self.colorWheel = ColorWheel(canvas=self.canvas, cx=self.cx, 
        						cy=self.cy, r=self.r)
        # color schm location; current active col
        self.yourColLoc = (x+w*2/3, 
                        self.cy-self.defSchm.schmHeight*self.classNum/2)
        self.curYourCol = 0

    # intialize data
    def initData(self):
        self.data = Data(self.canvas, self.dataFile)
        self.isAutoClust = False

    # initialize the view system
    def initView(self):
        self.viewType = "barPlot"
        self.data = Data(self.canvas, self.dataFile)
        
    # build radio buttons for zone 1
    def radiobutton(self):
        # a frame to put the buttons
        self.radioFrame = Frame(self.root, bg = self.backCol)
        (x, y, w, h) = self.zoneLoc[1]
        xMargin, yMargin = 50, self.subtitleSize
        self.radioFrame.place(x=x+xMargin, y=y+yMargin, anchor=W)
        # put buttons
        viewTypes = [("Bar plot", "barPlot"), ("Pie chart", "pieChart"),
                    ("Scatter plot", "scatPlot")]
        self.radioValue = StringVar()
        self.radioValue.set("barPlot")       
        for i in xrange(len(viewTypes)):
            (text, viewType) = viewTypes[i]
            self.radio = Radiobutton(self.radioFrame,  text=text,
                        variable = self.radioValue, value = viewType, 
                        command = self.newRadiobutton, width=13, 
                        font=("Arial",self.subtitleSize),
                        borderwidth=1)
            self.radio.grid(row=0, column=i)

    # react to radio buttions
    def newRadiobutton(self):
        self.viewType = self.radioValue.get()
        self.redrawAll()

    # build check button for zone 1
    def checkbutton(self):
        self.checkValue = IntVar()
        self.checkValue.set(0) # set initial state
        self.check = Checkbutton(self.root, text="Auto-cluster",
                        variable = self.checkValue, 
                        command = self.newCheckbutton, 
                        font=("Arial", self.textSize))
        (x, y, w, h) = self.zoneLoc[1]
        self.check.place(x=x+w-self.margin, 
                        y=y+self.margin+self.subtitleSize*2, anchor=NE)

    # react to check button
    def newCheckbutton(self):
        self.isAutoClust = bool(self.checkValue.get())
        self.data.getData(self.isAutoClust, self.classNum)
        self.redrawAll()

    # build a combo box for zone 3
    def combobox(self):
        self.boxValue = StringVar()
        self.box = ttk.Combobox(self.root, textvariable=self.boxValue, 
                        justify="center", state="readonly", width=3)
        self.box["values"] = tuple(range(self.minClass, self.maxClass+1))
        self.box.current(0) 
        (x, y, w, h) = self.zoneLoc[3]
        xMargin, yMargin = 200, self.subtitleSize
        self.box.place(x=x+xMargin, y=y+yMargin, anchor="center")

    # react to combobox selection
    def onComboboxSelection(self, event):
        self.classNum = int(self.boxValue.get())
        self.curDefSchm = 0
        self.curSchm=self.defSchm.colorSchemes[self.classNum][self.curDefSchm]
        self.initYourSchemes()
        self.initData()
        self.checkValue.set(0)
        self.workZone = 4
        self.redrawAll()

    # build two buttons for saving as favorites
    def saveButton(self):
        self.saveButton1 = Button(self.canvas, text="Save to favorites",
                        command=self.onSaveButton,font=("Arial",self.textSize))
        (x, y, w, h) = self.zoneLoc[4]
        self.saveButton1.place(x=x+w-self.margin, y=y+h, anchor=SE)
        self.saveButton2 = Button(self.canvas, text="Save to favorites",
                        command=self.onSaveButton,font=("Arial",self.textSize))
        (x, y, w, h) = self.zoneLoc[5]
        self.saveButton2.place(x=x+w-self.margin, y=y+h, anchor=SE)

    # react to button click, save color schemes
    def onSaveButton(self):
        maxFavSchm = 17
        if len(self.favSchm) < maxFavSchm and self.curSchm not in self.favSchm:
            self.favSchm += [self.curSchm]
            self.redrawAll()

    # build export buttons for saving favorites in zone 2
    def exportButton(self):
        self.exportFavButton = Button(self.canvas, text='Export favorites',
                        command=self.exportFav,font=("Arial",self.textSize))
        (x, y, w, h) = self.zoneLoc[2]
        self.exportFavButton.place(x=x+w-self.margin, y=y+self.margin/2, 
                        anchor=NE)

    # save current favorite schemes to given file
    def exportFav(self):
        # get filename
        initialDir = "~/Documents/Courses/2014Fall/15-112/termProject"
        filename = tkFileDialog.asksaveasfilename(parent=self.canvas, 
                        defaultextension=".txt", initialdir= initialDir,
                        initialfile="myFavoriteSchemes.txt")
        # write to file
        contents = ""
        for scheme in self.favSchm:
            for (r,g,b) in scheme:
                contents += rgbString(r,g,b)+"\t"
            contents += "\n"
        writeFile(filename, contents)

    # build button to clear all favorites
    def clearButton(self):
        self.clearButton = Button(self.canvas, text='Clear favorites',
                        command=self.clearFav,font=("Arial",self.textSize))
        (x, y, w, h) = self.zoneLoc[2]
        rMargin = 120
        self.clearButton.place(x=x+w-rMargin, y=y+self.margin/2, 
                        anchor=NE)

    # clear all current favorites
    def clearFav(self):
        self.favSchm = []
        self.redrawAll()

    # build import buttons in zone 1
    def importButton(self):
        self.importButton = Button(self.canvas, text='Import data',
                        command=self.importData, font=("Arial",self.textSize))
        (x, y, w, h) = self.zoneLoc[1]
        self.importButton.place(x=x+w-self.margin,y=y+self.margin/2, anchor=NE)

    # import data from given file
    def importData(self):
        # get filename
        initialDir = "~/Documents/Courses/2014Fall/15-112/termProject"
        filename = tkFileDialog.askopenfilename(parent=self.canvas, 
                                        initialdir= initialDir)
        self.dataFile = filename
        self.initData()
        self.initDefaultSchemes()
        self.initYourSchemes()
        self.initFavorites()      
        self.initView()
        self.combobox()
        self.checkValue.set(0)
        self.radioValue.set("barPlot") 
        self.redrawAll()

    # react to mouse pressed
    def onMousePressed(self, event):
        self.clickZone = self.inWhichZone(event)
        self.onMousePressedZone(event)
        self.redrawAll()

    # react to mouse pressed inside each zone
    def onMousePressedZone(self, event):
        if self.clickZone == 2:
            self.delFavSchm(event.x, event.y)
        elif self.clickZone == 4:
            self.newDefSchm(event.x, event.y)
            self.workZone = 4
        elif self.clickZone == 5:
        	self.workZone = 5 
        	self.curSchm = self.yourSchm
        	self.newYourCol(event.x, event.y)

    # check which zone user clicked in
    def inWhichZone(self, event):
        for i in xrange(6):
            (x, y, w, h) = self.zoneLoc[i]
            if (x<=event.x and event.x<=x+w and y<=event.y and event.y<=y+h):
                return i
        return None      

    # check whether user selected a new default scheme
    def newDefSchm(self, newX, newY):
        (x, y) = self.defSchmLoc
        newSchm = self.defSchm.getCurrentScheme(x, y, newX,newY, self.classNum)
        if newSchm != None: 
            self.curDefSchm = newSchm
        self.curSchm=self.defSchm.colorSchemes[self.classNum][self.curDefSchm]

    # calculate the top left location to draw i-th favorate schemes
    def favSchmLoc(self, i):
        (x, y, w, h) = self.zoneLoc[2]
        margin = self.favMargin 
        schmWidth, schmHeight = self.defSchm.schmWidth, self.defSchm.schmHeight
        # color scheme
        leftX = x+margin+(margin+schmWidth)*i
        topY = y+self.subtitleSize*2+self.margin
        # delete button
        delLeftX = leftX+(schmWidth-self.favDelWidth)/2
        delTopY = topY+schmHeight*(self.minClass+1)+margin
        return (leftX, topY, delLeftX, delTopY)

    # check whether user deleted a favorite scheme
    def delFavSchm(self, newX, newY):
        for i in xrange(len(self.favSchm)):
            (leftX, topY, delLeftX, delTopY) = self.favSchmLoc(i)
            if (delLeftX<=newX and newX<=(delLeftX+self.favDelWidth) 
                and delTopY<=newY and newY<=(delTopY+self.favDelWidth)):
                self.favSchm.pop(i)
                return

    # check whether user select a new color design
    def newYourCol(self, newX, newY):
        # chose a color inside wheel?
        if (newX - self.cx)**2 + (newY - self.cy)**2 <= self.r**2:
            self.yourSchm[self.curYourCol] = self.getColorFromWheel(newX, newY)
        # chose to work on another color?
        else:
            select = self.defSchm.getWorkingColor(self.yourColLoc, newX, newY, 
                                                    self.classNum)
            if select != None: self.curYourCol = select

	# get the color on given location from color wheel
    def getColorFromWheel(self, newX, newY):
		a, c = self.cy-newY, ((newX-self.cx)**2 + (newY-self.cy)**2)**0.5
		if newX>self.cx:
			radian = math.asin(a/c)
		else:
			radian = math.pi-math.asin(a/c)
		deg = radian*360/(math.pi*2)
		(r, g, b) = (255, 0, 0)
		(r2, g2, b2) = self.colorWheel.adjacent_colors(r, g, b, deg=deg)[1]
		return (r2, g2, b2)

    # draw the separation lines between sections
    def drawSectionLines(self):
        lineCol = "gray"
        # outline box
        self.canvas.create_rectangle(self.cMargin, self.cMargin ,
                    self.width-self.cMargin, self.height-self.bMargin,
                    outline=lineCol, fill=self.backCol)
        # vertical line
        (x, topY, bottomY) = (self.zoneLoc[0][0], self.zoneLoc[0][1],
                                self.zoneLoc[2][1]+self.zoneLoc[2][3],)
        self.canvas.create_line(x, topY, x, bottomY, fill=lineCol)
        # horizonal lines
        for zone in xrange(6):
            (x, y, w, h) = self.zoneLoc[zone]
            self.canvas.create_line(x, y, x+w, y, fill=lineCol)
        # title box
        (x, y, w, h) = self.zoneLoc[0]
        self.canvas.create_rectangle(x, y, x+w, y+h,
                    outline=lineCol, fill=rgbString(68,68,68))

    # draw title
    def drawTitle(self):
        # title
        rX = self.zoneLoc[0][0] + self.zoneLoc[0][2]
        cY = self.zoneLoc[0][1] + self.zoneLoc[0][3]/2
        self.canvas.create_text(rX-self.titleSize*6, cY, 
                            text="Color", fill="#ffffbf",
                            anchor=E, font=("Arial", self.titleSize,"bold"))
        self.canvas.create_text(rX-self.titleSize*3.5, cY, 
                            text="Your", fill="#fc8d59",
                            anchor=E, font=("Arial", self.titleSize,"bold"))
        self.canvas.create_text(rX-self.titleSize, cY,
                            text="Data", fill="#91bfdb",
                            anchor=E, font=("Arial", self.titleSize,"bold"))
        self.canvas.create_text(rX-self.titleSize, cY+self.titleSize, 
                            text="your color scheme generator", 
                            fill=rgbString(151,151,151),
                            anchor=SE,font=("Arial",self.subtitleSize,"bold"))
        # citation
        self.canvas.create_text(rX, self.height, 
                            text="""Colors from www.ColorBrewer.org,
by Cynthia A. Brewer, Penn State.""", fill=rgbString(90,90,90),
                            anchor=SE, font=("Arial", 10))

    # draw subtitles for all sections
    def drawSectionTitles(self):
        subTitles = [None, "View:", "Favourites:", "Number of data classes:",
                    "Pick a color scheme:", "Design your color schemes:"]
        for zone in xrange(1,6):
            (x, y, w, h) = self.zoneLoc[zone]
            self.canvas.create_text(x+self.margin, y+self.subtitleSize, 
                                text=subTitles[zone], anchor=W, 
                                fill=self.subCol, font=self.subFont)
        # highlight current working zone
        (x, y, w, h) = self.zoneLoc[self.workZone]
        self.canvas.create_text(x+self.margin, y+self.subtitleSize, 
                                text=subTitles[self.workZone], anchor=W, 
                                fill="red", font=self.subFont)


    # draw zone 1: view
    def drawZone1(self):
        (x, y, w, h) = self.zoneLoc[1]
        # plot 
        self.data.plotData(self.viewType, x+self.margin*2+self.subtitleSize*2,
                                y+self.margin+self.subtitleSize*3, 
                                w*4/6, h*3/4, 
                                self.classNum, self.curSchm)
        # legend of current color scheme                
        legendY = y + h - self.defSchm.schmHeight*self.maxClass
        self.defSchm.drawSingleScheme(x+w*5/6, legendY-self.margin*2, 
                                self.curSchm, detail=True)

    # draw zone 2: favorites
    def drawZone2(self):
        for i in xrange(len(self.favSchm)):
            (leftX, topY, delLeftX, delTopY) = self.favSchmLoc(i)
            # compressed color scheme
            self.defSchm.drawSingleScheme(leftX, topY, self.favSchm[i],
                                            compress=True)
            # delete button
            self.canvas.create_rectangle(delLeftX, delTopY, 
                                delLeftX+self.favDelWidth, 
                                delTopY+self.favDelWidth,
                                outline=self.favDelCol)
            self.canvas.create_line(delLeftX, delTopY, 
                                delLeftX+self.favDelWidth,
                                delTopY+self.favDelWidth, 
                                fill= self.favDelCol)
            self.canvas.create_line(delLeftX+self.favDelWidth, delTopY,
                                delLeftX, delTopY+self.favDelWidth,
                                fill= self.favDelCol)

    # draw zone 4: default color schemes
    def drawZone4(self):
        (x, y) = self.defSchmLoc
        self.defSchm.drawSchemes(x, y, self.classNum, self.curDefSchm)

    # draw zone 5: design your color
    def drawZone5(self):
        (x, y, w, h) = self.zoneLoc[5]
        # color wheel
        cx, cy, r = self.cx, self.cy, self.r
        self.colorWheel.drawColorWheel()
        # color scheme
        (left, top) = self.yourColLoc
        self.defSchm.drawSingleScheme(left, top,
        						self.yourSchm, highlight=self.curYourCol)

    # redraw the canvas
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawSectionLines()
        self.drawTitle()
        self.drawSectionTitles()
        self.drawZone1()
        self.drawZone2()
        self.drawZone4()
        self.drawZone5()

ColorYourData(width=880, height=610).run()



