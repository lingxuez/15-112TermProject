from tkinter import *
import tkinter.ttk

from eventBasedAnimationClass import EventBasedAnimationClass

class CanvasWithWidget(EventBasedAnimationClass):
    def initAnimation(self):
        # combobox
        self.combo()
        self.root.bind("<<ComboboxSelected>>", 
                        lambda event: self.onComboboxSelection(event))
        self.boxValue = None
        # checkbutton
        self.checkbutton()
        self.checkStatus = None
        self.TimerDelay = None 

    def combo(self):
        self.box_value = StringVar()
        self.box = tkinter.ttk.Combobox(self.root, 
                textvariable=self.box_value, 
                justify="center", # alignment of displayed text
                state="readonly", # interaction setting
                width=3)
        self.box["values"] = tuple(range(3,11)) # the list of values to display
        #self.box.current(0) 
        self.box.place(x=self.width/2, y=self.height/3, anchor="center")

    def onComboboxSelection(self, event):
        self.boxValue = self.box_value.get()
        self.redrawAll()

    def checkbutton(self):
        self.buttonValue = StringVar()
        self.buttonValue.set("unsafe") # set initial state
        self.button = Checkbutton(self.root, text="safe mode",
                        variable = self.buttonValue,
                        command = self.newCheck,
                        onvalue="safe", offvalue="unsafe",
                        cursor = "arrow",
                        width=15)
        self.button.place(x=self.width/2, y=self.height*2/3, anchor="center")

    def newCheck(self):
        self.checkStatus = self.buttonValue.get()
        self.redrawAll()

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(self.width/2, self.height/3+30,
                        text="You just chose %s colors" % self.boxValue)
        self.canvas.create_text(self.width/2, self.height*2/3+30,
                        text="Color mode: %s" % self.checkStatus)

CanvasWithWidget().run()


