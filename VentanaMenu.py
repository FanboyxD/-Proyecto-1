#------------------------Librerias-----------------------------------#
from tkinter import *
import random
import tkinter.font
import tkinter.messagebox
import json


#-------------------------Ventana del menu(tkinter)------------------#
root = Tk()
root.wm_title("Dakar Death")
root.resizable(width=False, height=False)


def version():#funcion que muestra una ventana emergente con la version del programa
    tkinter.messagebox.showinfo("Space invaders",'''Instituto Tecnologico de Costa Rica
        Dakar Death alpha v0.1''')#Cuadro de texto con la informacion


def salir(): #Esta funcion pregunta al usuario si desea salir al menu o cerrar el juego
    pregunta = tkinter.messagebox.askyesno('Salir','Desea Salir del juego?' )#cuadro de dialogo que contiene la pregunta

    if pregunta == True:#si selecciona "si" cierra la ventana
        root.destroy()


def imprimirscore(): #Se crea una ventana que muestra los scores mas altos(work-in-progress) 
    with open('puntajes.json') as file:   #abre el doc de puntajes
                scores = json.load(file)
    disp.create_text(disp.winfo_width()/2, 320, 
                             text=str(scores["Nombres"][0]) +" "+ str(scores["Scores"][0]),fill="yellow", font=Fuente2) #crea un texto con el jugador con el punteje mas alto
    disp.create_text(disp.winfo_width()/2, 350,
                             text=str(scores["Nombres"][1]) +" "+ str(scores["Scores"][1]),fill="yellow", font=Fuente2) #segundo puntaje mas alto
    disp.create_text(disp.winfo_width()/2, 380,
                             text=str(scores["Nombres"][2]) +" "+ str(scores["Scores"][2]),fill="yellow", font=Fuente2)  #tercer puntaje mas alto
    disp.create_text(disp.winfo_width()/2, 410,
                             text=str(scores["Nombres"][3]) +" "+ str(scores["Scores"][3]),fill="yellow", font=Fuente2)  #cuarto mas alto
    disp.create_text(disp.winfo_width()/2, 440,
                             text=str(scores["Nombres"][4]) +" "+ str(scores["Scores"][4]),fill="yellow", font=Fuente2)

menubar = Menu(root)#Se crea la barra de menu
root.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", underline=0, menu=filemenu)#menu en la barra de menu
filemenu.add_command(label="High scores", command=imprimirscore)#sub menu de "file"
filemenu.add_command(label="Quit", command=salir)#sub menu de "file"
aboutmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", underline=0, menu=aboutmenu)#menu en la barra
aboutmenu.add_command(label="Acerca de ...", command=version)#sub menu de "about"



#-------------------------Canvas o contenedores----------------------#
disp = Canvas(root, width=800, height=800, bg="black")
disp.grid(row=0, column=0)

gameState = 0
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")#Fuentes utilizadas en el programa
Fuente2 = tkinter.font.Font(family="OCR-A II", size=14)
FuenteMenu = tkinter.font.Font(family="Fixedsys", size=50)


def startGame():
    global gameState  #se llama a las variables globales estado del juego y nombre
    global name
    if len (name) > 0: #si hay un nombre el juego puede comenzar
        savename.place_forget()#se quitan los botones y el cuadro de texto y se desabilita
        playbut.place_forget()
        textField.config(state=DISABLED)
        textField.place_forget()
        gameState = 1 #variable que al estar en 1 inicia el juego
    else:
        tkinter.messagebox.showinfo(message="Name must have at least 1 character") #si no hay un nombre establecido no se puede jugar


def drawBackground():
    pass

def menu():
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 - 50,
                     text="Dakar Death", fill="white", font=FuenteMenu)
    disp.create_text(disp.winfo_width()/2, disp.winfo_height()/2 + 20,
                     text="Create Nick Name", fill="white", font=Fuente2)
    global name
    texto=data.get()
    if len (texto) >= 0:
        name = texto
    else:
        messagebox.showinfo(message="Name must have at least 1 character")
        
def usuario(): #funcion que obtiene el usuario y lo garda en una variable
    global name
    global texto
    name=data.get()
        
data = StringVar() #se define que es de tipo str
textField = Entry(disp,textvariable=data) #entry para insertar el usuario y poscicion
textField.place(x=320,y=450)
savename=Button(disp, text="Set Nick Name",command=usuario) #boton para guardar el usuario y poscicion
savename.place(x=450,y=450)
playbut=Button(disp, text=" READY ", font=21, command=startGame)#boton para iniciar el juego
playbut.place(x=350,y=480)

def draw():
    disp.delete("all")
    if gameState:
        root.withdraw()


    else:
        drawBackground()
        menu()
    root.after(25, draw)
draw()

root.mainloop()