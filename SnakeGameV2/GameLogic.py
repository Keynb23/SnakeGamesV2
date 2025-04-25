import pygame
import random
from CharacterClass import Snake, Food
from HighScoreManager import save_high_score
from GameConstants import *

class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.direction = (1, 0)  # Initial direction: right
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
        return None

    def update(self):
        if not self.game_over:
            # Move snake
            self.snake.move(self.direction)
            
            # Check for food collision
            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.score += 1
                self.food = Food()
            
            # Check for self collision
            if self.snake.body[0] in self.snake.body[1:]:
                self.game_over = True
                save_high_score(self.score)
            
            # Check for wall collision
            head_x, head_y = self.snake.body[0]
            if head_x < 0 or head_x >= SCREEN_WIDTH // GRID_SIZE or head_y < 0 or head_y >= SCREEN_HEIGHT // GRID_SIZE:
                self.game_over = True
                save_high_score(self.score)

    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw food
        pygame.draw.rect(screen, RED, (self.food.position[0] * GRID_SIZE, self.food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if self.game_over:
            # Draw game over text
            game_over_text = self.game_over_font.render(f"Game Over! Score: {self.score}", True, WHITE)
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