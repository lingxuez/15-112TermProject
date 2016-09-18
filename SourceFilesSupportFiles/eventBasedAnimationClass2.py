# eventBasedAnimationClass2.py
# from 15-112 lecture notes

from Tkinter import *

class EventBasedAnimationClass(object):
    def onMousePressed(self, event): pass
    def onKeyPressed(self, event): pass
    def onTimerFired(self): pass
    def redrawAll(self): pass
    def initAnimation(self): pass

    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height
        # in milliseconds (set to None to turn off timer)
        self.timerDelay = 250 

    def onMousePressedWrapper(self, event):
        self.onMousePressed(event)
        self.redrawAll()

    def onKeyPressedWrapper(self, event):
        self.onKeyPressed(event)
        self.redrawAll()

    def onTimerFiredWrapper(self):
        if (self.timerDelay == None):
            return # turns off timer
        self.onTimerFired()
        self.redrawAll()
        self.canvas.after(self.timerDelay, self.onTimerFiredWrapper)         

    def run(self):
        # create the root and the canvas
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.initAnimation()
        # set up events
        def f(event): self.onMousePressedWrapper(event)    
        self.root.bind("<Button-1>", f)
        self.root.bind("<Key>", lambda event: self.onKeyPressedWrapper(event))
        self.onTimerFiredWrapper()
        # and launch the app
        self.root.mainloop()
