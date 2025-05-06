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

class SpecialFood:
    def __init__(self):
        self.position = self.random_position()
        self.speed = (random.choice([-1, 1]), random.choice([-1, 1]))  # Slow movement
        self.lifetime = 10 * SNAKE_SPEED  # 10 seconds at SNAKE_SPEED FPS
        self.blink_timer = 0
        self.visible = True

    def random_position(self):
        max_x = SCREEN_WIDTH // GRID_SIZE
        max_y = SCREEN_HEIGHT // GRID_SIZE
        return (random.randint(0, max_x - 1), random.randint(0, max_y - 1))

    def update(self):
        self.lifetime -= 1
        # Move every few frames for slow movement
        if self.lifetime % 5 == 0:
            x, y = self.position
            dx, dy = self.speed
            new_x = (x + dx) % (SCREEN_WIDTH // GRID_SIZE)
            new_y = (y + dy) % (SCREEN_HEIGHT // GRID_SIZE)
            self.position = (new_x, new_y)
        # Start blinking at 7 seconds (last 3 seconds)
        if self.lifetime <= 3 * SNAKE_SPEED:
            self.blink_timer += 1
            self.visible = (self.blink_timer % 5) < 3  # Blink on/off

class BoostFood:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        max_x = SCREEN_WIDTH // GRID_SIZE
        max_y = SCREEN_HEIGHT // GRID_SIZE
        return (random.randint(0, max_x - 4), random.randint(0, max_y - 4))  # Ensure space for 2x2 grid