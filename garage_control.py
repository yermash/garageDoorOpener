#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import datetime
import hashlib

from flask import Flask, request, redirect, url_for, session

# -----------------------
# Flask app configuration
# -----------------------
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.permanent_session_lifetime = datetime.timedelta(days=1500)

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
STORED_HASH = os.environ.get("GARAGE_STORED_HASH")
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

        # Hash the user's input with SHA256 and compare to STORED_HASH
        entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        if entered_hash == STORED_HASH:
            # Mark session as permanent (lasts ~1 year)
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return '''
            <html>
              <head><title>Login</title></head>
              <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; text-align: center;">
                <h1>Wrong password!</h1>
                <p><a href="/login">Try again</a></p>
              </body>
            </html>
            '''
    # If GET, render a simple login form
    return '''
    <html>
      <head><title>Garage Login</title></head>
      <body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh;">
          <h1 style="margin-bottom: 1rem;">Login to Control Garage</h1>
          <form method="POST" style="text-align: center;">
            <p style="margin-bottom: 1rem;">
              <label for="password">Password:</label><br />
              <input type="password" name="password" id="password" style="font-size: 1rem; padding: 0.5rem; width: 200px;" />
            </p>
            <p>
              <input type="submit" value="Login" style="font-size: 1rem; padding: 0.5rem 1rem;" />
            </p>
          </form>
        </div>
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
      <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; text-align: center;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh;">
          <h1>You have been logged out!</h1>
          <p><a href="/login">Log back in</a></p>
        </div>
      </body>
    </html>
    '''

@app.route('/')
@login_required
def index():
    """Main page with a large circular button to toggle the garage door."""
    return '''
    <html>
      <head><title>Garage Control</title></head>
      <body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh;">
          <h1 style="margin-bottom: 2rem;">Garage Door Control</h1>
          <a href="/toggle" style="text-decoration: none;">
            <button style="
              width: 200px;
              height: 200px;
              border-radius: 50%;
              background-color: #4CAF50;
              color: white;
              font-size: 1.2rem;
              border: none;
              cursor: pointer;
            ">
              Open/Close
            </button>
          </a>
          <p style="margin-top: 2rem;">
            <a href="/logout" style="color: #333; text-decoration: none; font-size: 1rem;">Logout</a>
          </p>
        </div>
      </body>
    </html>
    '''

@app.route('/toggle')
@login_required
def toggle():
    """Toggle the relay for 1 second to trigger the garage door opener."""
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print('penis')
    time.sleep(1)
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    return '''
    <html>
      <head><title>Garage Toggled</title></head>
      <body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh;">
          <h1>Garage Door Toggled!</h1>
          <p style="margin-top: 2rem;">
            <a href="/" style="text-decoration: none;">
              <button style="
                padding: 1rem 2rem;
                background-color: #2196F3;
                color: white;
                font-size: 1.2rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
              ">
                Go Back
              </button>
            </a>
          </p>
        </div>
      </body>
    </html>
    '''

# -----------------------
# App runner
# -----------------------
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=6969, debug=False)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
