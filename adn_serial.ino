/*
motor speed
*/
#include <AFMotor.h>

#define R_MAX 255
#define L_MAX 255
#define R_MID 120
#define L_MID 120

#define DELAY_TIME 120
#define SMALL_DELAY_TIME 150
#define TINY_DELAY_TIME 100

/*
motor pin number
a: right motor
b: left motor
*/

int a1 = 4;
int a2 = 5;
int b1 = 6;
int b2 = 7;

AF_DCMotor motor1(4);
AF_DCMotor motor2(1);
/*
constant delay time
delay time is wheel operation time
if the delay time is longer, the wheel operation time is longer.
*/

void setup(){
   Serial.begin(9600);
   // pinMode(a1,OUTPUT);
   // pinMode(a2,OUTPUT);
   // pinMode(b1,OUTPUT);
   // pinMode(b2,OUTPUT);
  motor1.setSpeed(200);
  motor2.setSpeed(200);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}

void test() {
  //우회전
   // motor1.run(BACKWARD);//오(반대)
  // motor2.run(FORWARD);//왼
  // motor1.setSpeed(200);
  // motor2.setSpeed(200);
   delay(2000);
}

void mainFunction(){
   char DataToRead[2];
   DataToRead[1] = '\n';
   
   Serial.readBytesUntil(char(13),DataToRead, 2);
   char direction = DataToRead[0];
   
   int i=1;
   while(DataToRead[i] != '\n' && i < 2) i++;
   
   switch(direction){
      case 'G':
         motor1.run(BACKWARD);
      motor2.run(FORWARD);
      motor1.setSpeed(160);
      motor2.setSpeed(160);
         delay(TINY_DELAY_TIME);
         break;

      case 'B':
         motor1.run(FORWARD);
      motor2.run(BACKWARD);
      motor1.setSpeed(160);
      motor2.setSpeed(160);
         delay(SMALL_DELAY_TIME);
         break;

      case 'L':
         motor2.run(FORWARD);
      motor2.setSpeed(200);
         delay(SMALL_DELAY_TIME);
         break;
      case 'R':
      motor1.run(BACKWARD);
      motor1.setSpeed(160);
         delay(SMALL_DELAY_TIME);
         break;
      case 'l':
         motor2.run(FORWARD);
      motor2.setSpeed(200);
         delay(SMALL_DELAY_TIME);
         break;
      case 'r':
         motor1.run(BACKWARD);
      motor1.setSpeed(160);
         delay(SMALL_DELAY_TIME);
         break;


      default:
         motor1.run(RELEASE);
      motor2.run(RELEASE);
      motor1.setSpeed(100);
      motor2.setSpeed(100);
         return;
    }
   if(direction == 'R' || direction == 'L'){
      delay(20);
    }
    else if(direction =='B'){
      delay(100);
    }
   
  //   analogWrite(a1,0);
   // analogWrite(a2,0);
   // analogWrite(b1,0);
   // analogWrite(b2,0);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
   delay(300);
   Serial.println(direction);
   
}

void loop(){
  // test();
 
  mainFunction();
}
