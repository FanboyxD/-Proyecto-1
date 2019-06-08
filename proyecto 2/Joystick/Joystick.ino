// Se definen las variables necearias para el funcionamiento del control
const int btnshoot = 2; // Pin de coneccion de boton para el disparo
const int btnp = 3; //Pin del boton de pausa
const int btnr = 4; // Pin del boton de reanudar
const int btng = 5; //Pin del boton para guardar la partida
const int btnq = 6; // Pin del boton para reanudar la partida

const int ejeX = A0; // Pines de VRx y VRy del joystick (ejes x/y)
const int ejeY = A1;

//Configuracion inicicial
void setup(){
  //Se define que funcion tienen las patillas y se inicia la comunicacion serial
  pinMode(btnshoot, INPUT); //Para este caso todos los pines son de entrada
  pinMode(btnp, INPUT); 
  pinMode(btnr, INPUT); 
  pinMode(btng, INPUT); 
  pinMode(btnq, INPUT); 
  pinMode(ejeX, INPUT);
  pinMode(ejeY, INPUT);
  Serial.begin(9600);
}

// Loop del arduino
void loop() {
  //Se envian los datos en forma de {"x:,"y:, etc}como si se tratara de un archivo json
  Serial.println("{\"x\":" + (String)analogRead(ejeX) + ", \"y\":" + (String)analogRead(ejeY) +  ", \"Bshoot\":" + (String)digitalRead(btnshoot) + ", \"Pause\":" + (String)digitalRead(btnp) + ", \"continue\":" + (String)digitalRead(btnr) + ", \"Saveas\":" + (String)digitalRead(btng) + ", \"Load\":" + (String)digitalRead(btnq) +"}");
  delay(100);// tiene un tiempo de espera de 100ms antes de volver a realizar la operacion
}
