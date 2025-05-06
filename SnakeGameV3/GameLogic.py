import pygame
import random
from CharacterClass import Snake, Food, SpecialFood, BoostFood
from HighScoreManager import save_high_score
from GameConstants import *

class SnakeGame:
    def __init__(self, username):
        self.username = username
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.level = 1  # Start at Level 1
        self.game_over = False
        self.direction = (1, 0)  # Initial direction: right
        self.special_foods = []  # List to store special foods
        self.boost_food = None  # Single boost food
        self.boost_food_timer = 0  # Timer for boost food duration
        self.last_boost_spawn = 0  # Frame count since last spawn attempt
        self.boost_meter = 75  # Start with 75% boost meter
        self.boost_timer = 0  # Timer for active boost
        self.current_speed = SNAKE_SPEED  # Current speed of the snake
        # Game over UI
        self.game_over_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
        self.game_over_font.set_bold(True)
        self.text_font = pygame.font.Font(None, TEXT_FONT_SIZE)
        self.text_font.set_bold(True)
        # Center buttons horizontally, spaced 40 pixels apart
        button_total_width = 2 * GAME_OVER_BUTTON_WIDTH + 40
        self.play_again_button = pygame.Rect(
            SCREEN_WIDTH // 2 - button_total_width // 2,
            SCREEN_HEIGHT // 2 + 50,
            GAME_OVER_BUTTON_WIDTH,
            GAME_OVER_BUTTON_HEIGHT
        )
        self.exit_button = pygame.Rect(
            SCREEN_WIDTH // 2 - button_total_width // 2 + GAME_OVER_BUTTON_WIDTH + 40,
            SCREEN_HEIGHT // 2 + 50,
            GAME_OVER_BUTTON_WIDTH,
            GAME_OVER_BUTTON_HEIGHT
        )

    def handle_input(self):
        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_w and self.direction != (0, 1):
                        self.direction = (0, -1)  # Up
                    elif event.key == pygame.K_s and self.direction != (0, -1):
                        self.direction = (0, 1)   # Down
                    elif event.key == pygame.K_a and self.direction != (1, 0):
                        self.direction = (-1, 0)  # Left
                    elif event.key == pygame.K_d and self.direction != (-1, 0):
                        self.direction = (1, 0)   # Right
                else:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                mouse_pos = event.pos
                if self.play_again_button.collidepoint(mouse_pos):
                    return "restart"
                if self.exit_button.collidepoint(mouse_pos):
                    return "exit"

        # Handle boost activation
        if shift_pressed and self.boost_meter > 0 and self.boost_timer <= 0:
            self.boost_timer = BOOST_DURATION  # Start 3-second boost
            self.boost_meter = max(0, self.boost_meter - 50)  # Consume 50% of boost meter
            print(f"Boost activated! Speed set to {self.current_speed}, Timer: {self.boost_timer / SNAKE_SPEED}s")

        return None

    def update(self):
        if not self.game_over:
            # Update timers
            self.last_boost_spawn += 1

            if self.boost_timer > 0:
                self.current_speed = BOOST_SPEED
                self.boost_timer -= 1
                print(f"Boost active, Speed: {self.current_speed}, Time left: {self.boost_timer / SNAKE_SPEED:.2f}s")
            else:
                self.current_speed = SNAKE_SPEED
                if self.current_speed != SNAKE_SPEED:
                    print(f"Boost ended, Speed reverted to {self.current_speed}")

            # Manage boost food
            if self.boost_food:
                self.boost_food_timer -= 1
                if self.boost_food_timer <= 0:
                    self.boost_food = None
                    self.last_boost_spawn = 0  # Reset spawn timer after boost food vanishes

            # Spawn boost food every minute
            if self.boost_food is None and self.last_boost_spawn >= BOOST_SPAWN_INTERVAL:
                if random.random() < 0.05:  # 5% chance per frame after 60 seconds
                    self.boost_food = BoostFood()
                    self.boost_food_timer = BOOST_FOOD_TOTAL_DURATION
                    self.last_boost_spawn = 0
                    print("Boost food spawned after 60 seconds")

            # Move snake
            self.snake.move(self.direction)
            
            # Check for level progression to Level 2
            if self.score >= 10 and self.level == 1 and not self.special_foods:
                self.level = 2
                # Spawn 10 special foods
                for _ in range(10):
                    self.special_foods.append(SpecialFood())
            
            # Check for food collision
            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.score += 1
                self.food = Food()

            # Check for special food collision
            for special_food in self.special_foods[:]:
                special_food.update()
                if special_food.lifetime <= 0:
                    self.special_foods.remove(special_food)
                    continue
                if self.snake.body[0] == special_food.position:
                    self.score += 1 * 1.25  # 1.25 multiplier for points
                    # 0.5 multiplier for length (round to nearest integer)
                    length_increase = int(1 * 0.5)
                    if length_increase > 0:
                        self.snake.body.extend([self.snake.body[-1]] * length_increase)
                        self.snake.length += length_increase
                    self.special_foods.remove(special_food)

            # Check for boost food collision
            if self.boost_food and self.snake.body[0] == self.boost_food.position:
                self.boost_meter = min(100, self.boost_meter + 50)  # Fill boost meter by 50%
                self.boost_food = None
                self.boost_food_timer = 0
                self.last_boost_spawn = 0  # Reset spawn timer on eat
                print(f"Boost food eaten, Meter: {self.boost_meter}%")
            
            # Check for self collision
            if self.snake.body[0] in self.snake.body[1:]:
                self.game_over = True
                save_high_score(self.username, self.score)
            
            # Check for wall collision
            head_x, head_y = self.snake.body[0]
            if head_x < 0 or head_x >= SCREEN_WIDTH // GRID_SIZE or head_y < 0 or head_y >= SCREEN_HEIGHT // GRID_SIZE:
                self.game_over = True
                save_high_score(self.username, self.score)

    def draw(self, screen):
        screen.fill(BLACK)

        # Draw snake with fire tail during boost
        if self.boost_timer > 0:
            for i, segment in enumerate(self.snake.body):
                color = FIRE_YELLOW if i == len(self.snake.body) - 1 else FIRE_ORANGE if i > len(self.snake.body) // 2 else GREEN
                pygame.draw.rect(screen, color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        else:
            for segment in self.snake.body:
                pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw main food
        pygame.draw.rect(screen, RED, (self.food.position[0] * GRID_SIZE, self.food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw special foods
        for special_food in self.special_foods:
            if special_food.visible:
                pygame.draw.rect(screen, SPECIAL_FOOD_COLOR, (special_food.position[0] * GRID_SIZE, special_food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw boost food with blinking during last 3 seconds
        if self.boost_food:
            x, y = self.boost_food.position
            small_size = GRID_SIZE // 2
            # Blink during the last 3 seconds
            if self.boost_food_timer <= BOOST_FOOD_BLINK_DURATION:
                blink_interval = SNAKE_SPEED // 2  # Blink every 0.5 seconds
                if (self.boost_food_timer // blink_interval) % 2 == 0:
                    for dx in range(2):
                        for dy in range(2):
                            pygame.draw.rect(screen, BOOST_FOOD_COLOR, 
                                            (x * GRID_SIZE + dx * small_size, y * GRID_SIZE + dy * small_size, small_size, small_size))
            else:
                # Solid display for the first 8 seconds
                for dx in range(2):
                    for dy in range(2):
                        pygame.draw.rect(screen, BOOST_FOOD_COLOR, 
                                        (x * GRID_SIZE + dx * small_size, y * GRID_SIZE + dy * small_size, small_size, small_size))
        
        # Draw score, level, and boost meter
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {int(self.score)}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        boost_text = font.render(f"Boost: {self.boost_meter}%", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(boost_text, (10, 90))
        # Draw boost meter bar
        meter_width = 100
        meter_height = 10
        filled_width = (self.boost_meter / 100) * meter_width
        pygame.draw.rect(screen, BOOST_METER_COLOR, (10, 130, filled_width, meter_height))
        pygame.draw.rect(screen, WHITE, (10, 130, meter_width, meter_height), 2)  # Border
        
        if self.game_over:
            # Draw game over text
            game_over_text = self.game_over_font.render(f"Game Over! Score: {int(self.score)}", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            # Draw buttons with hover effects
            mouse_pos = pygame.mouse.get_pos()
            play_hovered = self.play_again_button.collidepoint(mouse_pos)
            exit_hovered = self.exit_button.collidepoint(mouse_pos)
            
            # Play Again button
            play_scale = 1.5 if play_hovered else 1.0
            play_rect = pygame.Rect(
                self.play_again_button.x - (GAME_OVER_BUTTON_WIDTH * (play_scale - 1)) / 2,
                self.play_again_button.y - (GAME_OVER_BUTTON_HEIGHT * (play_scale - 1)) / 2,
                GAME_OVER_BUTTON_WIDTH * play_scale,
                GAME_OVER_BUTTON_HEIGHT * play_scale
            )
            pygame.draw.rect(screen, BUTTON_PLAY_HOVER_COLOR if play_hovered else BUTTON_PLAY_COLOR, play_rect)
            play_text = self.text_font.render("Play Again", True, BUTTON_PLAY_TEXT_HOVER_COLOR if play_hovered else BUTTON_PLAY_TEXT_COLOR)
            if play_hovered:
                play_text_shadow = self.text_font.render("Play Again", True, BUTTON_PLAY_SHADOW_COLOR)
                screen.blit(play_text_shadow, (play_rect.x + (play_rect.width - play_text_shadow.get_width()) / 2 + int(SHADOW_OFFSET), play_rect.y + 10 + int(SHADOW_OFFSET)))
            screen.blit(play_text, (play_rect.x + (play_rect.width - play_text.get_width()) / 2, play_rect.y + 10))
            
            # Exit button
            exit_scale = 1.5 if exit_hovered else 1.0
            exit_rectangle = pygame.Rect(
                self.exit_button.x - (GAME_OVER_BUTTON_WIDTH * (exit_scale - 1)) / 2,
                self.exit_button.y - (GAME_OVER_BUTTON_HEIGHT * (exit_scale - 1)) / 2,
                GAME_OVER_BUTTON_WIDTH * exit_scale,
                GAME_OVER_BUTTON_HEIGHT * exit_scale
            )
            pygame.draw.rect(screen, BUTTON_EXIT_HOVER_COLOR if exit_hovered else BUTTON_EXIT_COLOR, exit_rectangle)
            exit_text = self.text_font.render("Exit", True, BUTTON_EXIT_TEXT_HOVER_COLOR if exit_hovered else BUTTON_EXIT_TEXT_COLOR)
            if exit_hovered:
                exit_text_shadow = self.text_font.render("Exit", True, BUTTON_EXIT_SHADOW_COLOR)
                screen.blit(exit_text_shadow, (exit_rectangle.x + (exit_rectangle.width - exit_text_shadow.get_width()) / 2 + int(SHADOW_OFFSET), exit_rectangle.y + 10 + int(SHADOW_OFFSET)))
            screen.blit(exit_text, (exit_rectangle.x + (exit_rectangle.width - exit_text.get_width()) / 2, exit_rectangle.y + 10))

    def get_speed(self):
        return self.current_speed