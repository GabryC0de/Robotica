#define speedPinR 9           //  Front Wheel PWM pin connect Model-Y M_B ENA
#define RightMotorDirPin1 22  //Front Right Motor direction pin 1 to Model-Y M_B IN1  (K1)
#define RightMotorDirPin2 24  //Front Right Motor direction pin 2 to Model-Y M_B IN2   (K1)
#define LeftMotorDirPin1 26   //Front Left Motor direction pin 1 to Model-Y M_B IN3 (K3)
#define LeftMotorDirPin2 28   //Front Left Motor direction pin 2 to Model-Y M_B IN4 (K3)
#define speedPinL 10          //  Front Wheel PWM pin connect Model-Y M_B ENB


void leftWheelForward(int PWM){         // left wheel forward drive
  digitalWrite(RightMotorDirPin1, LOW);
  digitalWrite(RightMotorDirPin2, LOW);
  analogWrite(speedPinR, 0);

  digitalWrite(LeftMotorDirPin1, HIGH);
  digitalWrite(LeftMotorDirPin2, LOW);
  analogWrite(speedPinL, PWM);
}

void botForward(int PWM_R, int PWM_L){  // driving both motors forward
  digitalWrite(RightMotorDirPin1, HIGH);
  digitalWrite(RightMotorDirPin2, LOW);
  analogWrite(speedPinR, PWM_R);

  digitalWrite(LeftMotorDirPin1, HIGH);
  digitalWrite(LeftMotorDirPin2, LOW);
  analogWrite(speedPinL, PWM_L);
}

void botBackwards(int PWM_R, int PWM_L){  // driving both motors backwards
  digitalWrite(RightMotorDirPin1, LOW);
  digitalWrite(RightMotorDirPin2, HIGH);
  analogWrite(speedPinR, PWM_R);

  digitalWrite(LeftMotorDirPin1, LOW);
  digitalWrite(LeftMotorDirPin2, HIGH);
  analogWrite(speedPinL, PWM_L);
}

void setup() {
  pinMode(RightMotorDirPin1, OUTPUT);
  pinMode(RightMotorDirPin2, OUTPUT);
  pinMode(speedPinL, OUTPUT);

  pinMode(LeftMotorDirPin1, OUTPUT);
  pinMode(LeftMotorDirPin2, OUTPUT);
  pinMode(speedPinR, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    Serial.println(Serial.read());  // Read a single character
    // if (command == 'r') {
    //   // Task for 'r' command (e.g., turn LED ON)
      
    // } else if (command == 'l') {
    //   // Task for 'l' command (e.g., turn LED OFF)
    //   digitalWrite(RightMotorDirPin1, LOW);
    //   digitalWrite(RightMotorDirPin2, LOW);
    //   analogWrite(speedPinR, 0);

    //   digitalWrite(LeftMotorDirPin1, HIGH);
    //   digitalWrite(LeftMotorDirPin2, LOW);
    //   analogWrite(speedPinL, 255);
    // } else if (command == 's') {
    //   digitalWrite(RightMotorDirPin1, LOW);
    //   digitalWrite(RightMotorDirPin2, LOW);
    //   analogWrite(speedPinR, 0);

    //   digitalWrite(LeftMotorDirPin1, LOW);
    //   digitalWrite(LeftMotorDirPin2, LOW);
    //   analogWrite(speedPinL, 0);
    // } else {
    //   Serial.println("Unknown command");
    // }
  }
}
