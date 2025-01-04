# Garage Door Opener
A simple solution to remotely control your garage door using a Raspberry Pi, a relay module, and a Flask web interface—secured via SHA-256 password hashing. With ngrok, you can safely tunnel your local service to the internet and access it from anywhere.

## Service Daemons
Systemd service files are included for both the Flask app and ngrok, allowing them to start on boot without manual intervention. This ensures uninterrupted operation and makes the solution more robust.

For detailed setup instructions, configuration examples, and service daemon installation steps, please refer to the repository’s documentation.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- 5V Relay Module
- Jumper wires
- Stable internet connection

## Software Requirements

- Python 3
- Flask
- RPi.GPIO library
- ngrok
