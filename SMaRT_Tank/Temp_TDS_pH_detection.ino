#define TdsSensorPin A1
#define VREF 5.0 // analog reference voltage(Volt) of the ADC
#define SCOUNT 30 // sum of sample point
#define PH_PIN A0
#include <OneWire.h>
int analogBuffer[SCOUNT]; // store the analog value in the array, read from ADC
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0,copyIndex = 0;
float averageVoltage = 0,tdsValue = 0,temperature = 25;
int DS18S20_Pin = 7;
float calibration_value = 21.34 - 1.5;
int phval = 0;
unsigned long int avgval;
int buffer_arr[10], temp;
int delaytime = 3000;
int buffer_arr_index = 0;

OneWire ds(DS18S20_Pin);

void setup()
{
Serial.begin(115200);
pinMode(TdsSensorPin,INPUT);
}
void loop()
{
static unsigned long analogSampleTimepoint = millis();
if(millis()-analogSampleTimepoint > 250U) //every 40 milliseconds,read the analog value from the ADC
{
analogSampleTimepoint = millis();
analogBuffer[analogBufferIndex] = analogRead(TdsSensorPin); //read the analog value and store into the buffer
analogBufferIndex++;
if(analogBufferIndex == SCOUNT)
analogBufferIndex = 0;
}
static unsigned long phSampleTimepoint = millis();
if (millis()-phSampleTimepoint > 500U){
  buffer_arr[buffer_arr_index] = analogRead(PH_PIN);
  buffer_arr_index += 1;
}
if (buffer_arr_index == 10)
  buffer_arr_index = 0;
static unsigned long printTimepoint = millis();
if(millis()-printTimepoint > 5000U)
{
printTimepoint = millis();
for(copyIndex=0;copyIndex<SCOUNT;copyIndex++)
analogBufferTemp[copyIndex]= analogBuffer[copyIndex];
averageVoltage = getMedianNum(analogBufferTemp,SCOUNT) * (float)VREF/ 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
float compensationCoefficient=1.0+0.02*(temperature-25.0); //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
float compensationVolatge=averageVoltage/compensationCoefficient; //temperature compensation
tdsValue=(133.42*compensationVolatge*compensationVolatge*compensationVolatge - 255.86*compensationVolatge*compensationVolatge + 857.39*compensationVolatge)*0.5; //convert voltage value to tds value

 for(int i=0;i<9;i++)
 {
 for(int j=i+1;j<10;j++)
  {
 if(buffer_arr[i]>buffer_arr[j])
    {
 temp=buffer_arr[i];
 buffer_arr[i]=buffer_arr[j];
 buffer_arr[j]=temp;
    }
  }
 }
 avgval=0;
 for(int i=2;i<8;i++)
 avgval+=buffer_arr[i];

 float volt=(float)avgval*5.0/1024/6;
 float ph_act = -5.70 * volt + calibration_value;
//Serial.print("voltage:");
//Serial.print(averageVoltage,2);
//Serial.print("V ");
float temperature = getTemp();
Serial.print(temperature);
Serial.print(",");
Serial.print(tdsValue,0);
Serial.print(",");
Serial.println(ph_act);
}
}
int getMedianNum(int bArray[], int iFilterLen)
{
int bTab[iFilterLen];
for (byte i = 0; i<iFilterLen; i++)
bTab[i] = bArray[i];
int i, j, bTemp;
for (j = 0; j < iFilterLen - 1; j++)
{
for (i = 0; i < iFilterLen - j - 1; i++)
{
if (bTab[i] > bTab[i + 1])
{
bTemp = bTab[i];
bTab[i] = bTab[i + 1];
bTab[i + 1] = bTemp;
}
}
}
if ((iFilterLen & 1) > 0)
bTemp = bTab[(iFilterLen - 1) / 2];
else
bTemp = (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
return bTemp;
}
float getTemp(){
 //returns the temperature from one DS18S20 in DEG Celsius

 byte data[12];
 byte addr[8];

 if ( !ds.search(addr)) {
   //no more sensors on chain, reset search
   ds.reset_search();
   return -1000;
 }

 if ( OneWire::crc8( addr, 7) != addr[7]) {
   Serial.println("CRC is not valid!");
   return -1000;
 }

 if ( addr[0] != 0x10 && addr[0] != 0x28) {
   Serial.print("Device is not recognized");
   return -1000;
 }

 ds.reset();
 ds.select(addr);
 ds.write(0x44,1); // start conversion, with parasite power on at the end

 byte present = ds.reset();
 ds.select(addr);  
 ds.write(0xBE); // Read Scratchpad

 
 for (int i = 0; i < 9; i++) { // we need 9 bytes
  data[i] = ds.read();
 }
 
 ds.reset_search();
 
 byte MSB = data[1];
 byte LSB = data[0];

 float tempRead = ((MSB << 8) | LSB); //using two's compliment
 float TemperatureSum = (tempRead / 16) - 0.6;
 
 return TemperatureSum;
 
}
