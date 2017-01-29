#!/usr/bin/env python3
import argparse
import subprocess
import zmq
import sys
import os


class Screen(object):
    def __init__(self, display, dry=False):
        self.display = display
        self.dry = dry

    def turnon(self):
        if not self.dry:
            self.run(['xset', 'dpms', 'force', 'on'])
            self.run(['xset', '-dpms'])

    def turnoff(self):
        if not self.dry:
            self.run(['xset', 'dpms', 'force', 'off'])
            self.run(['xset', '+dpms'])

    def run(self, cmd):
        env = dict(os.environ, DISPLAY=self.display)
        try:
            subprocess.check_call(cmd, env=env)
        except subprocess.CalledProcessError:
            pass


class Logger(object):
    def __init__(self, remote=None):
        self.remote = remote

    def log(self, txt):
        print(txt)
        if not self.remote:
            return

        ctx = zmq.Context()
        sock = ctx.socket(zmq.PUSH)
        sock.connect(self.remote)

        sock.send_json({
            'op': 'log',
            'data': txt
        })


def server(addr, ttl):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(addr)

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    while True:
        evts = poller.poll(ttl * 1000)
        yield [sock.recv() for sock, _ in evts]


def main(args):
    screen = Screen(args.display, args.dry)
    logger = Logger(args.log)

    is_on = True
    screen.turnon()

    for evts in server(args.bind, args.ttl):
        if evts:
            screen.turnon()
            if not is_on:
                logger.log('screen on')
            is_on = True
        else:
            if is_on:
                screen.turnoff()
                logger.log('screen off')
                is_on = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bind', help='(tcp://127.0.0.1:5557)')
    parser.add_argument('-n', '--dry', action='store_true', help='dry run')
    parser.add_argument('-t', '--ttl', type=int, default=60, help='shutdown screen after X seconds of silence')
    parser.add_argument('-l', '--log', help='zmq socket for logging')
    parser.add_argument('-d', '--display', default=':0', help='control display (default :0)')
    args = parser.parse_args()

    main(args)
