# termProject.py
# name: Lingxue Zhu
# andrewId: lzhu1
# section: L

import copy
from tkinter import *
import tkinter.ttk
from eventBasedAnimationClass import EventBasedAnimationClass

# class of the main app
class ColorYourData(EventBasedAnimationClass):

    @staticmethod
    def rgbString(red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    # constructor
    def __init__(self, width=900, height=650):
        super(ColorYourData, self).__init__(width, height)
        self.timerDelay = 1000

    # init
    def initAnimation(self):
        # decide the location of each zone
        self.titleSize, self.subtitleSize, self.textSize =30, 14, 12 
        self.subFont = ("Arial",self.subtitleSize,"bold")
        self.subCol = self.rgbString(90,90,90)
        self.lZoneWidth = self.width/3
        self.bMargin, self.cMargin, self.margin = 30, 5, 5
        self.initZone()
        # widgets
        self.initWidgets()
        # other status
        self.classNum = 3
        self.isCorBlind = False
        self.viewType = "barPlot"

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
        (w, h) = (self.lZoneWidth, self.height/3)
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

    # build radio buttons for zone 1
    def radiobutton(self):
        # a frame to put the buttons
        self.radioFrame = Frame(self.root)
        (x, y, w, h) = self.zoneLoc[1]
        xMargin, yMargin = 50, self.subtitleSize
        self.radioFrame.place(x=x+xMargin, y=y+yMargin, anchor=W)
        # put buttons
        viewTypes = [("Bar plot", "barPlot"), ("Pie chart", "pieChart"),
                    ("Trend lines", "trendLine")]
        self.radioValue = StringVar()
        self.radioValue.set("barPlot")       
        for i in range(len(viewTypes)):
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
        self.box = tkinter.ttk.Combobox(self.root, 
                textvariable=self.boxValue, 
                justify="center", # alignment of displayed text
                state="readonly", # interaction setting
                width=3)
        self.box["values"] = tuple(range(3,11)) # the list of values to display
        self.box.current(0) 
        (x, y, w, h) = self.zoneLoc[3]
        xMargin, yMargin = 200, self.subtitleSize
        self.box.place(x=x+xMargin, y=y+yMargin, anchor="center")

    def onComboboxSelection(self, event):
        self.classNum = int(self.boxValue.get())
        self.redrawAll()

    # draw the separation lines between sections
    def drawSectionLines(self):
        lineCol = "gray"
        # outline box
        self.canvas.create_rectangle(self.cMargin, self.cMargin ,
                    self.width-self.cMargin, self.height-self.bMargin,
                    outline=lineCol)
        # vertical line
        (x, topY, bottomY) = (self.zoneLoc[0][0], self.zoneLoc[0][1],
                                self.zoneLoc[2][1]+self.zoneLoc[2][3],)
        self.canvas.create_line(x, topY, x, bottomY, fill=lineCol)
        # horizonal lines
        for zone in range(6):
            (x, y, w, h) = self.zoneLoc[zone]
            self.canvas.create_line(x, y, x+w, y, fill=lineCol)
        # title box
        (x, y, w, h) = self.zoneLoc[0]
        self.canvas.create_rectangle(x, y, x+w, y+h,
                    outline=lineCol, fill=self.rgbString(68,68,68))

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
                            fill=self.rgbString(151,151,151),
                            anchor=SE, font=("Arial", self.subtitleSize,"bold"))
        # citation
        self.canvas.create_text(rX, self.height, 
                            text="""Colors from www.ColorBrewer.org,
by Cynthia A. Brewer, Penn State.""", fill=self.rgbString(90,90,90),
                            anchor=SE, font=("Arial", 10))

    # draw subtitles for all sections
    def drawSectionTitles(self):
        subTitles = [None, "View:", "Favourites:", "Number of data classes:",
                    "Pick a color scheme:", "Design your color schemes:"]
        for zone in range(1,6):
            (x, y, w, h) = self.zoneLoc[zone]
            self.canvas.create_text(x+self.margin, y+self.subtitleSize, 
                                text=subTitles[zone], anchor=W, 
                                fill=self.subCol, font=self.subFont)

    # draw zone 1: view
    def drawZone1(self):
        (x, y, w, h) = self.zoneLoc[1]
        self.canvas.create_text(x+w/2, y+h/2, 
                        text="Display %s (%d colors)" % (self.viewType, self.classNum))

    # draw zone 4: default color schemes
    def drawZone4(self):
        if self.isCorBlind:
            text = "only show colorblind safe colors"
        else:
            text = "display all colors"
        (x, y, w, h) = self.zoneLoc[4]
        self.canvas.create_text(x+w/2, y+h/2, text=text)

    # redraw the canvas
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawSectionLines()
        self.drawTitle()
        self.drawSectionTitles()
        self.drawZone1()
        self.drawZone4()

ColorYourData().run()



