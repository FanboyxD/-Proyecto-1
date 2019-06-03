const int btn = 2;
const int ejeX = A0;
const int ejeY = A1;
int X = 0;
int Y = 0;
int LED = 0;

void setup(){
  pinMode(btn, INPUT);
  pinMode(ejeX, INPUT);
  pinMode(ejeY, INPUT);
  Serial.begin(9600);
}


void loop() {
  Serial.println("{\"x\":" + (String)analogRead(ejeX) + ", \"y\":" + (String)analogRead(ejeY) +  ", \"boton\":" + (String)digitalRead(btn) + "}");
  delay(100);
}
