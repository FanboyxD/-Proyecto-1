# Proyeco-TKINTER-Dakar-death
Instituto Tecnologico de Costa Rica

El codigo mostrado a continuación forma parte del curso CE1102-Taller de Programación.
El proyecto consiste en crear el juego "Dakar deaht" por medio de python, la interfaz grafica tkinter/pygame y sockets, y la creacion de un control por medio de arduino y la libreria pyserial

# Pre-requisitos
-Las herramientas que usamos en este proyecto fueron:
-Python 3.7.2 como lenguaje de programación
-tkinter y pygame como interfaz grafica de python
-sockets para la conexion entre computadoras y su respectiva ip
-Un microcontrolador arduino
-Componentes para la creacion del control(joystick, 5 botones, jumpers para las conecciones, 6 resistencias y un LED)

# Instalación 
Se debe descargar el archivo .zip y descomprimirlo de la siguiente manera:
Se debe darle click derecho y por medio de Winrar seleccionar la opcion "Extraer a + nombre del Archivo" o "Extrac to + nombre del archivo" , con ello se creara una carpeta con el nombre del archivo que contendra todos los archivos necesarios para el funcionamiento del programa. 
Nota:*No se debe alterar ningun archivo de la carpeta para no afectar el funcionamiento del juego*

# Ejecución del programa
Previamente se debe haber instalado python 3.7.2 y de haber cambiado la ipv4 del archivo "network"(debe editarlo con un programa de codigo y cambiar la variable "self.host") con la respectiva del pc al que se desea conectar(puede buscar la ip en cmd --> ipconfig (la que aparece denominada como ipv4)), luego debe ejecutar el archivo denominado "server".
Tambien se debe cofigurar el puerto de conexion del arduino en la linea 20 del archivo "game" (Puede ver el puerto del arduino en arduino IDE --> Herramientas --> Puerto), se debe sustituir COM + numero de puerto ejemplo: COM7)
En la carpeta "Joystick" se encuentra un programa de arduino, el cual debera ser cargado en el microcontrolador para el funcionamiento del control(se debe haber instalado anteriormente arduino IDE 1.8.9 y el control preparado)
Una vez que en el server aparezca "wating for coneccion" de debe ejecutar el archivo "Dakar deaht"

# Iniciar el juego
Se debe introducir un usuario el el cuadro de texto que aparece en centro, luego debe dar click en "set nick name", el usuario debera tener como minimo 1 caracter de lo contrario no podra iniciar el juego. 
Una vez definido el usuario debe dar click al boton den play y comenzara el juego. 
Para reiniciar el juego cuando solo necesita presionar la tecla "esc" la cual lo devolvera a la ventana del menu, esta a su vez posee pestañas para ver el high score y cerrar la ventana

En caso de querer pausar el juego debe presionar el boton que se haya asignado(boton 3 por defecto) y para reanudarlo el boton asignado para reanudar(boton 4 por defecto)
En caso de guardar la partida debe presionar el boton asignado(boton 5 por defecto), para cargar la partida se debe presionar el boton asignado(boton 6 por defecto)
El score se asigna en base a las banderas recogidas, los enemigos derrotados y si el jugador pierde puntos por obstaculos del jugo

# Versión
Esta es la versión 2.0 del juego.
Futuras Versiones incluiran correciones del juego y su mejoramiento

# Autores
- Harold Espinoza Matarrita - *Programador*
- Fabricio Mena Mejia - *Programador*

