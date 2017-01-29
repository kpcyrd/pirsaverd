# pirsaverd

Passive infrared screensaver for raspberry pi.

## Start GPIO PIR sensor

The PIR sensor is expected to be present on GPIO 7.

    sudo ./pirsensord.py 'tcp://127.0.0.1:5557'

## Start screensaver

Starts the screensaver server. Expects a message every `$TTL` seconds or the screen is turned off.

    ./pirsaverd.py -d "$DISPLAY" --ttl 60 tcp://127.0.0.1:5557

## Security

There is no encryption and even with encryption, monitoring the traffic is sufficient to tell if there's a person in front of the screen or not. For privacy reasons, use an isolated wired network or bind to localhost only.

Authentication is still todo, so everybody able to connect to the screensaver server is able to turn the screen on.

## License

GPLv3
