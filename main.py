#!/usr/bin/env python

import smbus
from time import sleep
import pigpio

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

pi = pigpio.pi()

servo1 = 23
servo2 = 17


def init_mpu():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    bus.write_byte_data(Device_Address, CONFIG, 0)

    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


bus = smbus.SMBus(1)
Device_Address = 0x68

init_mpu()

while True:
    value = bus.read_byte_data(Device_Address, ACCEL_XOUT_H)
    value = value / 65.0 * 1000 + 500

    print(value)

    if 500 <= value <= 1500:
        pi.set_servo_pulsewidth(servo1, value)
    elif value > 3000:
        pi.set_servo_pulsewidth(servo1, 500)

    sleep(0.08)
