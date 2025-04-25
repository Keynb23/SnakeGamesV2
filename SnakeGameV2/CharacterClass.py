import random
from GameConstants import *

class Snake:
    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.length = 3

    def move(self, direction):
        head_x, head_y = self.body[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)
        self.length += 1

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        max_x = SCREEN_WIDTH // GRID_SIZE
        max_y = SCREEN_HEIGHT // GRID_SIZE
        return (random.randint(0, max_x - 1), random.randint(0, max_y - 1))