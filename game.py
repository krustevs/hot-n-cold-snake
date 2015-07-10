import threading, time
from math import floor
from random import randint
from mcpi.vec3 import Vec3

from world import World
from rgb_led import RgbLed


class Game:
    def __init__(self):
        self.world = World()
        self.led = RgbLed(16,12,11)
        self.alive = False

        self.generate_random_apple()
        self.led.turn_on()
        self.led.set((0,0,0))

        self.world.post("Hello!")
        self.start()

    def start(self):
        self.alive = True
        def thread_loop():
            while self.alive:
                time.sleep(0.05)
                self.loop()

        t = threading.Thread(target=thread_loop)
        t.setDaemon(True)
        t.start()

    def loop(self):
        if not self.alive:
            return

        if self.world.check_collision():
            self.world.post("You Lost!")
            game.quit()
            return

        distance = self.calculate_distance()
        self.display_distance(distance)
        sqrDist = distance.lengthSqr()

        if sqrDist < 3:
            self.generate_random_apple()
            self.world.extend_snake()

        self.world.move_snake()       

    def calculate_distance(self):
        snake_pos = self.world.get_player_pos()
        apple_pos = self.world.get_apple_pos()
        return apple_pos - snake_pos

    def display_distance(self, distance):
        color = (
            (100 - floor(abs(distance.x))*2)*1,
            (100 - floor(abs(distance.y))*2)*0.7,
            (100 - floor(abs(distance.z))*2)*0.4,
        )
        self.led.set(color)

    def generate_random_apple(self):
        x = randint(-100, 100)
        z = randint(-100, 100)
        self.world.place_apple(x,z)

    def quit(self):
        game.alive = False
        #time.sleep(0.2)
        self.world.remove_apple()
        self.world.snake.cleanup()
        self.world.post("Goodbye!")
        self.led.cleanup()

if __name__ == '__main__':
    game = Game()

    def exit_handler():
        if game.alive:
            game.quit()

    import atexit
    atexit.register(exit_handler)