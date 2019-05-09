#------------------------Librerias-----------------------------------#
from tkinter import *
import random
import tkinter.font
import tkinter.messagebox
import json
from pygame_functions import *


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
    auxiliar=Tk()
    auxiliar.wm_title("Dakar Death")
    auxiliar.resizable(width=False, height=False)
    aux2 = Canvas(auxiliar, width=200, height=200, bg="black")
    aux2.grid(row=0, column=0)

    with open('puntajes.json') as file:   #abre el doc de puntajes
                scores = json.load(file)
    aux2.create_text(100, 40, 
                             text=str(scores["Nombres"][0]) +" "+ str(scores["Scores"][0]),fill="yellow", font=Fuente2) #crea un texto con el jugador con el punteje mas alto
    aux2.create_text(100, 70,
                             text=str(scores["Nombres"][1]) +" "+ str(scores["Scores"][1]),fill="yellow", font=Fuente2) #segundo puntaje mas alto
    aux2.create_text(100, 100,
                             text=str(scores["Nombres"][2]) +" "+ str(scores["Scores"][2]),fill="yellow", font=Fuente2)  #tercer puntaje mas alto
    aux2.create_text(100, 130,
                             text=str(scores["Nombres"][3]) +" "+ str(scores["Scores"][3]),fill="yellow", font=Fuente2)  #cuarto mas alto
    aux2.create_text(100, 160,
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
Fuente2 = tkinter.font.Font(family="OCR-A II", size=20)
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
        screenSize(600,600)
        setAutoUpdate(False)

        setBackgroundImage( [  ["images/Map 1.png", "images/Map 2.png"] ,
                               ["images/Map 3.png", "images/Map 4.png"]  ])

        testSprite  = makeSprite("images/links.gif",32)  # links.gif contains 32 separate frames of animation. Sizes are automatically calculated.

        moveSprite(testSprite,300,300,True)

        showSprite(testSprite)

        nextFrame = clock()
        frame=0
        while True:
            if clock() > nextFrame:                         # We only animate our character every 80ms.
                frame = (frame+1)%8                         # There are 8 frames of animation in each direction
                nextFrame += 80                             # so the modulus 8 allows it to loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            if keyPressed("right"):
                changeSpriteImage(testSprite, 0*8+frame)    # 0*8 because right animations are the 0th set in the sprite sheet
                scrollBackground(-5,0)                      # The player is moving right, so we scroll the background left

            elif keyPressed("down"):
                changeSpriteImage(testSprite, 1*8+frame)    # down facing animations are the 1st set
                scrollBackground(0, -5)

            elif keyPressed("left"):
                changeSpriteImage(testSprite, 2*8+frame)    # and so on
                scrollBackground(5,0)

            elif keyPressed("up"):
                changeSpriteImage(testSprite,3*8+frame)
                scrollBackground(0,5)

            else:
                changeSpriteImage(testSprite, 1 * 8 + 5)  # the static facing front look

            updateDisplay()
            tick(120)
        endWait()

    else:
        drawBackground()
        menu()
    root.after(25, draw)
draw()

root.mainloop()