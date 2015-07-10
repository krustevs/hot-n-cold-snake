from mcpi import minecraft
from mcpi.vec3 import Vec3
from math import floor

from snake import Snake

class World():

    def __init__(self):
        self.mc = minecraft.Minecraft.create()
        self.apple = None
        self.snake = Snake(self.mc)

    def get_player_pos(self):
        return self.mc.player.getPos()

    def get_apple_pos(self):
        return self.apple

    def place_apple(self, x, z):
        self.remove_apple()
        y = self.mc.getHeight(x,z)
        self.mc.setBlock(x, y, z, 35, 14)
        self.apple = Vec3(x,y,z)

    def remove_apple(self):
        if self.apple is None:
            return

        self.mc.setBlock(self.apple.x, self.apple.y, self.apple.z, 0)
        self.apple = None

    def check_collision(self):
        collision = self.get_player_pos()# + self.mc.player.getDirection()
        pos = [floor(axis) for axis in collision]
        return (pos[0], pos[1], pos[2]) in self.snake.body

    def move_snake(self):
        new_pos = self.get_player_pos()
        new_pos = tuple([floor(i) for i in new_pos])
        self.snake.update(new_pos)

    def extend_snake(self):
        self.snake.extend()

    def post(self, message):
        self.mc.postToChat(message)
        print(message)

if __name__ == '__main__':
    w = World()