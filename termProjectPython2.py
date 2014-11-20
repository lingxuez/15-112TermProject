# termProjectPython2.py
# name: Lingxue Zhu
# andrewId: lzhu1
# section: L

import copy
import colorsys
import os

from Tkinter import *
import ttk
from eventBasedAnimationClass2 import EventBasedAnimationClass

# turn rgb into hex strings
def rgbString( red, green, blue ):
        return "#%02x%02x%02x" % (red, green, blue)

# a class to read-in and draw default color schemes
class DefaultColorSchemes(object):
    # constructor
    def __init__(self, canvas, filePath):
        self.colorSchemes = self.getColorSchemes(filePath)
        self.canvas = canvas
        self.schmWidth, self.schmHeight, self.margin = 20, 20, 15

    @staticmethod
    # from lecture notes
    def readFile(filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()

    # read in color scheme files, return a 3d list
    def getColorSchemes(self, path):
        s = self.readFile(path)
        sLine = s.splitlines()
        maxNum = 12
        colorSchemes = [0] * maxNum
        for i in xrange(maxNum):
            colorSchemes[i] = []
        # save line by line; ignore first line, which is column names
        for line in sLine[1:]: 
            sepLine = line.split(",")
            classNum = sepLine[1]
            (r,g,b) = tuple(int(a) for a in sepLine[4:])
            # if a new scheme started
            if len(classNum)>0 and int(classNum)<maxNum:
                colorSchemes[int(classNum)] += [[(r,g,b)]]
                currentClass = int(classNum)
            else:
                colorSchemes[currentClass][-1] += [(r,g,b)]
        return colorSchemes

    # draw one scheme at given location
    def drawSingleScheme(self, x, y, scheme, detail):
        margin=5
        # colors
        for (r,g,b) in scheme:
            self.canvas.create_rectangle( x, y, 
                            x+self.schmWidth, y+self.schmHeight, 
                            fill=rgbString(r, g, b), 
                            outline=rgbString(128, 128, 128), width=2)
            # information
            if detail:
                self.canvas.create_text( x+self.schmWidth+margin, 
                                y+self.schmHeight/2, 
                                anchor=W, text=rgbString(r,g,b), 
                                font=("Arial", 10), fill=rgbString(90,90,90))
            y += self.schmHeight  

    # draw color schemes at given location on canvas
    def drawSchemes(self, x, y, classNum, curSchm):
        schemes = self.colorSchemes[classNum]
        lwd, hCol = 7, rgbString(178, 178, 178)
        # highlight current scheme
        left = x + (self.schmWidth+self.margin)*curSchm
        self.canvas.create_rectangle( left-lwd/2, y-lwd/2, 
                    left+self.schmWidth+lwd/2, 
                    y+self.schmHeight*classNum+lwd/2,
                    outline=hCol, width=lwd)
        # draw all schemes
        for scheme in schemes:
            self.drawSingleScheme(x, y, scheme, detail=False)
            x += self.schmWidth+self.margin

    # get which color scheme did (newX, newY) falled into
    def getCurrentScheme(self, x, y, newX, newY, classNum):
        schemes = self.colorSchemes[classNum]
        for i in xrange(len(schemes)):
            left = x + (self.schmWidth+self.margin)*i
            right = left+self.schmWidth
            top, bottom = y, y+self.schmHeight*classNum
            if (left<=newX and newX<=right and top<=newY and newY<=bottom):
                return i
        return None

# class to generate and draw color wheel
class ColorWheel(object):
    # constructor
    def __init__(self, canvas, cx, cy, r, startColor=(255,0,0)):
        self.cx, self.cy, self.r = cx, cy, r
        self.startColor = startColor
        self.canvas = canvas

    # return left and right adjacency colors; found online
    def adjacent_colors(self, r, g, b, deg=30): 
        d = deg/360.
        r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
        h, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
        h = [(h+d) % 1 for d in (-d, d)]           # Rotation by d
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
        degStep, startDeg, fullDeg = 1, 90, 360
        # color wheel
        for i in xrange(int(fullDeg/degStep)+1):
            currentColor = self.adjacent_colors(*startColor, deg=i*degStep)[1]
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                            start = startDeg + i*360/fullDeg,
                            extent = degStep*360/fullDeg,
                            fill = rgbString(*currentColor), 
                            outline = rgbString(*currentColor))

