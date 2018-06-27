#!/usr/bin/env python

import time
import pigpio

pi = pigpio.pi()

servo1 = 17
servo2 = 23

pi.set_servo_pulsewidth(servo2, 500)

pi.set_servo_pulsewidth(servo2, 0)

pi.stop()