import colorsys
from tkinter import *

DEG30 = 30/360
def adjacent_colors( r, g, b, d=DEG30): # Assumption: r, g, b in [0, 255]
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

testcolor = (0,255,0)
a = adjacent_colors(*testcolor)
lNeigh = a[0]
rNeigh = a[1]


root = Tk()
canvas = Canvas(root, width=200, height=200)
canvas.pack()
canvas.create_rectangle(0,0,30,90, fill=rgbString(*lNeigh))
canvas.create_rectangle(30,0, 60, 90, fill=rgbString(*testcolor))
canvas.create_rectangle(60 ,0, 90, 90, fill=rgbString(*rNeigh))
root.mainloop()

