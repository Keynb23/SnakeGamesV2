import pygame
from GameConstants import *
from HighScoreManager import get_high_scores

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
        self.username = ""
        self.username_input_active = False
        self.input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 40)

        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.exit_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.dev_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 490, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.choosing_level = False
        self.starting_level = 1

    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            play_hovered = self.play_button.collidepoint(mouse_pos)
            exit_hovered = self.exit_button.collidepoint(mouse_pos)
            dev_hovered = self.dev_button.collidepoint(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if self.username_input_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.username:
                                self.start_game = True
                                self.running = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        elif event.key != pygame.K_ESCAPE and len(self.username) < 15:
                            self.username += event.unicode
                elif self.choosing_level:
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            self.starting_level = int(event.unicode)
                            self.username_input_active = True
                            self.choosing_level = False
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_hovered:
                            self.username_input_active = True
                        if exit_hovered:
                            self.running = False
                        if dev_hovered:
                            self.choosing_level = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.username_input_active = True
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

            self.screen.fill(BLACK)

            if self.username_input_active:
                prompt_text = self.text_font.render("Enter a username:", True, WHITE)
                self.screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                pygame.draw.rect(self.screen, WHITE, self.input_box, 2)
                username_surface = self.text_font.render(self.username, True, WHITE)
                self.screen.blit(username_surface, (self.input_box.x + 5, self.input_box.y + 5))
            elif self.choosing_level:
                prompt = self.text_font.render("Select starting level (1-5)", True, WHITE)
                self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            else:
                # Title
                title_shadow = self.title_font.render("SNAKE GAME", True, RED)
                self.screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + SHADOW_OFFSET, 100 + SHADOW_OFFSET))
                title = self.title_font.render("SNAKE GAME", True, YELLOW)
                self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

                # High Scores
                high_scores = get_high_scores()
                if not isinstance(high_scores, (list, tuple)):
                    print(f"Error: high_scores is not iterable, got {type(high_scores)}: {high_scores}")
                    score_text = self.text_font.render("Error loading scores", True, WHITE)
                    self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
                else:
                    if not high_scores:
                        score_text = self.text_font.render("No scores yet!", True, WHITE)
                        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
                    else:
                        for i, entry in enumerate(high_scores):
                            try:
                                score_text = self.text_font.render(f"{i + 1}. {entry['username']} - {entry['score']}", True, WHITE)
                                self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200 + i * 30))
                            except (KeyError, TypeError) as e:
                                print(f"Error rendering high score entry: {e}")
                                break

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

                # Dev Button
                pygame.draw.rect(self.screen, DARK_GRAY, self.dev_button)
                dev_text = self.text_font.render("Dev Start", True, WHITE)
                self.screen.blit(dev_text, (self.dev_button.x + (self.dev_button.width - dev_text.get_width()) // 2, self.dev_button.y + 10))

                # Controls
                game_controls = self.control_font.render("MOVEMENT = WASD", True, WHITE)
                self.screen.blit(game_controls, (SCREEN_WIDTH - game_controls.get_width() - 50, 350))

                # Credits
                credits_text = "A Key'n Brosdahl Project"
                credits_render = self.text_font.render(credits_text, True, YELLOW)
                credits_shadow = self.text_font.render(credits_text, True, RED)
                credit_x = SCREEN_WIDTH - credits_render.get_width() - 20
                credit_y = SCREEN_HEIGHT - credits_render.get_height() - 20
                self.screen.blit(credits_shadow, (credit_x + SHADOW_OFFSET, credit_y + SHADOW_OFFSET))
                self.screen.blit(credits_render, (credit_x, credit_y))

            pygame.display.flip()

        return self.username if self.start_game else None, self.starting_level