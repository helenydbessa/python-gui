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
        global canvas_width
        global canvas_height
        global width_scale
        global height_scale
        # determine the ratio of old width/height to new width/height
        width_scale = float(event.width)/self.width
        #print("wscale = ", width_scale)
        height_scale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, width_scale, height_scale)
        canvas_width = round(canvas_width * width_scale)
        canvas_height = round(canvas_height * height_scale)
        #self.escala()
        # img = PhotoImage(width=(round(canvas_width*width_scale)), height=(round(canvas_height*height_scale)))
        # canvas.create_image((canvas_width//2), (canvas_height // 2), image=img, state="normal", tag="all")



width_scale = 1.0
height_scale = 1.0
canvas_width = round(1000 * width_scale)
canvas_height = round(650 * height_scale)
array_posicoes = np.array([])
array_posicoes_escalado = np.array([])
botao = 0

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
    global botao
    global array_posicoes
    print("posicao = ", botao)
    x = event.x
    y = event.y
    print(botao)
    #my_label['text'] = f'x={x}y={y}'
    if(len(array_posicoes) % 5 < 3):
        array_posicoes = np.append(array_posicoes, [botao, x, y])
    else:
        array_posicoes = np.append(array_posicoes, [x, y])
    if botao == 1:
        circulo()
    elif botao == 2:
        reta()
    # x2 = {event.x} + int(x_incr)
    # y2 = {event.y} + int(y_incr)
    # for i in range(x1, x2):
    #     for j in range(y1, y2):
    #         img.put("#FF5733", (i, j))

def reta():
    global array_posicoes
    if(len(array_posicoes) % 5 == 0):
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
    print(x1, " ", y1, " ", x2, " ", y2)
    dx = x2 - x1
    print(dx)
    dy = y2 - y1
    print(dy)
    if abs(dx) > abs(dy):
        passos =abs(dx)
    else:
        passos = abs(dy)
    print(passos)
    x_incr = dx/passos
    y_incr = dy/passos
    x = x1
    y = y1
    for p in range(round(passos)):
        x += x_incr
        y += y_incr
        img.put("#FF5733", (round(x), round(y)))

def circulo():
    print("circulo")
    global array_posicoes
    if(len(array_posicoes) % 5 == 0):
        x1 = array_posicoes[-4]
        y1 = array_posicoes[-3]
        x2 = array_posicoes[-2]
        y2 = array_posicoes[-1]
        #print(array_posicoes)
        bresenham(x1, y1, x2, y2)

def bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    raio = sqrt(dx ** 2 + dy ** 2)
    print(raio)
    x = 0
    y = raio
    p = 3 - 2*raio
    #print(p)
    plot_circle_points(x1, y1, x, y)
    while x < y:
        if p < 0:
            p = p + 4*x + 6
        else:
            p = p + 4*(x-y) + 10
            y = y - 1
        x = x + 1
        plot_circle_points(x1, y1, x, y)
    #canvas.create_oval(x0, y0, x1, y1)

def plot_circle_points(xc, yc, x, y):
    # print(xc)
    # print(yc)
    # print(x)
    # print("y = ", y)

    img.put("#FF5733", (round(xc+x), round(yc+y)))
    if xc-x > 0:
        img.put("#FF5733", (round(xc-x), round(yc+y)))
    if yc-y > 0:
        img.put("#FF5733", (round(xc+x), round(yc-y)))
    if xc-x > 0 and yc-y > 0:
        img.put("#FF5733", (round(xc-x), round(yc-y)))
    img.put("#FF5733", (round(xc+y), round(yc+x)))
    if xc-y > 0:
        img.put("#FF5733", (round(xc-y), round(yc+x)))
    if yc-x > 0:
        img.put("#FF5733", (round(xc+y), round(yc-x)))
    if xc-y > 0 and yc-x > 0:
        img.put("#FF5733", (round(xc-y), round(yc-x)))

