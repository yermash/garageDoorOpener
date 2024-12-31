# Garage Door Opener

This project provides a solution for remotely controlling your garage door using a Raspberry Pi, a relay module, and a web interface accessible via ngrok.

## Features

- **Remote Control**: Operate your garage door from any device with internet access.
- **Web Interface**: User-friendly web page with large, mobile-friendly buttons for easy operation.
- **Secure Access**: Password-protected interface with SHA-256 hashed password verification.
- **Session Management**: Sessions last up to 1000 days, reducing the need for frequent logins.

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

## Setup Instructions

1. **Hardware Setup**:
   - Connect the relay module to the Raspberry Pi:
     - VCC to 5V
     - GND to Ground
     - IN1 to GPIO 18
   - Connect the relay's output to the garage door opener's manual switch terminals.

2. **Software Setup**:
   - Clone this repository to your Raspberry Pi.
   - Install the required Python libraries:
     ```bash
     sudo apt-get update
     sudo apt-get install python3-flask python3-rpi.gpio
     ```
   - Ensure ngrok is installed and authenticated on your Raspberry Pi.

3. **Configuration**:
   - Update the `STORED_HASH` variable in `garage_control.py` with the SHA-256 hash of your desired password.
   - Set up ngrok to forward HTTP traffic to port 80:
     ```bash
     ngrok http 80
     ```
   - Note the ngrok URL provided; this will be used to access the web interface.

4. **Running the Application**:
   - Execute the `garage_control.py` script with superuser privileges to allow access to GPIO and port 80:
     ```bash
     sudo python3 garage_control.py
     ```
   - Access the web interface via the ngrok URL.

## Security Considerations

- Ensure your ngrok URL is kept private to prevent unauthorized access.
- Regularly update your password and the corresponding SHA-256 hash in the script.
- Consider implementing additional security measures, such as IP whitelisting or two-factor authentication.

## Troubleshooting

- **GPIO Issues**: If the relay does not respond, verify the GPIO pin configuration and ensure the RPi.GPIO library is functioning correctly.
- **Port Conflicts**: If you encounter a "Port already in use" error, ensure no other services (e.g., nginx) are occupying port 80.
- **ngrok Connectivity**: If ngrok fails to establish a tunnel, check your internet connection and ngrok account status.

## License

This project is licensed under the MIT License.
