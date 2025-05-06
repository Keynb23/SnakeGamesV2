import pygame

# Automatically detect screen size
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
GRID_SIZE = 20

BLACK = (0, 0, 0)
DARK_GRAY = (160, 160, 160)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_RED = (100, 0, 0)
SPECIAL_FOOD_COLOR = (255, 215, 0)  # Gold for special foods
BOOST_FOOD_COLOR = (0, 0, 255)  # Blue for boost food
BOOST_METER_COLOR = (0, 191, 255)  # Cyan for boost meter
FIRE_ORANGE = (255, 165, 0)  # Orange for fire tail
FIRE_YELLOW = (255, 255, 0)  # Yellow for fire tail
PURPLE = (128, 0, 128)  # Purple background at 81 points
TARANTINO_YELLOW = (255, 255, 0)  # Yellow for "Ha Nice" text
TARANTINO_BLACK = (0, 0, 0)  # Black outline for "Ha Nice"
SUNSHINE_YELLOW = (255, 255, 0)  # Yellow for Level 4 sun
BLOOD_RED = (255, 0, 0)  # Blood color
RAINBOW_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130)]  # Red, Orange, Yellow, Green, Blue, Indigo

SNAKE_SPEED = 10
BOOST_SPEED = SNAKE_SPEED * 2  # 2 times the default speed (20 FPS)
BOOST_DURATION = 3 * SNAKE_SPEED  # 3 seconds at SNAKE_SPEED FPS
BOOST_FOOD_DURATION = 8 * SNAKE_SPEED  # 8 seconds visible
BOOST_FOOD_BLINK_DURATION = 3 * SNAKE_SPEED  # 3 seconds blinking
BOOST_FOOD_TOTAL_DURATION = BOOST_FOOD_DURATION + BOOST_FOOD_BLINK_DURATION  # Total 11 seconds
BOOST_SPAWN_INTERVAL = 60 * SNAKE_SPEED  # Spawn every 60 seconds
DEMON_DOGS_INTERVAL = 15  # Points interval for spawning special foods
MULTIPLIER_DURATION = 8 * SNAKE_SPEED  # 8 seconds at SNAKE_SPEED FPS
MULTIPLIER_VALUE = 2.4  # 2.4x multiplier for points
HA_NICE_DURATION = 3 * SNAKE_SPEED  # 3 seconds display for "Ha Nice"
LEVEL_4_CUTSCENE_DURATION = 15 * SNAKE_SPEED  # 15 seconds for the cutscene

# UI Styles
TITLE_FONT_SIZE = 60
TEXT_FONT_SIZE = 36
CONTROL_FONT_SIZE = 28
HA_NICE_FONT_SIZE = 72  # Large font for "Ha Nice"
NARRATIVE_FONT_SIZE = 24  # Font for Level 4 narrative

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

# Play button
BUTTON_PLAY_COLOR = WHITE
BUTTON_PLAY_HOVER_COLOR = YELLOW
BUTTON_PLAY_TEXT_COLOR = BLACK
BUTTON_PLAY_TEXT_HOVER_COLOR = RED
BUTTON_PLAY_SHADOW_COLOR = BLACK

# Exit button (inverted style)
BUTTON_EXIT_COLOR = DARK_RED
BUTTON_EXIT_HOVER_COLOR = RED
BUTTON_EXIT_TEXT_COLOR = WHITE
BUTTON_EXIT_TEXT_HOVER_COLOR = YELLOW
BUTTON_EXIT_SHADOW_COLOR = BLACK

# Shared shadow
SHADOW_OFFSET = 1.5

# Game Over UI
GAME_OVER_FONT_SIZE = 48
GAME_OVER_BUTTON_WIDTH = 150
GAME_OVER_BUTTON_HEIGHT = 50