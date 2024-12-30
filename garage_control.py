#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from flask import Flask, request, render_template_string

# --- Flask app setup ---
app = Flask(__name__)

# --- GPIO setup ---
RELAY_PIN = 18  # BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)  
# Depending on relay module, "HIGH" might mean "off" and "LOW" means "on"

@app.route('/')
def index():
    # Simple page with a button to toggle the garage
    return '''
    <html>
      <head><title>Garage Control</title></head>
      <body>
        <h1>Garage Door Control</h1>
        <p><a href="/toggle"><button>Open/Close Garage</button></a></p>
      </body>
    </html>
    '''

@app.route('/toggle', methods=['GET'])
def toggle():
    # Pull the relay pin low for a short time to toggle the door
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(1)  # Adjust the time as needed
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    return '''
    <html>
      <head><title>Garage Toggled</title></head>
      <body>
        <h1>Garage Door Toggled!</h1>
        <p><a href="/">Go back</a></p>
      </body>
    </html>
    '''

if __name__ == '__main__':
    try:
        # Running on port 80 requires root or running via sudo.
        # Alternatively, choose a higher port number like 5000 or 8080.
        app.run(host='0.0.0.0', port=80, debug=False)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
