from Tkinter import *
import Tkconstants, tkFileDialog

def asksaveasfile():
    return tkFileDialog.asksaveasfile(mode='w', parent=canvas, defaultextension=".txt",
                            initialdir="/Users/lingxue/Documents/Courses/2014Fall/15-112/termProject",
                            initialfile="myfile.txt")

root = Tk()
canvas = Canvas(root, width=100, height=100)
canvas.pack()
myButton = Button(canvas, text='asksaveasfile', command=asksaveasfile)
myButton.pack()
root.mainloop()