def escala():
    global array_posicoes
    global array_posicoes_escalado
    maior_x = 0
    maior_y = 0
    # print("escala")
    eh_int = False
    if scale_width.get().isdigit() and scale_height.get().isdigit():
        eh_int = True
    posicoes = len(array_posicoes)
    print("posicoes = ", posicoes)
    if(eh_int == True):
        for i in range(posicoes):
            print(array_posicoes)
            # print("i = ", i)
            # print(array_posicoes_escalado)
            if(i % 5 == 1 or i % 5 == 2):
                if array_posicoes[i] > array_posicoes[i+2]:
                    print("x1 > x2 ou y1 > y2")
                    d = array_posicoes[i] - array_posicoes[i+2]
                    if i % 5 == 1:
                        menor_x = array_posicoes[i+2]
                    else:
                        menor_y = array_posicoes[i+2]
                    # subtrai = dx * int(scale_width.get())
                    # temp = array_posicoes[i] - subtrai
                    #print(temp)
                    # print(type(temp))
                    array_posicoes_escalado = np.append(array_posicoes_escalado, array_posicoes[i])
                else:
                    if(i % 5 == 1):
                        menor_x = array_posicoes[i]
                    else:
                        menor_y = array_posicoes[i]
                    array_posicoes_escalado = np.append(array_posicoes_escalado, array_posicoes[i])
                # print(maior_x)
                # print(type(scale_width.get()))
            elif(i % 5 == 3 or i % 5 == 4):
                d = abs(array_posicoes[i] - array_posicoes[i-2])
                if i % 5 == 3:
                    if menor_x == array_posicoes[i]:
                        print("x1 > x2")
                        subtrai = d * int(scale_width.get())
                        temp = array_posicoes[i] - subtrai
                        #temp = maior_x * int(scale_width.get())
                        array_posicoes_escalado = np.append(array_posicoes_escalado, temp)
                    else:
                        print("x1 < x2")
                        soma = d * int(scale_width.get())
                        temp = array_posicoes[i] + soma
                        array_posicoes_escalado = np.append(array_posicoes_escalado, temp)
                else:
                    if menor_y == array_posicoes[i]:
                        print("y1 > y2")
                        subtrai = d * int(scale_width.get())
                        temp = array_posicoes[i] - subtrai
                        #temp = maior_x * int(scale_width.get())
                        array_posicoes_escalado = np.append(array_posicoes_escalado, temp)
                    else:
                        print("y1 < y2")
                        soma = d * int(scale_width.get())
                        temp = array_posicoes[i] + soma
                        array_posicoes_escalado = np.append(array_posicoes_escalado, temp)
            # elif(i % 5 == 4):
            #     print("elif")
            #     temp = array_posicoes[i] * int(scale_height.get())
            #     array_posicoes_escalado = np.append(array_posicoes_escalado, temp)
            else:
                array_posicoes_escalado = np.append(array_posicoes_escalado, array_posicoes[i])
        posicoes = len(array_posicoes_escalado)
        # print("posicoes = ", posicoes)
        # print(array_posicoes)
        # print(array_posicoes_escalado)
        for j in range(posicoes):
            if(j % 5 == 0):
                if array_posicoes_escalado[j] == 2:
                    DDA(array_posicoes_escalado[j+1], array_posicoes_escalado[j+2], array_posicoes_escalado[j+3], array_posicoes_escalado[j+4])
                else:
                    bresenham(array_posicoes_escalado[j+1], array_posicoes_escalado[j+2], array_posicoes_escalado[j+3], array_posicoes_escalado[j+4])

def fazerCirculo():
    global botao
    botao = 1

def fazerReta():
    global botao
    botao = 2

circle = Button(master, text="círculo", command=fazerCirculo) #1
circle.pack(side="top")
straight_line = Button(master, text="reta", command=fazerReta) #2
straight_line.pack(side="bottom")
translation = Button(master, text="translação") #3
translation.pack(side="left")
rotation = Button(master, text="rotação") #4
rotation.pack(side="left")
reflection_X = Button(master, text="refletir X") #5
reflection_X.pack(side="left")
reflection_Y = Button(master, text="refletir Y") #6
reflection_Y.pack(side="left")
reflection_XY = Button(master, text="refletir XY") #7
reflection_XY.pack(side="left")
cut = Button(master, text="recorte") #8
cut.pack(side="right")

Label(master, text="Escala largura").pack(side="bottom")
scale_width = Entry(master)
scale_width.pack(side="bottom")
scale_width.insert(END, "1")
Label(master, text="Escala altura").pack(side="top")
scale_height = Entry(master)
scale_height.pack(side="bottom")
scale_height.insert(END, "1")
send_scale = Button(master, text="mandar escala", command=escala) #1
send_scale.pack(side="bottom")

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
