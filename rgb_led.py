import time, threading
from random import randint

import RPi.GPIO as GPIO

from pin import Pin

class RgbLed:

    def __init__(self, red, green, blue):
        GPIO.setmode(GPIO.BOARD)
        self.pins = {
            'red': Pin(red),
            'green': Pin(green),
            'blue': Pin(blue)
        }

    def turn_on(self):
        for pin in self.pins.values():
            pin.turn_on()

    def turn_off(self):
        for pin in self.pins.values():
            pin.turn_off()

    def set(self, color):
        if not self.on():
            return
        color = tuple(color)

        self.pins['red'].set(color[0])
        self.pins['green'].set(color[1])
        self.pins['blue'].set(color[2])

    def color(self):
        return (
            self.pins['red']._value,
            self.pins['green']._value,
            self.pins['blue']._value
        )

    def on(self):
        return (self.pins['red'].on or
           self.pins['green'].on or
           self.pins['blue'].on)

    def cleanup(self):
        for pin in self.pins.values():
            pin.cleanup()
        GPIO.cleanup()

    def __getitem__(self, key):
        return self.pins[key]
    def __iter__(self):
        for pin in self.pins.values():
            yield self.pins[key]



if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    led = RgbLed(12,11,16)
    import atexit
    atexit.register(exit_handler, led)
    print('Hello!')


def exit_handler(led):
    print('Goodbye!')
    led.cleanup()
    GPIO.cleanup()

