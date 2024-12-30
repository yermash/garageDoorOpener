#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import datetime

from flask import Flask, request, redirect, url_for, render_template_string, session
import requests

url = "https://e988-2607-fb90-ddd9-326-00-4efd.ngrok-free.app/"
headers = {
    "ngrok-skip-browser-warning": "anyvalue"  # or "1"
}
response = requests.get(url, headers=headers)
print(response.text)

# https://9905-2607-fb90-ddd9-326-00-4efd.ngrok-free.app/
# -----------------------
# Flask app configuration
# -----------------------
app = Flask(__name__)

# Make sure this secret key is set to something unique and random in production!
app.secret_key = "CHANGE_ME_TO_SOMETHING_SECURE"

# Sets the Flask session to be "permanent," so it can last longer than just browser close
app.permanent_session_lifetime = datetime.timedelta(days=365)  # 1 year

# -----------------------
# GPIO setup
# -----------------------
RELAY_PIN = 18  # BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)
# Note: Many relay modules are "active-low," so GPIO.LOW might trigger the relay.

# -----------------------
# Configuration
# -----------------------
PASSWORD = "garage123"  # CHANGE THIS!

# -----------------------
# Helper function
# -----------------------
def login_required(f):
    """Decorator that checks if the user is logged in; otherwise, redirect to /login."""
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  # Preserve function name for Flask
    return wrapper

# -----------------------
# Routes
# -----------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login form. Once the correct password is entered, store session cookie for 1 year."""
    if request.method == 'POST':
        entered_password = request.form.get('password', '')
        if entered_password == PASSWORD:
            # Mark session as permanent (lasts 1 year)
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return '''
            <html>
              <head><title>Login</title></head>
              <body>
                <h1>Wrong password!</h1>
                <p><a href="/login">Try again</a></p>
              </body>
            </html>
            '''
    # If GET, render a simple login form
    return '''
    <html>
      <head><title>Garage Login</title></head>
      <body>
        <h1>Login to Control Garage</h1>
        <form method="POST">
          <p>Password: <input type="password" name="password" /></p>
          <p><input type="submit" value="Login" /></p>
        </form>
      </body>
    </html>
    '''

@app.route('/logout')
def logout():
    """Optional logout route to clear session early if you want."""
    session.clear()
    return '''
    <html>
      <head><title>Logged Out</title></head>
      <body>
        <h1>You have been logged out!</h1>
        <p><a href="/login">Log back in</a></p>
      </body>
    </html>
    '''

@app.route('/')
@login_required
def index():
    """Main page with a button to toggle the garage door."""
    return '''
    <html>
      <head><title>Garage Control</title></head>
      <body>
        <h1>Garage Door Control</h1>
        <p><a href="/toggle"><button>Open/Close Garage</button></a></p>
        <p><a href="/logout">Logout</a></p>
      </body>
    </html>
    '''

@app.route('/toggle')
@login_required
def toggle():
    """Toggle the relay for 1 second to trigger the garage door opener."""
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(1)
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

# -----------------------
# App runner
# -----------------------
if __name__ == '__main__':
    try:
        # If you want to run on port 80, you may need sudo (on Linux).
        # Alternatively, run on a higher port if you prefer not to use sudo.
        app.run(host='0.0.0.0', port=80, debug=False)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
