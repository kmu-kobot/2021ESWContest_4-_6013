#include<stdlib.h>
int GasPinA = A0;
int GasPinB = A1;
int alertFlag = 0;
int buzz = 10;
int mean;
void setup() {
  // put your setup code here, to run once:
  pinMode(GasPinA, INPUT);
  pinMode(GasPinB, INPUT);
  pinMode(buzz, OUTPUT);
  Serial.begin(9600);
  digitalWrite(buzz, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Serial.println(analogRead(GasPinA));
  // Serial.println(analogRead(GasPinB));
  mean = (analogRead(GasPinA) + analogRead(GasPinB)) / 2;
  if(mean > 85){
    alertFlag = 1;
    digitalWrite(buzz, LOW);
    delay(100);
  }
  else if(mean < 85){
    alertFlag = 0;
    digitalWrite(buzz, HIGH);
    delay(100);
  }
  
  if(Serial.available())
  {
    String getData = Serial.readStringUntil('\n');
    if(getData == "CO")
    {
      if(alertFlag == 1)
      {
        Serial.print("WARNING");
        delay(20);
        Serial.print(mean, DEC);
        delay(5);
      }
      else
      {
        Serial.print(mean, DEC);
        delay(50);
      }
    }
  }
  delay(50);
}