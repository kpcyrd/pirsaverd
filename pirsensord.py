#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import zmq
import sys

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)


def log(x):
    print(x, file=sys.stderr, flush=True)


def signal_motion(remote):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect(remote)
    socket.send_json({'txt': 'ohai'})
    socket.close()


def main(remotes):
    log('PIR Module test (^C to exit)')
    time.sleep(2)
    log('ready')

    try:
        while True:
            if GPIO.input(PIR_PIN):
                for remote in remotes:
                    signal_motion(remote)
            time.sleep(1)
    except:
        log(' quit')
        GPIO.cleanup()


if __name__ == '__main__':
    remotes = sys.argv[1:]
    main(remotes)
