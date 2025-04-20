#include <Wire.h>
#include <LiquidCrystal_I2C.h> 
#define trigPin 12
#define echoPin 11
#define ledVermelho 7
#define ledAmarelo 6
#define ledVerde 5
#define buzzer 13
#define lin 2
#define col 16
#define index 0x27

LiquidCrystal_I2C display(index,col,lin);

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  display.init();
  display.backlight();
  display.clear();
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long tempo = pulseIn(echoPin, HIGH);
  float distancia = (tempo * 0.0343) / 2;

  display.setCursor(0,0); 
  display.print("PROJETO IOT"); 
  delay(2000);  
  display.clear(); 
  delay(500);

  if(distancia > 150){
    digitalWrite(ledVerde, HIGH);
    delay(300);
    digitalWrite(ledVerde, LOW);
    
    display.setCursor(0,0); 
    display.print("SEGURO"); 
    }

    else if (distancia > 50){
      digitalWrite(ledAmarelo, HIGH);
      delay(200);
      digitalWrite(ledAmarelo, LOW);

      display.setCursor(0,0); 
      display.print("ARRISCADO."); 
      display.setCursor(0, 1); 
      display.print("ATENCAO!");

      } else{
          digitalWrite(buzzer, HIGH);
          digitalWrite(ledVermelho, HIGH);
          delay(100);
          digitalWrite(ledVermelho, LOW);
          digitalWrite(buzzer, LOW);

          display.setCursor(0,0); 
          display.print("PARE!"); 
        }

  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.print(" cm\n");

  delay(1000);
}
