const int pingPin = 12; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 13; // Echo Pin of Ultrasonic Sensor

void setup() {
   Serial.begin(9600); // Starting Serial Terminal
   pinMode(pingPin, OUTPUT);
   pinMode(echoPin, INPUT);
}

void loop() {
   long duration, inches, cm;
   
   digitalWrite(pingPin, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
  
   duration = pulseIn(echoPin, HIGH);
   inches = microsecondsToInches(duration);
   cm = microsecondsToCentimeters(duration);

   //Serial.print(inches);
   //Serial.print("in, ");
   //Serial.print(cm);
   //Serial.print("cm");
   //Serial.println();
   Serial.println(duration);
   delay(100);
}

float microsecondsToInches(long microseconds) {
   return microseconds / 74.0 / 2.0;
}

float microsecondsToCentimeters(long microseconds) {
   return microseconds / 2.0 / 2.0;
}