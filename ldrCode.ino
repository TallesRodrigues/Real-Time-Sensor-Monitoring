
int ldrPin;
int ldrValue;
int id_device;
String sensor;
String insert_command;

void setup() {
  // put your setup code here, to run once:
    ldrPin =0;
    id_device = 1;
    sensor = "ldr";
    insert_command = "Insert";
    Serial.begin(9600);
    
}

void loop() {
  // put your main code here, to run repeatedly:
  ldrValue = analogRead(ldrPin);

 Serial.println(insert_command+","+id_device+","+sensor+","+ldrValue); 
     
 
 delay(1*1000);
}
