import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize variables
button_pressed_count = 0
button_last_state = False
daemon_running = False

def debounce(channel):
    reading = GPIO.input(channel)
    time.sleep(0.05)
    reading = GPIO.input(channel)
    return reading

while True:
    # check for button press
    button_current_state = GPIO.input(4)

    if button_current_state != button_last_state:
        if button_current_state == False:
            if debounce(4) == GPIO.LOW:
                button_pressed_count += 1
                print("Button pressed {} times".format(button_pressed_count))

                # if button pressed 3 times, run the CLI command
                if button_pressed_count == 3:
                    print("Running edge-impulse-daemon command...")
                    subprocess.Popen(["edge-impulse-daemon"])
                    daemon_running = True
                    button_pressed_count = 0
                
        button_last_state = button_current_state
    else:
        print("Button not pressed")

    # check for single button press
    if button_pressed_count == 1 and daemon_running:
        if debounce(4) == GPIO.LOW:
            print("Running SendData.py command...")
            subprocess.call(["python3", "SendData.py"])
            button_pressed_count = 0

    # add a small delay to avoid high CPU usage
    time.sleep(0.1)