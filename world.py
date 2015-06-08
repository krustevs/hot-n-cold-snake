from mcpi import minecraft
from mcpi.vec3 import Vec3

class World():

    def __init__(self):
        self.mc = minecraft.Minecraft.create()
        self.mc.postToChat("Hello!")
        self.apple = None

    def get_snake_pos(self):
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

if __name__ == '__main__':
    w = World()