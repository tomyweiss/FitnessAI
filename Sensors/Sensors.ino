// These constants won't change. They're used to give names to the pins used:
const int analogInPin0 = A0;  // Analog input pin that the potentiometer is attached to

const int analogOutPin = 9;  // Analog output pin that the LED is attached to

int sensorValue0 = 0;  // value read from the pot

int outputValue = 0;  // value output to the PWM (analog out)

// Mux control pins
int s0 = 8;
int s1 = 9;
int s2 = 10;
int s3 = 11;

// Mux in "SIG" pin
int SIG_pin = 0;

void setup() {
  // Initialize serial communications at 9600 bps:
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);

  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);

  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Read the analog in value:

  // Loop through and read all 16 values
  int reading = 0;
  for (int i = 0; i < 14 /*16*/; i++) {
    reading = readMux(i);
    if (reading > 0) {
      // Get the current timestamp
      unsigned long currentMillis = millis();
      unsigned long seconds = currentMillis / 1000;
      unsigned long hours = seconds / 3600;
      seconds %= 3600;
      unsigned long minutes = seconds / 60;
      seconds %= 60;

      // Format the timestamp
      char timestamp[9];
      snprintf(timestamp, sizeof(timestamp), "%02lu:%02lu:%02lu", hours, minutes, seconds);

      // Remove the decimal part of the milliseconds
      int decimalPart = currentMillis % 1000;
      int milliseconds = decimalPart / 10;

      // Log the force data along with the timestamp
     
      Serial.print(timestamp);
      Serial.print(":");
      Serial.print(milliseconds);
      Serial.print(",");
      Serial.print(i);
      Serial.print(",");
      Serial.print(reading);
       Serial.println("|");
      
      
    }
    delay(30);
  }

  /*sensorValue0 = analogRead(analogInPin0);
  Serial.print("\n sen0 = ");
  Serial.print(sensorValue0);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(10);
  digitalWrite(LED_BUILTIN, LOW);
  delay(10);*/
}

int readMux(int channel) {
  int controlPin[] = { s0, s1, s2, s3 };

  int muxChannel[16][4] = {
    { 0, 0, 0, 0 }, //channel 0
    { 1, 0, 0, 0 }, //channel 1
    { 0, 1, 0, 0 }, //channel 2
    { 1, 1, 0, 0 }, //channel 3
    { 0, 0, 1, 0 }, //channel 4
    { 1, 0, 1, 0 }, //channel 5
    { 0, 1, 1, 0 }, //channel 6
    { 1, 1, 1, 0 }, //channel 7
    { 0, 0, 0, 1 }, //channel 8
    {1, 0, 0, 1}, //channel 9
    {0, 1, 0, 1}, //channel 10
    {1, 1, 0, 1}, //channel 11
    {0, 0, 1, 1}, //channel 12
    {1, 0, 1, 1}, //channel 13
    {0, 1, 1, 1}, //channel 14
    {1, 1, 1, 1}  //channel 15
  };

  // Loop through the 4 sig
  for (int i = 0; i < 4; i++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  // Read the value at the SIG pin
  int val = analogRead(SIG_pin);

  // Return the value
  return val;
}