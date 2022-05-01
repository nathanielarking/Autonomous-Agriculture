int flowPin = 5;    //This is the input pin on the Arduino
volatile int count = 0; //This integer needs to be set as volatile to ensure it updates correctly during the interrupt process.
int last_count = 0;
float vol = 0;

unsigned long int last_time = 0;

ICACHE_RAM_ATTR void Flow()
{
   count++; //Every time this function is called, increment "count" by 1
}

void setup() {
  // put your setup code here, to run once:
  pinMode(flowPin, INPUT_PULLUP);           //Sets the pin as an input
  attachInterrupt(digitalPinToInterrupt(flowPin), Flow, RISING);  //Configures interrupt 0 (pin 2 on the Arduino Uno) to run the function "Flow"
  Serial.begin(115200);

  //last_time = millis();

}
void loop() {

  vol = (float(count) / 1380) * 1000;
  //float rate = (((count - last_count) / 1380) / (millis() - last_time)) * 1000 * 60; //Find the flow rate in L/min 
  //last_count = count;
  //last_time = millis();

  //Serial.print("Volume (ml): ");
  Serial.println(count);
  //Serial.print(", Rate(L/min): ");
  //Serial.println(rate);

  delay(500);
  
}
