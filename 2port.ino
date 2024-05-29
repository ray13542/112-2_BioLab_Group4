#define INTERVAL_LENGTH_US 1000UL  //1000UL = 1ms
unsigned long previousMicros = micros();
void setup() 
{
  Serial.begin(115200);
}

void loop() 
{
  unsigned long currentmicros = micros();
  if ((currentmicros-previousMicros) >= INTERVAL_LENGTH_US)
  {
    previousMicros += INTERVAL_LENGTH_US;
    int v1 = analogRead(A1);
    int v2 = analogRead(A2);
    String combined_string = String(v1)+','+String(v2);
    Serial.println(combined_string);
  }
  
}