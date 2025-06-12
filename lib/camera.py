# Edge Impulse climatology imports
import sensor, ml, uos, gc

net = None
labels = None

#Camera Initialization method
def cameraInit():
    sensor.reset()                         # Reset and initialize the sensor.
    sensor.set_pixformat(sensor.GRAYSCALE)    # Set pixel format to RGB565 (or GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
    sensor.set_windowing((240, 240))       # Set 240x240 window.
    sensor.skip_frames(time=2000)          # Let the camera adjust.

    # Edge Impulse ML Get Clima part
    try:
        global net
        # load the model, alloc the model file on the heap if we have at least 64K free after loading
        net = ml.Model("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
    except Exception as e:
        print(e)
        raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

    try:
        global labels
        labels = [line.rstrip('\n') for line in open("labels.txt")]
    except Exception as e:
        raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')


def translateClima(clima):
    """Returns the climatology translated from English to Spanish"""
    clima = clima.strip().lower()
    translations = {
        "cloudy": "Nublado",
        "foggy": "Brumoso",
        "rainy": "Lluvioso",
        "shine": "Soleado",
        "sunrise": "Amanecer",
    }
    return translations.get(clima,clima)

def abreviateClima(clima):
    """Return the receibed climatology (in spanish) to an abreviation"""
    translations = {
        "Nublado": "N",
        "Brumoso": "B",
        "Lluvioso": "L",
        "Soleado": "S",
        "Amanecer": "A",
    }
    return translations.get(clima,clima)

def getPredictionsList():
    img = sensor.snapshot()
    return list(zip(labels, net.predict([img])[0].flatten().tolist()))
