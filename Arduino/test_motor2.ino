String incoming;
int x;
int y;
int xMin;
int xMax;
int yMin;
int yMax;
int PWMMin;
int PWMMax;
int forwardSpeed;
long area;

void setup() {
  Serial.begin(9600);
  
  //Motor Pins
  pinMode(6,OUTPUT);                          //6 = EN1
  pinMode(7,OUTPUT);                          //7 = IN1
  pinMode(8,OUTPUT);                          //8 = IN2
  pinMode(9,OUTPUT);                          //9 = EN2
  pinMode(10,OUTPUT);                         //10 = IN3
  pinMode(11,OUTPUT);                         //11 = EN4
  
  //Pixel Coordinates
  xMin = 0;
  xMax = 320;
  yMin = 140;
  yMax = 240;

  //Speeds
  PWMMin = 20;
  PWMMax = 100;

  //Incoming String
  incoming.reserve(16); 
  //always reserve 8 bytes of memory for the incoming string
  //using strings is dangerous on microcontrollers with limited RAM because it can cause memory fragmentation
  //always reserving 8 bytes of memory for our string can apparently help protect against this
  //explained more in detail here https://cpp4arduino.com/2018/11/06/what-is-heap-fragmentation.html#:~:text=This%20phenomenon%20is%20what%20we,full%20capacity%20of%20the%20microcontroller
  //I chose 16 because every character we read in is a byte and our max x value is 320 and our max y value is 240 and thus the maximum possible value for the area of the object detection box is 240x320=76800
  //each character in a string is a byte. The longest string we will receive is xxx yyy aaaaa\n which is 14 bytes long. Then I just rounded up to the closest power of 2 that was greater   
}
void loop() {
  /*
  digitalWrite(9,HIGH); //9 = IN1
  digitalWrite(10,LOW); //10 = IN2
  20 <= turnSpeed <= 100 
  */
  if (Serial.available() > 0) {
    // read the incoming string from the raspberry pi
    incoming = Serial.readStringUntil('\n');
    int strLength = incoming.length()+1;
    char array[strLength]; //we need a char array so that we can split up the 3 values from each other
    incoming.toCharArray(array,strLength);
    
    char * value = strtok(array, " "); //split up the incoming data based on space
    x = atoi(value); //convert to int and save
    value=strtok(NULL, " "); //advance to second value
    y = atoi(value); //convert to int and save
    value=strtok(NULL, " "); //advance to third value
    area = atol(value); //convert to long and save because this value might get more than the max int value: its pixels squared
/*
    Serial.println(x); //just printing them out to test
    Serial.println(y); //just printing them out to test
    Serial.println(area); //just printing them out to test
*/
  //Translational
  if(y > 140){ //Forward
  forwardSpeed = (((y - yMin)*(PWMMax - PWMMin))/(yMax - yMin)) + PWMMin;
  //Left Motor
      analogWrite(6,forwardSpeed);
      digitalWrite(7,HIGH);
      digitalWrite(8,LOW);
  //Right Motor
      analogWrite(9,forwardSpeed);
      digitalWrite(10,HIGH);
      digitalWrite(11,LOW);
  }else{ //Float
    //Left Motor
      analogWrite(6,0);
      digitalWrite(7,HIGH);
      digitalWrite(8,HIGH);
  //Right Motor
      analogWrite(9,0);
      digitalWrite(10,HIGH);
      digitalWrite(11,HIGH);  
  }
  //Orientation
  if(x < 150){                              //Left Turn
     //Left Motor
     analogWrite(6,20);
     digitalWrite(7,LOW);
     digitalWrite(8,HIGH);
     //Right Motor
     analogWrite(9,20);
     digitalWrite(10,LOW);
     digitalWrite(11,HIGH);
  }else if(x > 170){                        //Right Turn
     //Left Motor
     analogWrite(6,20);
     digitalWrite(7,LOW);
     digitalWrite(8,HIGH);
     //Right Motor
     analogWrite(9,20);
     digitalWrite(10,HIGH);
     digitalWrite(11,LOW);
  }else{                                    //Float
     //Left Motor
      analogWrite(6,0);
      digitalWrite(7,HIGH);
      digitalWrite(8,HIGH);
  //Right Motor
      analogWrite(9,0);
      digitalWrite(10,HIGH);
      digitalWrite(11,HIGH);  
  }
  }
  }
