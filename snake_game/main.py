import pygame
from menu import Menu
from auth import Auth
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((601, 601))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    auth = Auth()
    menu = Menu(screen, clock)
    
    # Auth flow
    current_user = None
    while current_user is None:
        action, username, password = menu.show_auth_screen()
        if action == "quit":
            pygame.quit()
            return
        elif action == "register":
            success, msg = auth.register(username, password)
            menu.show_message(msg)
            if success:
                current_user = username
        elif action == "login":
            success, msg = auth.login(username, password)
            menu.show_message(msg)
            if success:
                current_user = username

    # Main menu loop
    while True:
        choice = menu.show_main_menu(current_user)
        if choice == "play":
            difficulty = menu.show_difficulty_menu()
            if difficulty:
                game = Game(screen, clock, current_user, difficulty)
                game.run()
        elif choice == "leaderboard":
            menu.show_leaderboard()
        elif choice == "logout":
            current_user = None
            while current_user is None:
                action, username, password = menu.show_auth_screen()
                if action == "quit":
                    pygame.quit()
                    return
                elif action == "register":
                    success, msg = auth.register(username, password)
                    menu.show_message(msg)
                    if success:
                        current_user = username
                elif action == "login":
                    success, msg = auth.login(username, password)
                    menu.show_message(msg)
                    if success:
                        current_user = username
        elif choice == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
