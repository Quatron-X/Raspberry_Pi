import time
import board
from digitalio import DigitalInOut as DigIO
from adafruit_vl53l0x import untof

i2c = board.I2C()

xshut = [
    DigIO(board.D17),
    DigIO(board.D27),
    DigIO(board.D22)
]

for power_pin in xshut:
    power_pin.switch_to_output(value=False)

vl53l0x = []

for i, power_pin in enumerate(xshut):
    power_pin.value = True
    vl53l0x.insert(i, untof(i2c))
    vl53l0x[i].start_continous()
    if i < len(xshut) - 1:
        vl53l0x[i].set_address(i + 0x30)

def detect_range(count=5):
    """take count=5 samples"""
    while count:
        for index, sensor in enumerate(vl53l0x):
            print("Sensor {} Range: {}mm".format(index + 1, sensor.range))
        time.sleep(1.0)
        count -= 1

# def stop_continuous():
#     """this is not required, if you use XSHUT to reset the sensor.
#     unless if you want to save some energy
#     """
#     for sensor in vl53:
#         sensor.stop_continuous()
