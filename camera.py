#   example-tft144.py          V1.6
#   Brian Lavery (C) Oct 2014    brian (at) blavery (dot) com
#   Free software.

# Demonstrates the "BLACK" & "RED" 128x128 SPI TFT board

# There are 3 variants of this file:
#      example-tft144.py                <<<< THIS ONE  - picks virtual or raspberry automatically
#      example-tft144-rpi-only.py
#      example-tft144-vgpio-only.py



import RPi.GPIO as GPIO
from lib_tft144 import TFT144
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
# My tests. Two configurations.

if GPIO.RPI_REVISION == 0:   # VIRTUAL-GPIO
    print("Virtual")
    RST =  8
    CE =  10    # VirtGPIO: the chosen Chip Select pin#. (different from rpi)
    DC =   9
    LED =  7
    spidev = GPIO
    # the virtual GPIO module directly supports spidev function

else:   # RPI
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    RST = 15    # RST may use direct +3V strapping, and then be listed as 0 here. (Soft Reset used instead)
    CE =   0    # RPI GPIO: 0 or 1 for CE0 / CE1 number (NOT the pin#)
    DC =  12    # Labeled on board as "A0"   Command/Data select
    LED =  13   # LED may also be strapped direct to +3V, (and then LED=0 here). LED sinks 10-14 mA @ 3V
    import spidev


# Don't forget the other 2 SPI pins SCK and MOSI (SDA)

TFT = TFT144(GPIO, spidev.SpiDev(), CE, DC, RST, LED, isRedBoard=False)

with PiCamera() as camera:
    camera.resolution = (128, 112)
    camera.rotation = 270
    camera.framerate = 40
    rawCapture = PiRGBArray(camera, size=(128, 112))
    # allow the camera to warmup
    time.sleep(0.1)
    print("Starting...")
    start = time.time()

    # capture frames from the camera
    c=0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        img = frame.array
        # show the frame
        TFT.display(128, img)
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if time.time() - start > 10:
            break
        c+=1
#os.system("shutdown -h now")
TFT.clear_display(TFT.WHITE)

print(c/10.)
