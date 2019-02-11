#!/usr/bin/env python

import smbus
from time import sleep
import pigpio

# MPU hex id things
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

SERVO_CENTER = 1500


class Servo:
    def __init__(self, rasp_pi, pin_number):
        self.rasp_pi = rasp_pi
        self.pin_number = pin_number

    def set_pulse_width(self, pulse_width):
        self.rasp_pi.set_servo_pulsewidth(self.pin_number, pulse_width)


# Servo pin numbers
servo1_pin = 23
servo2_pin = 17

# Variable to store raspberry pi
pi_local = None

# Variables to store servo objects
servo1 = servo2 = None

# Variables to store values from mpu
accelX = accelY = accelZ = None
gForceX = gForceY = gForceZ = None

gyroX = gyroY = gyroZ = None
rotX = rotY = rotZ = None
gyroX_cal = gyroY_cal = gyroZ_cal = None
angle_pitch = angle_roll = None
angle_roll_acc = angle_pitch_acc = None
angle_pitch_output = angle_roll_output = None
acc_calibration_value = 1000 # Enter the accelerometer calibration value
angle_acc = None

loop_timer = None
servoXpos = 90
servoYpos = 90
count = 0


def init_mpu():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    bus.write_byte_data(Device_Address, CONFIG, 0)

    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def setup():
    global pi_local, servo1, servo2

    pi_local = pigpio.pi()

    servo1 = Servo(pi_local, servo1_pin)
    servo2 = Servo(pi_local, servo2_pin)

    servo1.set_pulse_width(SERVO_CENTER)
    servo2.set_pulse_width(SERVO_CENTER)

    init_mpu()


bus = smbus.SMBus(1)
Device_Address = 0x68

setup()

while True:
    value = bus.read_byte_data(Device_Address, ACCEL_XOUT_H)
    value = value / 65.0 * 1000 + 500

    print(value)

    if 500 <= value <= 1500:
        servo1.set_servo_pulse_width(value)
    elif value > 3000:
        servo1.set_servo_pulse_width(500)

    sleep(0.08)
