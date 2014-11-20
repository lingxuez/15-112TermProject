import colorsys
from tkinter import *

# return left and right adjacency colors
def adjacent_colors( r, g, b, deg=30): # Assumption: r, g, b in [0, 255]
    d = deg/360
    r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
    h = [(h+d) % 1 for d in (-d, d)]           # Rotation by d
    adjacent = []
    for hi in h:
    	r, g, b = colorsys.hls_to_rgb(hi, l, s)
    	r, g, b = int(round(r*255)), int(round(g*255)), int(round(b*255)), 
    	adjacent += [(r,g,b)] # H'LS -> new RGB
    return adjacent

def rgbString( red, green, blue ):
        return "#%02x%02x%02x" % (red, green, blue)

def drawColorBand(x1=0, y1=0, x2=360, y2=200):    
    startColor = (255, 0, 0) # red
    degStep, fullDeg = 1, 360
    for i in range(int(fullDeg/degStep)+1):
        currentColor = adjacent_colors(*startColor, deg=i*degStep)[1]
        canvas.create_rectangle(x1+i*(x2-x1)/fullDeg, y1, 
                        x1+(i+1)*(x2-x1)/fullDeg, y2, 
                        fill=rgbString(*currentColor), 
                        outline=rgbString(*currentColor))

def drawColorWheel(cx=100, cy=100, r=100):
    startColor = (255, 0, 0) # red
    degStep, startDeg, fullDeg = 1, 90, 360
    for i in range(int(fullDeg/degStep)+1):
        currentColor = adjacent_colors(*startColor, deg=i*degStep)[1]
        canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                        start = startDeg + i*360/fullDeg,
                        extent = degStep*360/fullDeg,
                        fill=rgbString(*currentColor), 
                        outline=rgbString(*currentColor))

root = Tk()
canvas = Canvas(root, width=400, height=400)
canvas.pack()
drawColorBand()
drawColorWheel(cx=200, cy=300, r=100)
root.mainloop()



