#!/usr/bin/env python

import smbus
from time import sleep
import pigpio
import math

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

    def set_angle(self, angle):
        self.set_pulse_width(map_range(angle, 0, 180, 500, 2500))


# Servo pin numbers
servoX_pin = 23
servoY_pin = 17

# Variable to store raspberry pi
pi_local = None

# Variables to store servo objects
servoX = servoY = None

# Variables to store values from mpu
accelX = accelY = accelZ = 0
gForceX = gForceY = gForceZ = 0

gyroX = gyroY = gyroZ = 0
rotX = rotY = rotZ = 0
gyroX_cal = gyroY_cal = gyroZ_cal = 0
angle_pitch = angle_roll = 0
angle_roll_acc = angle_pitch_acc = 0
angle_pitch_output = angle_roll_output = 0
acc_calibration_value = 1000 # Enter the accelerometer calibration value
angle_acc = 0

loop_timer = 0
servoXpos = 90
servoYpos = 90
count = 0


def init_mpu():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    bus.write_byte_data(Device_Address, CONFIG, 0)

    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def record_gyro_registers():
    global gyroX, gyroY, gyroZ
    gyroX = bus.read_byte_data(Device_Address, GYRO_XOUT_H)
    gyroY = bus.read_byte_data(Device_Address, GYRO_YOUT_H)
    gyroZ = bus.read_byte_data(Device_Address, GYRO_ZOUT_H)


def record_accel_registers():
    global accelX, accelY, accelZ
    accelX = bus.read_byte_data(Device_Address, ACCEL_XOUT_H)
    accelY = bus.read_byte_data(Device_Address, ACCEL_YOUT_H)
    accelZ = bus.read_byte_data(Device_Address, ACCEL_ZOUT_H)


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def micros():
    # TODO: return time since program started in microseconds
    return 0


def setup():
    global pi_local, servoX, servoY, gyroX_cal, gyroY_cal, gyroZ_cal, loop_timer

    pi_local = pigpio.pi()

    servoX = Servo(pi_local, servoX_pin)
    servoY = Servo(pi_local, servoY_pin)

    servoX.set_pulse_width(SERVO_CENTER)
    servoY.set_pulse_width(SERVO_CENTER)

    init_mpu()

    print("Calibrating MPU...", end="")

    for i in range(0, 2000):
        if i % 125 == 0:
            print(".", end="")
        record_gyro_registers()
        gyroX_cal += gyroX
        gyroY_cal += gyroY
        gyroZ_cal += gyroZ
        sleep(0.0037)
    print()

    gyroX_cal /= 2000
    gyroY_cal /= 2000
    gyroZ_cal /= 2000

    print(f"gyroX_cal:{gyroX_cal:10d}   gyroY_cal:{gyroY_cal:10d}   gyroZ_cal:{gyroZ_cal:10d}")

    loop_timer = micros()


def loop():
    global gyroX, gyroY, gyroZ, angle_pitch, angle_roll, servoXpos, servoYpos, count, loop_timer, servoX

    record_accel_registers()
    record_gyro_registers()

    gyroX -= gyroX_cal
    gyroY -= gyroY_cal
    gyroZ -= gyroZ_cal

    angle_pitch += gyroX * 0.000122
    angle_roll += gyroY * 0.000122

    # TODO: check whether python sine function is in radians or degrees
    angle_pitch += angle_roll * math.sin(gyroZ * 0.000002131)
    angle_roll += angle_pitch * math.sin(gyroZ * 0.000002131)

    servoXpos = map_range(angle_roll, 90.00, -90.00, 0, 180)
    servoYpos = map_range(angle_pitch, -90.00, 90.00, 0, 180)

    count += 1
    while micros() - loop_timer < 8000:
        if count == 1:
            if 0 <= servoXpos <= 180:
                servoX.set_angle(servoXpos)
        if count == 2:
            count = 0
            if 0 <= servoYpos <= 180:
                servoY.set_angle(servoYpos)

    loop_timer += 8000


bus = smbus.SMBus(1)
Device_Address = 0x68

setup()

while True:
    loop()
