import gui
import serial
import time

HEATER_PIN = 4
LIGHT_PIN = 5

def USING_PI():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

if USING_PI():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HEATER_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_PIN, GPIO.OUT)
    GPIO.output(LIGHT_PIN, GPIO.LOW)
else:
    GPIO = ''

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
arduino.reset_input_buffer()

light_mode = 0

def update(app):
    if arduino.in_waiting > 0 and int(time.time()) % 5 == 0:
            data = arduino.readline().decode('utf-8').rstrip()
            update_tuple = app.data.process_next_data(data)
            app.update(update_tuple)
    app.after(1000, lambda app=app: update(app))



def main():
    app_gui = gui.Main_GUI()
    update(app_gui)
    app_gui.run()

if __name__ == "__main__":
    main()

