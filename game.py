import threading, time, math
from random import randint
from mcpi.vec3 import Vec3

from world import World
from rgb_led import RgbLed


class Game:
    def __init__(self):
        self.world = World()
        self.led = RgbLed(16,12,11)
        
        snake_pos = self.world.get_snake_pos()
        self.generate_random_apple()
        self.led.turn_on()
        self.led.set((0,0,0))

        self.start()

    def start(self):
        def thread_loop():
            while True:
                time.sleep(0.1)
                self.loop()

        t = threading.Thread(target=thread_loop)
        t.setDaemon(True)
        t.start()

    def loop(self):
        distance = self.calculate_distance()
        self.display_distance(distance)
        sqrDist = distance.lengthSqr()
        #print (sqrDist)
        if sqrDist < 3:
            self.generate_random_apple()


    def calculate_distance(self):
        snake_pos = self.world.get_snake_pos()
        apple_pos = self.world.get_apple_pos()
        return apple_pos - snake_pos

    def display_distance(self, distance):
        color = (
            (100 - math.floor(abs(distance.x))*2)*1,
            (100 - math.floor(abs(distance.y))*2)*0.7,
            (100 - math.floor(abs(distance.z))*2)*0.4,
        )
        self.led.set(color)

    def generate_random_apple(self):
        x = randint(-100, 100)
        z = randint(-100, 100)
        self.world.place_apple(x,z)

if __name__ == '__main__':
    g = Game()

    def exit_handler():
        g.world.remove_apple()
        g.led.cleanup()
        print('Goodbye!')

    import atexit
    atexit.register(exit_handler)