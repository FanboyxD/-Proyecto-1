const int btn = 2;
const int ejeX = 0;
const int ejeY = 1;
int LED = 0;

void setup(){
  pinMode(btn, INPUT);
  pinMode(ejeX, INPUT);
  pinMode(ejeY, INPUT);
  Serial.begin(9600);
}


void loop() {
  Serial.println();
  delay(500);
}
