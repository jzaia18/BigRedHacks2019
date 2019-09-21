/*
  Hello World.ino
  2013 Copyright (c) Seeed Technology Inc.  All right reserved.

  Author:Loovee
  2013-9-18

k,
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.
;p
  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include <CurieBLE.h>
#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

//Bluetooth Initialization

BLEService userService("0000181c-0000-1000-8000-00805f9b34fbC");       // BLE User Data Service
BLEUnsignedCharCharacteristic switchCharacteristic("0000181c-0000-1000-8000-00805f9b34fb", BLERead | BLENotify);

//LCD Initialization
const int colorR = 117;
const int colorG = 21;
const int colorB = 32;

//Button Initialization
int buttonState = 0;
int buttonCount = 0;
const int buttonPin = 2;

//Temp Sensor Initialization
const int B = 4275;
const int R0 = 100000;
const int pinTempSensor = A0;
int mode = 0; 

void setup()  
{

    // Initialize the button pins
    pinMode(buttonPin, INPUT);
    
    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);
    lcd.setRGB(colorR, colorG, colorB);
    
    // Print a message to the LCD.
    lcd.print("Temperature Demo");

    //Set the Baud Rate
    Serial.begin(9600);

    // begin initialization
    BLE.begin();

    // set advertised local name and service UUID:
    BLE.setLocalName("TempService");
    BLE.setAdvertisedService(userService);

    // add the characteristic to the service
    userService.addCharacteristic(switchCharacteristic);

    // add service
    BLE.addService(userService);

    // set the initial value for the characeristic:
    switchCharacteristic.setValue(0);

    // start advertising
    BLE.advertise();

    Serial.println("BLE LED Peripheral");

    // Wait
    delay(2000);
}

void loop() 
{
    // listen for BLE peripherals to connect:
    BLEDevice central = BLE.central();

    // if a central is connected to peripheral:
    if (central) {
    lcd.print("Connected to central: ");
    // print the central's MAC address:
    lcd.print(central.address());

    delay(2000);
    lcd.clear();
    
    while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:

       
      updateTemperature();

     
  }
   // when the central disconnects, print it out:
      lcd.print(F("Disconnected from central: "));
      lcd.println(central.address());
}
}


void updateTemperature(){

      // Read the Temperature Sensor
      int degree = analogRead(pinTempSensor);

      // Temperature Index
      float R = 1023.0/degree-1.0;
      R = R0*R; 

      // Convert the temperature index to celcius
      float temperature = 1.0/(log(R/R0)/B+1/298.15)-273.15;

      lcd.print(temperature);
      

      switchCharacteristic.setValue(temperature);  // and update the heart rate measurement characteristic
      delay(1000);
      lcd.clear();
}



/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
