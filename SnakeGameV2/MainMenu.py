import pygame
from GameConstants import *
from HighScoreManager import get_high_score

class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.title_font.set_bold(True)
        self.text_font = pygame.font.Font(None, TEXT_FONT_SIZE)
        self.text_font.set_bold(True)
        self.control_font = pygame.font.Font(None, CONTROL_FONT_SIZE)
        self.control_font.set_bold(True)
        self.running = True
        self.start_game = False

        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.exit_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT)

    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            play_hovered = self.play_button.collidepoint(mouse_pos)
            exit_hovered = self.exit_button.collidepoint(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_hovered:
                        self.start_game = True
                        self.running = False
                    if exit_hovered:
                        self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game = True
                        self.running = False
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.screen.fill(BLACK)

            # Title with red shadow
            title_shadow = self.title_font.render("SNAKE GAME", True, RED)
            self.screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + SHADOW_OFFSET, 100 + SHADOW_OFFSET))
            title = self.title_font.render("SNAKE GAME", True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            # High score
            high_score = get_high_score()
            hs_text = self.text_font.render(f"High Score: {high_score}", True, WHITE)
            self.screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 200))

            # Play Button
            play_scale = 1.5 if play_hovered else 1.0
            play_rect = pygame.Rect(
                self.play_button.x - (BUTTON_WIDTH * (play_scale - 1)) / 2,
                self.play_button.y - (BUTTON_HEIGHT * (play_scale - 1)) / 2,
                BUTTON_WIDTH * play_scale,
                BUTTON_HEIGHT * play_scale
            )
            pygame.draw.rect(self.screen, BUTTON_PLAY_HOVER_COLOR if play_hovered else BUTTON_PLAY_COLOR, play_rect)
            play_text = self.text_font.render("Play Now", True, BUTTON_PLAY_TEXT_HOVER_COLOR if play_hovered else BUTTON_PLAY_TEXT_COLOR)
            if play_hovered:
                play_shadow = self.text_font.render("Play Now", True, BUTTON_PLAY_SHADOW_COLOR)
                self.screen.blit(play_shadow, (play_rect.x + (play_rect.width - play_shadow.get_width()) / 2 + SHADOW_OFFSET, play_rect.y + 10 + SHADOW_OFFSET))
            self.screen.blit(play_text, (play_rect.x + (play_rect.width - play_text.get_width()) / 2, play_rect.y + 10))

            # Exit Button
            exit_scale = 1.5 if exit_hovered else 1.0
            exit_rect = pygame.Rect(
                self.exit_button.x - (BUTTON_WIDTH * (exit_scale - 1)) / 2,
                self.exit_button.y - (BUTTON_HEIGHT * (exit_scale - 1)) / 2,
                BUTTON_WIDTH * exit_scale,
                BUTTON_HEIGHT * exit_scale
            )
            pygame.draw.rect(self.screen, BUTTON_EXIT_HOVER_COLOR if exit_hovered else BUTTON_EXIT_COLOR, exit_rect)
            exit_text = self.text_font.render("Exit", True, BUTTON_EXIT_TEXT_HOVER_COLOR if exit_hovered else BUTTON_EXIT_TEXT_COLOR)
            if exit_hovered:
                exit_shadow = self.text_font.render("Exit", True, BUTTON_EXIT_SHADOW_COLOR)
                self.screen.blit(exit_shadow, (exit_rect.x + (exit_rect.width - exit_shadow.get_width()) / 2 + SHADOW_OFFSET, exit_rect.y + 10 + SHADOW_OFFSET))
            self.screen.blit(exit_text, (exit_rect.x + (exit_rect.width - exit_text.get_width()) / 2, exit_rect.y + 10))

            # Controls
            game_controls = self.control_font.render("MOVEMENT = WASD ", True, WHITE)
            self.screen.blit(game_controls, (SCREEN_WIDTH - game_controls.get_width() - 50, 350))

            # Credits
            # Credits in bottom-right corner with red shadow
            credits_text = "A Key'n Brosdahl Project"
            credits_render = self.control_font.render(credits_text, True, YELLOW)
            credits_shadow = self.control_font.render(credits_text, True, RED)

            credit_x = SCREEN_WIDTH - credits_render.get_width() - 20
            credit_y = SCREEN_HEIGHT - credits_render.get_height() - 20

            self.screen.blit(credits_shadow, (credit_x + SHADOW_OFFSET, credit_y + SHADOW_OFFSET))
            self.screen.blit(credits_render, (credit_x, credit_y))


            pygame.display.flip()

    
