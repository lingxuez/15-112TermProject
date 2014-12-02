import colorsys
from Tkinter import *

def _cubic(t, a, b):
    weight = t * t * (3 - 2*t)
    return a + weight * (b - a)

def ryb_to_rgb(r, y, b): # Assumption: r, y, b in [0, 1]
    # red
    x0, x1 = _cubic(b, 1.0, 0.163), _cubic(b, 1.0, 0.0)
    x2, x3 = _cubic(b, 1.0, 0.5), _cubic(b, 1.0, 0.2)
    y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
    red = _cubic(r, y0, y1)

    # green
    x0, x1 = _cubic(b, 1.0, 0.373), _cubic(b, 1.0, 0.66)
    x2, x3 = _cubic(b, 0., 0.), _cubic(b, 0.5, 0.094)
    y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
    green = _cubic(r, y0, y1)

    # blue
    x0, x1 = _cubic(b, 1.0, 0.6), _cubic(b, 0.0, 0.2)
    x2, x3 = _cubic(b, 0.0, 0.5), _cubic(b, 0.0, 0.0)
    y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
    blue = _cubic(r, y0, y1)

    return (red, green, blue)

# return left and right adjacency colors
def adjacent_colors( (r, g, b) , deg, sVal): # Assumption: r, g, b in [0, 255]
    d = deg/360.
    r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
    s = sVal*s
    h = [(h+d) % 1 for d in (-d, d)]           # Rotation by d
    adjacent = []
    for hi in h:
    	r, g, b = colorsys.hls_to_rgb(hi, l, s)
    	r, g, b = int(round(r*255)), int(round(g*255)), int(round(b*255)), 
    	adjacent += [(r,g,b)] # H'LS -> new RGB
    return adjacent

def rgbString( (red, green, blue) ):
        return "#%02x%02x%02x" % (red, green, blue)

def drawColorWheel(cx=100, cy=100, r=100):
    startColor = (255, 0, 0) # red
    degStep, startDeg, fullDeg = 36, 90, 360
    for s in [1, 0.66, 0.33, 0]:
        for i in range(int(fullDeg/degStep)+1):        
            currentColor = adjacent_colors(startColor, deg=i*degStep,sVal=s)[1]
            canvas.create_arc(cx-r*s, cy-r*s, cx+r*s, cy+r*s,
                        start = startDeg + i*degStep*360/fullDeg,
                        extent = degStep*360/fullDeg,
                        fill=rgbString(currentColor), 
                        style="arc", width=r/3, 
                        outline=rgbString(currentColor))

root = Tk()
canvas = Canvas(root, width=400, height=400)
canvas.pack()
#drawColorBand()
drawColorWheel(cx=200, cy=300, r=100)
root.mainloop()



