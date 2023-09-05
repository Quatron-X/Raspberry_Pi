import time
import board
from digitalio import DigitalInOut as DigIO
import adafruit_vl53l1x as tof

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

xshut = [
    # Update the D6 and D5 pins to match the pins to which you wired your sensor XSHUT pins.
    DigIO(board.D6),
    DigIO(board.D5),
    # Add more VL53L1X sensors by defining their XSHUT pins here.
]

for shutdown_pin in xshut:
    shutdown_pin.switch_to_output(value=False)

vl53l1x = []

for pin_number, shutdown_pin in enumerate(xshut):
    shutdown_pin.value = True
    sensor_i2c = tof.VL53L1X(i2c)
    vl53l1x.append(sensor_i2c)
    if pin_number < len(xshut) - 1:
        sensor_i2c.set_address(pin_number + 0x30)

# Start ranging for sensor data collection.
for sensor in vl53l1x:
    sensor.start_ranging()
for sensor_number, sensor in enumerate(vl53l1x):
    if sensor.data_ready:
        print("Sensor {}: {}".format(sensor_number + 1, sensor.distance))
        sensor.clear_interrupt()
    time.sleep(0.5)

# Print the various sensor I2C addresses to the serial console.
def i2c_scan():
    if i2c.try_lock():
        print("Sensor I2C addresses:", [hex(x) for x in i2c.scan()])
        i2c.unlock()
