from Tkinter import *
import Tkconstants, tkFileDialog

def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

def asksaveasfilename():
    filename = tkFileDialog.asksaveasfilename(parent=canvas, defaultextension=".txt",
                            initialdir="/Users/lingxue/Documents/Courses/2014Fall/15-112/termProject",
                            initialfile="myfile.txt")
    writeFile(filename, "myfile!")

root = Tk()
canvas = Canvas(root, width=100, height=100)
canvas.pack()
myButton = Button(canvas, text='asksaveasfilename', command=asksaveasfilename)

myButton.pack()
root.mainloop()
