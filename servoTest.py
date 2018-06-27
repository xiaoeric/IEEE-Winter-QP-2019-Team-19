#!/usr/bin/env python

import time
import pigpio

pi = pigpio.pi()

servo1 = 17
servo2 = 23

pi.set_servo_pulsewidth(servo1, 1000)
pi.set_servo_pulsewidth(servo2, 1000)
time.sleep(0.5)
pi.set_servo_pulsewidth(servo1, 1500)
pi.set_servo_pulsewidth(servo2, 1500)
time.sleep(0.5)
pi.set_servo_pulsewidth(servo1, 2000)
pi.set_servo_pulsewidth(servo2, 2000)
time.sleep(0.5)
pi.set_servo_pulsewidth(servo1, 1500)
pi.set_servo_pulsewidth(servo2, 1500)
time.sleep(0.5)

pi.set_servo_pulsewidth(servo1, 0)

pi.set_servo_pulsewidth(servo2, 0)



pi.stop()