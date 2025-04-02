#define ultrasomInput 12
#define ultrasomOutput 11
#define ledVermelho 7
#define ledAmarelo 6
#define ledVerde 5
#define buzzer 13

void setup() {
  Serial.begin(9600);
  pinMode(ultrasomInput, OUTPUT);
  pinMode(ultrasomOutput, INPUT);

}

void loop() {
  digitalWrite(ultrasomInput, LOW);
  delayMicroseconds(2);
  digitalWrite(ultrasomInput, HIGH);
  delayMicroseconds(10);
  digitalWrite(ultrasomInput, LOW);

  long tempo = pulseIn(ultrasomOutput, HIGH);
  float distancia = (tempo * 0.0343) / 2;

  if(distancia > 300){
    digitalWrite(ledVerde, HIGH);
    delay(300);
    digitalWrite(ledVerde, LOW);
    }

    else if (distancia > 50){
      digitalWrite(ledAmarelo, HIGH);
      delay(200);
      digitalWrite(ledAmarelo, LOW);
    
      } else{
          digitalWrite(buzzer, HIGH);
          digitalWrite(ledVermelho, HIGH);
          digitalWrite(ledVermelho, LOW);
          digitalWrite(buzzer, LOW);
        }

  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.print(" cm\n");

  delay(500);
}
