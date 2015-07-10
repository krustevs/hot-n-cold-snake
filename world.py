from mcpi import minecraft
from mcpi.vec3 import Vec3
from math import floor
from itertools import product

from snake import Snake

shell = [Vec3(i[0], i[1], i[2]) for i in list(product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]))]

class World():

    def __init__(self):
        self.mc = minecraft.Minecraft.create()
        self.apple = None
        self.snake = Snake(self.mc)

    def get_player_pos(self):
        return self.mc.player.getTilePos()

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
        pos = [floor(axis) for axis in self.get_player_pos()]
        center = Vec3(pos[0], pos[1], pos[2])
        for offset in shell:
            block = center + offset
            if (block.x, block.y, block.z) in list(self.snake.body)[3:]:
                return True
        return False

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