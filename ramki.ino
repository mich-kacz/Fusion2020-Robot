void setup()
{
  Serial.begin(19200);
  Serial.setTimeout(10);
  Serial.println("Connection start");
}



void loop(void)
{
  char data[15];
  int ret, rozm;
  long wart;
  if(Serial.available())
  {
     ret=Serial.readBytesUntil('\n',data,11);
     wart=atol(data);
     rozm= sizeof(data);
     Serial.print("Size of data: ");Serial.print(rozm);
     Serial.print("\t Return: ");Serial.print(ret);Serial.print("\t");
     Serial.println(data);
     
  }

}
