# 🌤️ Open Weather Station

## Table of contents
- [🌤️ Open Weather Station](#️-open-weather-station)
  - [Table of contents](#table-of-contents)
  - [⚡ Components](#-components)
  - [📂 Folders](#-folders)
  - [🚀 Steps to execute and configure everything](#-steps-to-execute-and-configure-everything)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Configure the board](#2-configure-the-board)
    - [3. Configure the sensors](#3-configure-the-sensors)
    - [4. Configure The Things Network (TTN)](#4-configure-the-things-network-ttn)
    - [5. Configure the backend with Docker](#5-configure-the-backend-with-docker)
    - [6. Configure the frontend with Grafana](#6-configure-the-frontend-with-grafana)
    - [7. Connect the power to the board](#7-connect-the-power-to-the-board)
    - [Debugging the process](#debugging-the-process)
  - [License](#license)

This program has been developed on OpenMV IDE using micropython because of the Lora Shield by OpenMV having a camera (and using it for machine learning and detect the climatology).

All the sensors use Grove connectors and I2C protocol.

This repository, shows the components used, the libraries I created for each component, the lora communication to <a href="https://www.thethingsnetwork.org/"> The Things Network</a> and how to extract data with the use of TIG (Telegraf, Influxdb and Grafana) and also a bit of models I created for it to stay outside and take measures.


## ⚡ Components
<p align="left">
  <strong> - Portenta H7 </strong>
    <a href="https://docs.arduino.cc/resources/datasheets/ABX00042-ABX00045-ABX00046-datasheet.pdf">
    <i class="fas fa-file-alt"></i> Docs
    </a>
    <a href="https://store.arduino.cc/en-es/products/portenta-h7">
    <i class="fas fa-shopping-cart"></i> Arduino Store
    </a>
</p>
<p align="left">
  <strong> - Portenta Vision Shield - Lora </strong>
    <a href="https://docs.arduino.cc/resources/datasheets/ASX00021-ASX00026-datasheet.pdf">
    <i class="fas fa-file-alt"></i> Docs
    </a>
    <a href="https://store.arduino.cc/en-es/products/arduino-portenta-vision-shield-lora%C2%AE">
    <i class="fas fa-shopping-cart"></i> Arduino Store
    </a>
</p>
<p align="left">
  <strong> - I2C Hub (Grove 6 Port) </strong>
    <a href="https://www.seeedstudio.com/Grove-I2C-Hub-6-Port-p-4349.html">
    <i class="fas fa-shopping-cart"></i> Seeedstudio
    </a>
</p>
<p align="left">
  <strong> - AHT20 (Temperature and Humidty) </strong>
    <a href="https://files.seeedstudio.com/wiki/Grove-AHT20_I2C_Industrial_Grade_Temperature_and_Humidity_Sensor/AHT20-datasheet-2020-4-16.pdf">
    <i class="fas fa-file-alt"></i> Docs
    </a>
    <a href="https://www.seeedstudio.com/Grove-AHT20-I2C-Industrial-grade-temperature-and-humidity-sensor-p-4497.html">
    <i class="fas fa-shopping-cart"></i> Seeedstudio
    </a>
</p>
<p align="left">
  <strong> - SGP40 (VOC Gas) </strong>
    <a href="https://files.seeedstudio.com/wiki/Grove_SGP40/Sensirion_Gas_Sensors_Datasheet_SGP40.pdf">
    <i class="fas fa-file-alt"></i> Docs
    </a>
    <a href="https://www.seeedstudio.com/Grove-Air-Quality-Sensor-SGP40-p-5700.html">
    <i class="fas fa-shopping-cart"></i> Seeedstudio
    </a>
</p>
<p align="left">
  <strong> - LIS3DHTR (3 Axis Digital Accelerometer) </strong>
    <a href="https://www.mouser.es/datasheet/2/389/lis3dh-1849589.pdf">
    <i class="fas fa-file-alt"></i> Docs
    </a>
    <a href="https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-LIS3DHTR-p-4533.html">
    <i class="fas fa-shopping-cart"></i> Seeedstudio
    </a>
</p>
<p align="left">
  <strong> - LCD RGB Backlight</strong>
    <a href="https://files.seeedstudio.com/wiki/Grove-LCD_RGB_Backlight/Grove-LCD_RGB_Backlight_V5.0_Datasheet.pdf">
    <i class="fas fa-file-alt"></i> Docs (LCD)
    </a>
    <a href="https://www.nxp.com/docs/en/data-sheet/PCA9633.pdf">
    <i class="fas fa-file-alt"></i> Docs (RGB)
    </a>
    <a href="https://www.seeedstudio.com/Grove-LCD-RGB-Backlight.html">
    <i class="fas fa-shopping-cart"></i> Seeedstudio
    </a>
</p>
<p align="left">
  <strong> - Lithium Polymer Battery</strong>
    <a href="https://www.eemb.com/product-136">
    <i class="fas fa-file-alt"></i> Docs
    </a>
    <a href="https://es.aliexpress.com/i/10000043885157.html">
    <i class="fas fa-shopping-cart"></i> Aliexpress
    </a>
</p>
<p align="left">
  <strong> - Lipo Rider Plus (Charger / Booster) </strong>
    <a href="https://raw.githubusercontent.com/SeeedDocument/Lipo-Rider-Plus/master/res/ETA9740_V1.1.pdf">
    <i class="fas fa-file-alt"></i> Docs
    </a>
    <a href="https://www.seeedstudio.com/Lipo-Rider-Plus-p-4204.html">
    <i class="fas fa-shopping-cart"></i> Seeedstudio
    </a>
</p>
<p align="left">
  <strong> - Solar Panel 5V 2.5W </strong>
</p>

## 📂 Folders

- **root**
    - labels.txt and trained.tflite are two files generated by <a href="https://edgeimpulse.com/"> Edge Impulse</a> used for the machine learning algorithm that (along with the OpenMV shield camera) determinates the weather. You can check the dataset used for this data here <a href="https://www.kaggle.com/datasets/vijaygiitk/multiclass-weather-dataset">Kaggle</a>
    - main.py it's the main program where eveything is managed. It divides in two parts "init()" where all components initialice and check if they are connected or not and the "loop()" where all the process happens.
    - loraConfig.py it's ur ".env" it contains the variables needed for the lora communication.
- **lib**
    It contains a .py file for each component used and supported on this program.
  - [aht20.py](lib/aht20.py) for the AHT20 temperature and humidity sensor.
  - [camera.py](lib/camera.py) for the Edge Impulse (machine learning) calls that returns the predicted weather.
  - [lcd.py](lib/lcd.py) for the LCD module, currently not used on the main, but is there in case is needed.
  - [lis3dhtr.py](lib/lis3dhtr.py) for the LIS3DHTR 3 Axis module.
  - [loramanager.py](lib/loramanager.py) for the lora management and comunication.
  - [sgp40.py](lib/sgp40.py) for the SGP40 VOC Gas sensor.
- **model**
    It contains all the .stl that I used to print a "cover" for all the components, also has a .f3d in case you want to modify anything on Fusion360
    - **schematics**
        It contains the schematics for the project
- **docker**
    It contains all the configurations and an docker-compose file for the TIG construction, further information will be send on how to configure it.


---

## 🚀 Steps to execute and configure everything

### 1. Clone the repository

```bash
git clone https://github.com/dvalsan/open-weather-station.git
cd open-weather-station
```

### 2. Configure the board

- Install [OpenMV IDE](https://openmv.io/pages/download).
- Connect the micro controller to the computer and make sure the IDE detects it.
- Once the IDE detects the board it will prompt a window to install the firmware, double click the reset button on the micro controller and start the firmware installation.
- Open the main.py file with the OpenMV IDE and load it on the board (Tools > Save Open Script to OpenMV Cam as main.py).
- Load the following files and folders into de board:
  - labels.txt
  - trained.tflite
  - lib folder
  - loraConfig.py (you need to configure this one with your LoRa information, follow the example)

### 3. Configure the sensors

- Connect the sensors to the hub with the help of the Grove connectors.
- You will also need a connector that goes from Grove to pin to connect the SDA and SCL I2C pins to the Portenta H7. [Portenta H7 datasheet](https://docs.arduino.cc/resources/datasheets/ABX00042-ABX00045-ABX00046-datasheet.pdf).

### 4. Configure The Things Network (TTN)

- Create an account on [The Things Network](https://www.thethingsnetwork.org/) and enter your console though your profile, once there select your location.
- Create a new project and add the board (Portenta Vision Shield LoRa in this case), also you will need your LoRa board DevEUI. 
- Once you configure your board access the Device overview, there is a section called "Activation information" where you need to annotate the AppEUI (usually its full zeros), DevEUI (you already know this one) and AppKey, these three values go to your loraConfig.py file inside your board files.
- Select your board on the devices section and go to the "Payload formatters" tab, there select the "Formatter type" as "Custom Javascript formatter" and paste the code from the loraPayloadFormatter.js on this repository.

### 5. Configure the backend with Docker

- To configure the backend you need two things: 
  - First is having docker installed on your computer, you can se more about Docker and the installation process [in here](https://www.docker.com/)
  - Secondly you will need to configure TTN MQTT to extract your data, go into your TTN console and project, on the left tab you will see and option called "Other integrations" open it and select MQTT there annotate three things:
    - Public address
    - Username
    - Click the "Generate new API key" button and copy it as the password.
  - These three values go into your docker/configurations/telegraf/telegraf.conf file, as the "servers", "username" and "password" variables.
  - Once you have that configured go into the docker folder and execute:
```bash
docker compose up
```
  - This will launch the influxDB database with the initialization under docker/configurations/influxdb/init-influxdb.sh, configure telegraf and start Grafana.

### 6. Configure the frontend with Grafana

- Grafana is located on your localhost:3000 the user is "admin" and password is "admin123" you can change this password later on your Porfile > Preferences > Language.
- With grafana open and logged in select the upper-left corner to open the menu and go to Connections > Add new connection search for influxdb and add it.
- To configure the connection we can make use of docker url management with the containers:
  - HTTP
    - URL: "http://influxdb:8086"
  - InfluxDB Details
    - Database: telegraf
    - User: telegraf
    - Password: telegrafroot
    - HTTP Method: GET
- Then click "Save & test" if everything is correct you will get a message saying "datasource is working."
- Then to create the dashboard go again to the menu and select Dashboards > New > New dashboard > Import dashboard and paste the docker/configurations/grafana/basicexample.json code into the "Import via dashboard JSON model" text area, click on Load > Import.
- You will see a lot of red icons on each measure cell this is because the datasource is not set, go into each one of them and select Edit, under the Queries tab on the bottom side, you will se a "Data source" select the one you configured and click on "Save dashboard" at the top-right, and the everything will be settled up.

### 7. Connect the power to the board

- You will need a battery that can bee connected to the Lipo Rider Plus, once you connect the battery the charging can be though the USB-C connector or you can connect a solar panel to the pins, to do this connect the positive cable into the "USB" pin and the ground cable on the "GND" pin beside the USB pin.
- Once you have the battery connected, use the USB to power the board and put the slider into the "ON" position.

### Debugging the process
- The board will send a join message to TTN, and every 5 minutes it will send up messages with the sensors data, to monitor this go to your TTN console and project, go to your board and select the "Live data" tab.
- To check if everything is being sent from the TTN server you can download [MQTT Explorer](https://mqtt-explorer.com/) or similar to check on the TTN MQTT queue, you will need to use the URL, Username and Password that you got from the integrations menu.
- To get see if everything is being saved on the database follow these steps:
  - Open a terminal and insert
```bash
docker ps
```
  - You will see all of the docker process, search for the one that has the image "influxdb:1.8" and annotate the container id
  - Execute the following code to enter the container as interactive
```bash
docker exec -it <your-container-id> influx
```
  - Once inside the container we need to select the database
```bash
use telegraf
```
  - And then we can check the database using basic SQL sentences
``` bash
SELECT * FROM TTN
```

## License

**MIT License**

Copyright (c) 2025 David Valdivia Sanchis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