# the main app
class ColorYourData(EventBasedAnimationClass):
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
        self.initZone()
        self.initWidgets()
        self.initDefaultSchemes()
        self.viewType = "barPlot"
        self.timerDelay = None

    # initialize toplelf (x,y), width, height of all zones
    def initZone(self):
        self.zoneLoc = []
        # zone 0: title
        (x, y) = (self.cMargin+self.lZoneWidth, self.cMargin)
        (w, h) = (self.width-2*self.cMargin-self.lZoneWidth, 
                    self.titleSize*2+self.subtitleSize)
        self.zoneLoc += [(x,y,w,h)]
        # zone 1: view plots
        (x, y) = (self.zoneLoc[0][0], self.zoneLoc[0][1]+self.zoneLoc[0][3])
        (w, h) = (self.zoneLoc[0][2], self.height*2/3)
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
        
    # initialize all buttons, combo boxes
    def initWidgets(self):
        self.radiobutton()
        self.checkbutton()
        self.combobox()
        self.root.bind("<<ComboboxSelected>>", 
                        lambda event: self.onComboboxSelection(event))

    # initialize default color schemes
    def initDefaultSchemes(self):
        self.classNum = 3 
        self.isCorBlind = False
        path = "ColorBrewerDivSchemes.csv"
        self.defSchm = DefaultColorSchemes(self.canvas, path)
        self.curDefSchm = 0
        # location
        (x, y, w, h) = self.zoneLoc[4]
        self.defSchmLoc = (x+self.margin*2, y+self.subtitleSize*2)
        
    # build radio buttons for zone 1
    def radiobutton(self):
        # a frame to put the buttons
        self.radioFrame = Frame(self.root, bg = self.backCol)
        (x, y, w, h) = self.zoneLoc[1]
        xMargin, yMargin = 50, self.subtitleSize
        self.radioFrame.place(x=x+xMargin, y=y+yMargin, anchor=W)
        # put buttons
        viewTypes = [("Bar plot", "barPlot"), ("Pie chart", "pieChart"),
                    ("Trend lines", "trendLine")]
        self.radioValue = StringVar()
        self.radioValue.set("barPlot")       
        for i in xrange(len(viewTypes)):
            (text, viewType) = viewTypes[i]
            self.radio = Radiobutton(self.radioFrame,  text=text,
                        variable = self.radioValue, value = viewType, 
                        command = self.newRadiobutton, width=15, 
                        font=("Arial",self.subtitleSize), 
                        borderwidth=1)
            self.radio.grid(row=0, column=i)

    # react to radio buttions
    def newRadiobutton(self):
        self.viewType = self.radioValue.get()
        self.redrawAll()

    # build check button for zone 4
    def checkbutton(self):
        self.checkValue = IntVar()
        self.checkValue.set("unsafe") # set initial state
        self.check = Checkbutton(self.root, text="colorblind safe",
                        variable = self.checkValue, 
                        command = self.newCheckbutton, 
                        font=("Arial", self.textSize))
        (x, y, w, h) = self.zoneLoc[4]
        self.check.place(x=x+self.margin, y=y+h, anchor=SW)

    # react to check button
    def newCheckbutton(self):
        self.isCorBlind = bool(self.checkValue.get())
        self.redrawAll()

    # build a combo box for zone 3
    def combobox(self):
        self.boxValue = StringVar()
        self.box = ttk.Combobox(self.root, 
                textvariable=self.boxValue, 
                justify="center", # alignment of displayed text
                state="readonly", # interaction setting
                width=3)
        self.box["values"] = tuple(range(3,11)) # the list of values to display
        self.box.current(0) 
        (x, y, w, h) = self.zoneLoc[3]
        xMargin, yMargin = 200, self.subtitleSize
        self.box.place(x=x+xMargin, y=y+yMargin, anchor="center")

    # react to combobox selection
    def onComboboxSelection(self, event):
        self.classNum = int(self.boxValue.get())
        self.redrawAll()

    # react to mouse pressed
    def onMousePressed(self, event):
        # selected a new default scheme?
        (x, y) = self.defSchmLoc
        newSchm = self.defSchm.getCurrentScheme(x, y, event.x, event.y,
                                                self.classNum)
        if newSchm != None:
            self.curDefSchm = newSchm

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
                            anchor=SE, font=("Arial", self.subtitleSize,"bold"))
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

    # draw zone 1: view
    def drawZone1(self):
        # plot
        # legend of current color scheme
        (x, y, w, h) = self.zoneLoc[1]
        scheme = self.defSchm.colorSchemes[self.classNum][self.curDefSchm]
        y = y + h - self.defSchm.schmHeight*self.classNum
        self.defSchm.drawSingleScheme(x+w*5/6, y-self.margin*2, scheme,
                                detail=True)

    # draw zone 4: default color schemes
    def drawZone4(self):
        (x, y) = self.defSchmLoc
        self.defSchm.drawSchemes(x, y, self.classNum, self.curDefSchm)

    # draw zone 5: design your color
    def drawZone5(self):
        (x, y, w, h) = self.zoneLoc[5]
        self.colorWheel = ColorWheel(canvas=self.canvas, 
                                    cx=x+w/3, cy=y+h/3, r=h/4)
        self.colorWheel.drawColorWheel()

    # redraw the canvas
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawSectionLines()
        self.drawTitle()
        self.drawSectionTitles()
        self.drawZone1()
        self.drawZone4()
        #self.drawZone5()

ColorYourData(width=900, height=650).run()



