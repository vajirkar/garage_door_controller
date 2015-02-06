import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
import time

CLOSED = 0
OPEN = 1
door_switch_pin = 3
door_state = CLOSED 
notstamped = timedelta(days=-100)
door_open_since = notstamped
warn_if_open_for_secs = 10
notification_sent = False


def send_email_notification():
    

def send_notification():
    global notification_sent
    if notification_sent == False:
        ''' send notification '''
        notification_sent = True
        send_email_notification()
        '''send_sms_notification()'''
        '''send_tweet_notification()'''

def print_door_state():
    if door_state == OPEN:
        print "%s Door Opened." % datetime.now()
    else:
        print "%s Door Closed." % datetime.now()

def update_timestamp():
    global notification_sent
    global door_open_since
    if door_state == OPEN:
        if door_open_since == notstamped:
            door_open_since = datetime.now()
        else:
            if datetime.now() - door_open_since > timedelta(seconds=warn_if_open_for_secs):
                print "Sending notification ... %s." % datetime.now()
                send_notification()

    if door_state == CLOSED:
        door_open_since = notstamped
        notification_sent = False

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(door_switch_pin, GPIO.IN)
    door_state = GPIO.input(door_switch_pin)
    print_door_state()
    ''' Setup the timestamp correctly upon startup, door could be open or closed '''
    update_timestamp()
    while True:
        polled_door_state = GPIO.input(door_switch_pin)
        ''' If door changed state, then update timestamp '''
        if door_state != polled_door_state:
            door_state = polled_door_state
            print_door_state()
            update_timestamp()
            ''' If door is open, then check for how long '''
        elif door_state == OPEN:
            update_timestamp()

        time.sleep(1)
