from collections import deque
from math import floor


class Snake:
    def __init__(self, mc):
        self.mc = mc
        self.body = deque()
        self.head_pos = None
        self.to_extend = None
        self.extend_size = 25
        self.extend()

    def update(self, new_pos):
        if self.head_pos != new_pos:
            self.move(self.head_pos)
        self.head_pos = new_pos

    def move(self, new_pos):
        if not new_pos:
            return

        self.body.appendleft(new_pos)
        self.mc.setBlock(new_pos[0], new_pos[1], new_pos[2], 35, 13)
        if (self.to_extend > 0):
            self.to_extend -= 1
        else:
            tail = self.body.pop()
            self.mc.setBlock(tail[0], tail[1], tail[2], 0)

    def extend(self):
        self.to_extend = self.extend_size
        self.extend_size = floor(self.extend_size * 1.5)

    def get_head_pos(self):
        if len(self.body) > 0:
            return tuple([floor(i) for i in self.body[0]])

    def cleanup(self):
        for node in self.body:
            self.mc.setBlock(node[0], node[1], node[2], 0)
