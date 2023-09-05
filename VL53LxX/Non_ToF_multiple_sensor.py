import time
import board
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X

i2c = board.I2C()

xshut = [
    DigitalInOut(board.D17),
    DigitalInOut(board.D27),
    DigitalInOut(board.D22)
]

for power_pin in xshut:
    power_pin.switch_to_output(value=False)

vl53 = []

for i, power_pin in enumerate(xshut):
    power_pin.value = True
    vl53.insert(i, VL53L0X(i2c))
    vl53[i].start_continous()
    if i < len(xshut) - 1:
        vl53[i].set_address(i + 0x30)

def detect_range(count=5):
    """take count=5 samples"""
    while count:
        for index, sensor in enumerate(vl53):
            print("Sensor {} Range: {}mm".format(index + 1, sensor.range))
        time.sleep(1.0)
        count -= 1

# def stop_continuous():
#     """this is not required, if you use XSHUT to reset the sensor.
#     unless if you want to save some energy
#     """
#     for sensor in vl53:
#         sensor.stop_continuous()
