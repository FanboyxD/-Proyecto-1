import tkinter
from tkinter import *
import os
gameState = 0
def load_img(name):
    path=os.path.join("imgs",name)
    img = PhotoImage(file=path)
    return img

def winabout():
 #   main.withdraw()
    winabout = Toplevel()
    winabout.title("About")
    winabout.resizable(width=800,height=800)

    arch_about = open('about.txt','r')
    texto = Text(winabout )

    texto.insert(END, arch_about.read())
    texto.pack()
    Back_ini=Button(winabout, text=" Back ", font=21, command=winabout.destroy).place(x=160,y=500)

    
    def on_closing():
        arch_about.close()
        winabout.destroy()
    

    winabout.protocol("WM_DELETE_WINDOW", on_closing)

    winabout.mainloop()
def scores_win():
    scores_win = Toplevel()
    scores_win.title("Scores")
    scores_win.resizable(width=800,height=800)

    arch_scores = open('score.txt','r')
    texto = Text(scores_win )

    texto.insert(END, arch_scores.read())
    texto.pack()
    Back_ini=Button(scores_win, text=" Back ", font=21, command=scores_win.destroy).place(x=160,y=500)

    
    def close():
        arch_scores.close()
        scores_win.destroy()
    

    scores_win.protocol("WM_DELETE_WINDOW", close)

    scores_win.mainloop()

    
def wingame():
    
    wingame = Toplevel()
    wingame.title('Space Invaders')
    wingame.resizable(width=False,height=False)
    wingame.geometry("500x640")
    

    bicho1=load_img("bicho1.PNG")
    bicho2=load_img("bicho2.PNG")
    bloque3=load_img('bloque3.PNG')
    bloque2=load_img('bloque2.PNG')
    bloque1=load_img('bloque1.PNG')
    nave=load_img('nave.PNG')
    disparo=load_img('disparo.PNG')




    space = tkinter.Canvas(wingame,bg='black',width=500,height=640)
    space.place(x=0,y=0)
    space.create_line(0,529,500,529 ,fill='Yellow')
    space.create_rectangle(0,-20,500,32 ,fill='grey')
    Back_inicio=Button(wingame, text=" Back ", font=21, command=wingame.destroy).place(x=0,y=0)

main = Tk()
main.title("Space Invaders")
main.minsize(360,640)
main.resizable(width= False, height=False)

bgini=load_img("fondo_inicio.PNG")
tituloini=load_img("titulo.PNG")
bichotitulo=load_img("bichotit.PNG")

Canvas1 = tkinter.Canvas(main,width=360,height=640)
Canvas1.place(x=0,y=0)
Canvas1.create_image(180,320,image=bgini)
Canvas1.create_image(180,100,image=tituloini)
Canvas1.create_image(180,300,image=bichotitulo)
aboutbut=Button(Canvas1, text=" About ", font=21, command=winabout).place(x=290,y=600)
playbut=Button(Canvas1, text=" Play ", font=21, command=wingame).place(x=160,y=460)
scores=Button(Canvas1, text="Scores", font=21, command=scores_win).place(x=10,y=600)
def nombre():
    global name
    texto=data.get()
    if len (texto) >= 1:
        name = texto
    else:
        messagebox.showinfo(message="Name must have at least 1 character")

data = StringVar()
textField = Entry(Canvas1,textvariable=data).place(x=125,y=435)
savename=Button(Canvas1, text="Set Name",command=nombre).place(x=255,y=435)
