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

        self.shuffling = False
        self.blinking = False

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

    def _blend(self, color, blend_time):
        step_length = 20
        steps = blend_time // step_length
        deltas = (
            (color[0] - self.pins['red']._value)/steps,
            (color[1] - self.pins['green']._value)/steps,
            (color[2] - self.pins['blue']._value)/steps,
        )
        for step in range(0, steps):
            self.set((
                self.pins['red']._value + deltas[0],
                self.pins['green']._value + deltas[1],
                self.pins['blue']._value + deltas[2],
            ))
            time.sleep(step_length/1000)
        self.set(color)

    def blend(self, color, blend_time):
        args = color, blend_time
        t = threading.Thread(target=self._blend, args=args)
        t.start()

    def blink(self, bpm, coef):
        t = threading.Thread(target=self._blink, args=(bpm, coef))
        t.start()

    def _blink(self, bpm, coef):
        self.blinking = True
        timeframe = 60/bpm
        time_on = timeframe*coef
        while self.blinking:
            self.turn_on()
            time.sleep(time_on)
            if self.blinking:
                self.turn_off()
                time.sleep(timeframe - time_on)

    def stop_blink(self):
        self.blinking = False

    def shuffle(self, interval, blend_time):
        args = interval, blend_time
        t = threading.Thread(target=self._shuffle, args=args)
        t.start()

    def _shuffle(self, interval, blend_time):
        self.shuffling = True

        while self.shuffling:
            colors = [1,1,1]
            colors[randint(0,2)] = 0
            color = (
                randint(0, 100) * 1   * colors[0],
                randint(0, 100) * 0.7 * colors[1],
                randint(0, 100) * 0.5 * colors[2],
            )
            self.blend(color, blend_time)
            time.sleep(interval)

    def stop_shuffle(self):
        self.shuffling = False

    def cleanup(self):
        if self.shuffling:
            self.stop_shuffle()
        if self.blinking:
            self.stop_blink()
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

