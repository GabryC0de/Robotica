#include <ArduinoJson.h>

int motor_left_speed;
int motor_right_speed;

#define speedPinRB 9   //  Front Wheel PWM pin connect Model-Y M_B ENA 
#define RightMotorDirPin1  22    //Front Right Motor direction pin 1 to Model-Y M_B IN1  (K1)
#define RightMotorDirPin2  24   //Front Right Motor direction pin 2 to Model-Y M_B IN2   (K1)                                 
#define LeftMotorDirPin1  26    //Front Left Motor direction pin 1 to Model-Y M_B IN3 (K3)
#define LeftMotorDirPin2  28   //Front Left Motor direction pin 2 to Model-Y M_B IN4 (K3)
#define speedPinLB 10   //  Front Wheel PWM pin connect Model-Y M_B ENB

#define speedPinR 11   //  Rear Wheel PWM pin connect Left Model-Y M_A ENA 
#define RightMotorDirPin1B  5    //Rear Right Motor direction pin 1 to Model-Y M_A IN1 ( K1)
#define RightMotorDirPin2B 6    //Rear Right Motor direction pin 2 to Model-Y M_A IN2 ( K1) 
#define LeftMotorDirPin1B 7    //Rear Left Motor direction pin 1 to Model-Y M_A IN3  (K3)
#define LeftMotorDirPin2B 8  //Rear Left Motor direction pin 2 to Model-Y M_A IN4 (K3)
#define speedPinL 12    //  Rear Wheel PWM pin connect Model-Y M_A ENB

void setup() {
  pinMode(RightMotorDirPin1, OUTPUT); 
  pinMode(RightMotorDirPin2, OUTPUT); 
  pinMode(speedPinR, OUTPUT);
 
  pinMode(LeftMotorDirPin1, OUTPUT);
  pinMode(LeftMotorDirPin2, OUTPUT); 
  pinMode(speedPinL, OUTPUT);  

  pinMode(RightMotorDirPin1B, OUTPUT); 
  pinMode(RightMotorDirPin2B, OUTPUT); 
  pinMode(speedPinRB, OUTPUT);
 
  pinMode(LeftMotorDirPin1B, OUTPUT);
  pinMode(LeftMotorDirPin2B, OUTPUT); 
  pinMode(speedPinLB, OUTPUT); 
  Serial.begin(9600); 
}

void loop() {

  // Check if data is available on the serial port
  if (Serial.available()) {
    // // Read the incoming JSON string
    String myString = Serial.readStringUntil('\n');
    delay(10);
    if (myString.charAt(0) != 'p') {
      Serial.println("");
      // Serial.println("PID not received");
    } else if(myString.charAt(0) == 'p') {
      
      String pid_value_string = myString.substring(1);
      int pid_value = pid_value_string.toInt();
      // Calcola la velocità dei motori in base al valore PID
      motor_left_speed = constrain(127 - pid_value, 0, 255);  // Motore sinistro (inversamente proporzionale)
      motor_right_speed = constrain(127 + pid_value, 0, 255); // Motore destro
      Forward(motor_right_speed, motor_left_speed);
      Serial.print("Left speed: ");
      Serial.print(motor_left_speed);
      Serial.print(" - Right speed: ");
      Serial.println(motor_right_speed);
    }
  }
}

// Funzioni --------------------------------------------

void Forward(int PWM_R, int PWM_L) {  // driving both motors forward

  digitalWrite(LeftMotorDirPin1, LOW);
  digitalWrite(LeftMotorDirPin2, HIGH); 
  analogWrite(speedPinR, PWM_R);

  digitalWrite(RightMotorDirPin1, LOW); 
  digitalWrite(RightMotorDirPin2, HIGH); 
  analogWrite(speedPinL, PWM_L); 
}

void Backwards(int PWM_R, int PWM_L) {  // driving both motors backwards
  digitalWrite(RightMotorDirPin1, LOW);
  digitalWrite(RightMotorDirPin2, HIGH);
  analogWrite(speedPinR, PWM_R);

  digitalWrite(LeftMotorDirPin1, LOW);
  digitalWrite(LeftMotorDirPin2, HIGH);
  analogWrite(speedPinL, PWM_L);
}





