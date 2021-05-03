import threading
from pyky040 import pyky040
from bulb import BulbService

DEVICE_NAME = "bedroom"

BRIGHTNESS_CLK_PIN = 17
BRIGHTNESS_DT_PIN = 18
BRIGHTNESS_SW_PIN = 27

TEMPERATURE_CLK_PIN = 12
TEMPERATURE_DT_PIN = 6
TEMPERATURE_SW_PIN = 13


bulb = BulbService(DEVICE_NAME)


def brightness_cb(scale_position):
    bulb.set_brightness(100 - scale_position)


def saturation_cb(scale_position):
    bulb.set_saturation(100 - scale_position)


def sw_callback():
    print("Switch!")
    bulb.toggle_power()


brightness_enc = pyky040.Encoder(CLK=BRIGHTNESS_CLK_PIN, DT=BRIGHTNESS_DT_PIN, SW=BRIGHTNESS_SW_PIN)
brightness_enc.setup(scale_min=0, scale_max=100, step=2, chg_callback=brightness_cb, sw_callback=sw_callback)

b_enc_t = threading.Thread(target=brightness_enc.watch)
b_enc_t.start()

sat_enc = pyky040.Encoder(CLK=TEMPERATURE_CLK_PIN, DT=TEMPERATURE_DT_PIN, SW=TEMPERATURE_SW_PIN)
sat_enc.setup(scale_min=0, scale_max=100, step=2, chg_callback=saturation_cb, sw_callback=sw_callback)
sat_enc.watch()

b_enc_t.join()
