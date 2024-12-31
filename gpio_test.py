#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# --- Pin Assignments ---
# Feel free to change these if you want different pins.
IN1_PIN = 18
IN2_PIN = 23  # Optional second relay channel

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN2_PIN, GPIO.OUT, initial=GPIO.HIGH)

print("Relay test starting...")

try:
    while True:
        # Toggle IN1
        GPIO.output(IN1_PIN, GPIO.LOW)  # Many relays are active LOW
        print("IN1 -> LOW (relay on?)")
        time.sleep(1)

        GPIO.output(IN1_PIN, GPIO.HIGH)
        print("IN1 -> HIGH (relay off?)")
        time.sleep(1)

        # Toggle IN2
        GPIO.output(IN2_PIN, GPIO.LOW)
        print("IN2 -> LOW (relay on?)")
        time.sleep(1)

        GPIO.output(IN2_PIN, GPIO.HIGH)
        print("IN2 -> HIGH (relay off?)")
        time.sleep(1)

except KeyboardInterrupt:
    print("Test interrupted by user.")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Test finished.")