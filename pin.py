import RPi.GPIO as GPIO

class Pin:
    def __init__(self, number):
        self.number = number
        self.on = False

        GPIO.setup(number, GPIO.OUT)
        GPIO.output(self.number, 0)

        self._value = 100
        self._pwm = GPIO.PWM(number, 200)
        self._pwm.start(0)

    def turn_on(self):
        if not self.on:
            self._pwm.ChangeDutyCycle(self._value)
            self.on = True

    def turn_off(self):
        if self.on:
            self._pwm.ChangeDutyCycle(0)
            self.on = False

    def set(self, value):
        if value > 100:
            value = 100
        if value < 0:
            value = 0
        self._value = value
        self.on = True
        self._pwm.ChangeDutyCycle(self._value)

    def cleanup(self):
        self.on = False
        self._pwm.stop()
        GPIO.output(self.number, 0)
