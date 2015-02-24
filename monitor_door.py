import sys
import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
import time
import send_email as send_email

CLOSED = 0
OPEN = 1
door1_switch_pin = 3
door2_switch_pin = 5
door_state = CLOSED 
notstamped = timedelta(days=-100)
door_open_since = notstamped
poll_freq_secs = 1
warn_if_open_for_secs = 10
repeat_notification_secs = 30
notification_sent = False
send_closed_notification = True
last_notification = notstamped
last_heartbeat = notstamped
heartbeat_freq_hours = 24 
heartbeat_freq_hours_ = heartbeat_freq_hours
heartbeat_reattempt_freq_hours = 1
heartbeat_send_failures = 0

def send_notification():
    global notification_sent
    global last_notification
    email_subject = "Garage Door Open Notification!"
    if notification_sent == False:
        last_notification = datetime.now()
        ''' send notification '''
        notification_sent = True
        msg = "Garage door open since " + door_open_since.strftime("%-I:%M%P %B %d, %Y") + "."
        msg = msg + " Time now " + datetime.now().strftime("%-I:%M%P %B %d, %Y") + "."
	try:
            print "Sending notification ... %s." % datetime.now()
            send_email.send_email_notification(email_subject, msg)
        except:
            ''' Ignore for now, re-notification will be sent '''
            print "send_email error... will re-notify later."
        '''send_sms_notification()'''
        '''send_tweet_notification()'''
    elif datetime.now() - last_notification > timedelta(seconds=repeat_notification_secs):
        last_notification = datetime.now()
        print "Sending repeat notification ... %s." % last_notification
        msg = "Garage door open since " + door_open_since.strftime("%-I:%M%P %B %d, %Y") + "."
        msg = msg + " Time now " + datetime.now().strftime("%-I:%M%P %B %d, %Y") + "."
        try:
            send_email.send_email_notification(email_subject, msg)
        except:
            ''' Ignore for now, re-notification will be sent '''
            print "send_email error, re-notification failed... will re-notify later."
        
def send_closed_notification():
    msg = "Garage doors now closed at " + datetime.now().strftime("%-I:%M%P %B %d, %Y") + "."
    try:
        send_email.send_email_notification("Garage Door Closed Notification.", msg)
    except:
        ''' Ignore for now. Closed notification failures not to be re-sent. '''
        print "send_email error, door closed notification not sent. Will not retry."

def send_heartbeat():
    global last_heartbeat

    msg = datetime.now().strftime("%-I:%M%P %B %d, %Y") +  " - Garage door monitor: All systems nominal. Heartbeat send failures = " + str(heartbeat_send_failures) + "."
    try:
        send_email.send_email_notification("Garage Door Monitor Status.", msg)
        last_heartbeat = datetime.now()
        heartbeat_freq_hours = heartbeat_freq_hours_
        heartbeat_send_failures = 0
    except:
        ''' Ignore for now, re-notification will be sent '''
        print "send_email error, heartbeat failed... will heartbeat later."
        heartbeat_freq_hours = heartbeat_reattempt_freq_hours
        heartbeat_send_failures = heartbeat_send_failures + 1

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
                send_notification()

    if door_state == CLOSED:
        if notification_sent and send_closed_notification:
            send_closed_notification()
        door_open_since = notstamped
        notification_sent = False
        last_notification = notstamped

if __name__ == '__main__':
    sys.path.append("/home/pi/gdc_settings")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(door1_switch_pin, GPIO.IN)
    GPIO.setup(door2_switch_pin, GPIO.IN)
    door_state = GPIO.input(door1_switch_pin) | GPIO.input(door2_switch_pin)
    print_door_state()
    ''' Setup the timestamp correctly upon startup, door could be open or closed '''
    update_timestamp()
    last_heartbeat = datetime.now()
    try:
        while True:
            polled_door_state = GPIO.input(door1_switch_pin) | GPIO.input(door2_switch_pin)
            ''' If door changed state, then update timestamp '''
            if door_state != polled_door_state:
                door_state = polled_door_state
                print_door_state()
                update_timestamp()
                ''' If door is open, then check for how long '''
            elif door_state == OPEN:
                update_timestamp()

            if datetime.now() - last_heartbeat > timedelta(hours=heartbeat_freq_hours):
                send_heartbeat()
            time.sleep(poll_freq_secs)
    except KeyboardInterrupt:
        print "Stopped by user."

    except:
        print "Exiting, some exception occurred."

    finally:
        GPIO.cleanup() # This ensures a clean exit.
