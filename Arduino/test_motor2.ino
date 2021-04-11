void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
}
String directionPi = "";
void loop() {
  // put your main code here, to run repeatedly:
  /*
  digitalWrite(9,HIGH); //9 = IN1
  digitalWrite(10,LOW); //10 = IN2
  */

  
  if (Serial.available() > 0){
    directionPi = Serial.readStringUntil('\n');
  }
  if(directionPi.compareTo("2") == 0){ //Backwards
     digitalWrite(9,LOW);
     digitalWrite(10,HIGH);
  }else if(directionPi.compareTo("1") == 0){ //Forwards
     digitalWrite(9,HIGH);
     digitalWrite(10,LOW);
  }else{
     digitalWrite(9,LOW);
     digitalWrite(10,LOW);
  }

  
  
  analogWrite(11,20);
}
