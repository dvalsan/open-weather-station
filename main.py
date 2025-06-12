from pyb import I2C
import machine, time, json, struct
import loraConfig
from lib import aht20, lis3dhtr, sgp40, camera, loramanager

i2c = I2C(3, I2C.MASTER)
led = machine.Pin("LED_RED", machine.Pin.OUT)

ENABLE_LORA = True
DEBUG_MODE = True

def initAll():
    initalizationFinished = False
    while(not initalizationFinished):

        # Si el hub y la pantalla están bien, procedemos a inicializar el resto, mostrando por pantalla si está mal

        try:
            # Inicializamos la calibración del AHT0
            aht20.init()

            # Inicializamos el acelerómetro
            lis3dhtr.init()

            # Cambiamos el rango de calibración del acelerómetro a +-4g
            lis3dhtr.setRange(4)

            # Inicializamos el sensor de calidad del aire SGP40 (VOC)
            sgp40.init()

            # Inicializamos la camara para el clima
            camera.cameraInit()

            # Conectamos con TTN para "inicializar" el lora
            if ENABLE_LORA:
                loramanager.DEV_EUI = loraConfig.DEV_EUI
                loramanager.APP_EUI = loraConfig.APP_EUI
                loramanager.APP_KEY = loraConfig.APP_KEY
                while not loramanager.connectToTtn():
                    if DEBUG_MODE:
                        print("Initial connection failed. Resetting...")
                    time.sleep(5)
                    machine.reset()  # Hard reset if connection fails

            initalizationFinished = True
        except Exception as e:
            led.off()
            if DEBUG_MODE:
                print(e)
            time.sleep(0.5)
            if str(e) == "Frame capture has timed out.":
                machine.reset()

    led.on()

def loop():
    while(True):
        try:
            # Recibimos tempteratura y humedad del AHT20
            temp, hum = aht20.read()

            # Leemos calidad del aire tanto en Raw como el equivalente
            # a través del SGP40 con las medidas obtenidas de antes
            airQualityRaw = sgp40.readRawValue(temp, hum)
            airQuality = sgp40.getAirQuality(airQualityRaw)

            # Medimos los ejes del acelerometro
            accel = lis3dhtr.readAcceleration()

            # Recogemos los datos de la camra y predicciones
            predictionList = camera.getPredictionsList()
            maxPrediction = max(predictionList, key=lambda x: x[1])
            maxClima = camera.translateClima(maxPrediction[0])
            maxPercentage = maxPrediction[1]*100

            if DEBUG_MODE:
                # Mostramos todo por pantalla
                print(f"Temp: {temp:.2f}ºC")
                print(f"Humedad:{hum: .2f}%")
                print(f"Calidad aire: {airQualityRaw} {airQuality}")
                print(f"Acc(g): X={accel[0]:.2f} Y={accel[1]:.2f} Z={accel[2]:.2f}")
                print(f"Clima: {maxClima} = {maxPrediction[1]*100:.2f}%")

            if ENABLE_LORA:
                # Al estar en TR0 (SF12) el tamaño max de byes es de 52, asi que toca transformar a binario los datos
                # Configuramos a TR0 para poder tener la mayor distancia posible
                payload = struct.pack(
                ">ffffff1s1s",
                temp,
                hum,
                accel[0],
                accel[1],
                accel[2],
                maxPercentage,
                sgp40.getAirQualityAbreviated(airQualityRaw).encode('utf-8'),
                camera.abreviateClima(maxClima).encode('utf-8')
                )

                if DEBUG_MODE:
                    print("logitud de paquete:",str(len(payload)))
                    print(f"Sending message #{loramanager.counter}: {payload}")

                # Enviamos el jsonData y sin confirmación
                loramanager.sendData(payload, False)

                # Wait before sending next message - CRITICAL for EU868 compliance
                # After the first message the fair use makes you wait a 1% times, this is equals to 3.5minutes
                # After the first message the rest are going through every 30s okay (tested with crono)
                # For EU868, minimum wait time should be 5+ minutes for small payloads

                waitTime = loraConfig.LORA_INITIAL_TIME if loramanager.counter == 0 else loraConfig.LORA_INTERVAL_TIME

                print(f"Waiting {waitTime} seconds before next transmission (EU868 duty cycle)...")

                # Implement a countdown to make it easier to track waiting time
                for remaining in range(waitTime, 0, -10):
                    print(f"Next transmission in {remaining} seconds...")
                    time.sleep(10)

        except Exception as e:
            led.off()
            if DEBUG_MODE:
                print(str(e))
            time.sleep(0.5)
            initAll()

initAll()
loop()
