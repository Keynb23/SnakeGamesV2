import pygame
from MainMenu import MainMenu
from GameLogic import SnakeGame
from GameConstants import *

def run_game():
    # Initialize Pygame only if not already initialized
    if not pygame.get_init():
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        screen = pygame.display.get_surface()  # Reuse existing display

    clock = pygame.time.Clock()

    try:
        while True:  # Main loop to allow returning to menu
            menu = MainMenu()
            menu.run()

            if not menu.start_game:
                break  # Exit if menu selects Exit

            game = SnakeGame()
            while True:
                action = game.handle_input()
                if action == "exit":
                    break  # Exit to menu
                if action == "restart":
                    game = SnakeGame()  # Restart
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                game.update()
                game.draw(screen)
                pygame.display.flip()
                clock.tick(SNAKE_SPEED)
    except Exception as e:
        print(f"Error starting game: {e}")
        raise
    finally:
        pygame.quit()

if __name__ == "__main__":
    run_game()