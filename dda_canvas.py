# pip install pillow ou pip install Image
# pip install numpy
from tkinter import *
from PIL import Image
import numpy as np
from math import *

class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        global array_posicoes
        # determine the ratio of old width/height to new width/height
        width_scale = float(event.width)/self.width
        print("wscale = ", width_scale)
        height_scale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, width_scale, height_scale)
        canvas_width = round(canvas_width * width_scale)
        canvas_height = round(canvas_height * height_scale)

width_scale = 1.0
height_scale = 1.0
canvas_width = round(1000 * width_scale)
canvas_height = round(700 * height_scale)
array_posicoes = np.array([])

scale_matrix = np.array([[width_scale, 0],
                [0, height_scale]])

master = Tk()
master.title("Painting using Ovals")
frame = Frame(master)
frame.pack(fill=BOTH, expand=YES)
canvas = ResizingCanvas(frame,
                        width=canvas_width,
                        height=canvas_height,
                        bg="#222222",
                        highlightthickness=0)
# canvas = Canvas(master,
#                 width=canvas_width,
#                 height=canvas_height, bg="#222222")
canvas.pack(expand=YES, fill=BOTH)


img = PhotoImage(width=(round(canvas_width*width_scale)), height=(round(canvas_height*height_scale)))

canvas.create_image((canvas_width//2), (canvas_height // 2), image=img, state="normal", tag="all")
# canvas.addtag('all', img)

# image.putpixel( (x, y), (0, 0, 0, 255) )


def display_coordinates(event):
    my_label['text'] = f'x={event.x}y={event.y}'

def posicao(event):
    global array_posicoes
    x = event.x
    y = event.y
    #my_label['text'] = f'x={x}y={y}'
    array_posicoes = np.append(array_posicoes, [x, y])
    reta()
    # x2 = {event.x} + int(x_incr)
    # y2 = {event.y} + int(y_incr)
    # for i in range(x1, x2):
    #     for j in range(y1, y2):
    #         img.put("#FF5733", (i, j))

def reta():
    global array_posicoes
    if(len(array_posicoes) % 4 == 0):
        x1 = array_posicoes[-4]
        print("x1 = ", x1)
        y1 = array_posicoes[-3]
        x2 = array_posicoes[-2]
        y2 = array_posicoes[-1]
        print(array_posicoes)
        DDA(x1, y1, x2, y2)
        # for i in range(x1, x2):
        #     for j in range(y1, y2):
        #         img.put("#FF5733", (i, j))
                #img.putpixel((i, j), (x1, y1, x2, y2))

def DDA(x1, y1, x2, y2):
    dx = x2 - x1
    print(dx)
    dy = y2 - y1
    print(dx)
    if abs(dx) > abs(dy):
        passos =abs(dx)
    else:
        passos = abs(dy)
    print(passos)
    x_incr = dx/passos
    y_incr = dy/passos
    x = x1
    y =y1
    for p in range(round(passos)):
        x += x_incr
        y += y_incr
        img.put("#FF5733", (round(x), round(y)))

def circulo():
    global array_posicoes
    if(len(array_posicoes) % 4 == 0):
        x1 = array_posicoes[-4]
        y1 = array_posicoes[-3]
        x2 = array_posicoes[-2]
        y2 = array_posicoes[-1]
        print(array_posicoes)
        bresenham(x1, y1, x2, y2)

def bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    raio = sqrt(dx ** 2 + dy ** 2)
    print(raio)
    x = 0
    y = raio
    p = 3 - 2*raio
    print(p)
    plot_circle_points(x1, y1, x, y)
    while x < y:
        if p < 0:
            p = p + 4*x + 6
        else:
            p = p +4*(x-y) + 10
            y = y - 1
        x += 1
        plot_circle_points(x1, y1, x, y)
    #canvas.create_oval(x0, y0, x1, y1)

def plot_circle_points(xc, yc, x, y):
    print(xc)
    print(yc)
    print(x)
    print(y)

    img.put("#FF5733", (round(xc+x), round(yc+y)))
    img.put("#FF5733", (round(xc-x), round(yc+y)))
    img.put("#FF5733", (round(xc+x), round(yc-y)))
    img.put("#FF5733", (round(xc-x), round(yc-y)))
    img.put("#FF5733", (round(xc+y), round(yc+x)))
    img.put("#FF5733", (round(xc-y), round(yc+x)))
    img.put("#FF5733", (round(xc+y), round(yc-x)))
    img.put("#FF5733", (round(xc-y), round(yc-x)))



canvas.addtag_all("all")
canvas.bind('<Button-1>', posicao)
#canvas.grid(row=0, column=0)
# my_label=Label(bd=4, relief="solid", font="Times 22 bold",
#                  bg="white", fg="black")
# my_label.grid(row=1, column=0)


#
# for x in range(200):
#   x = x + int(x_incr)
#   y = y + int(y_incr)
#  img.put("#FF5733", (x, y))
# image.putpixel((x, y), (x1, y1, x2, y2))

canvas.mainloop()
