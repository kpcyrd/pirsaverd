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


class Remote(object):
    def __init__(self, addr):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(addr)

    def notify(self):
        self.socket.send_json({'txt': 'ohai'})


def main(remotes):
    remotes = [Remote(x) for x in remotes]

    log('PIR Module test (^C to exit)')
    time.sleep(2)
    log('ready')

    try:
        while True:
            if GPIO.input(PIR_PIN):
                for remote in remotes:
                    remote.notify()
            time.sleep(1)
    except:
        log(' quit')
        GPIO.cleanup()


if __name__ == '__main__':
    remotes = sys.argv[1:]
    main(remotes)
