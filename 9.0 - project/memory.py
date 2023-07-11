import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 40)

# Game variables
clock = pygame.time.Clock()
card_size = (80, 80)
num_rows = 0
num_cols = 0
num_pairs = 0
total_cards = 0

# Create cards
cards = []

# Initialize game state
board = []
selected = []
matched = []

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2

game_state = START
difficulty = None

# Buttons
menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)


def show_menu():
    screen.fill(BLACK)
    title_text = FONT.render("Memory Game", True, WHITE)
    easy_text = FONT.render("Easy", True, WHITE)
    medium_text = FONT.render("Medium", True, WHITE)
    hard_text = FONT.render("Hard", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 200))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 250))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 300))

    pygame.display.flip()


def show_board():
    screen.fill(BLACK)
    for row in range(num_rows):
        for col in range(num_cols):
            if (row, col) in matched:
                pygame.draw.rect(screen, BLACK, (col * 90 + (WIDTH - num_cols * 90) // 2, row * 90 + (HEIGHT - num_rows * 90) // 2, *card_size))
            else:
                pygame.draw.rect(screen, RED, (col * 90 + (WIDTH - num_cols * 90) // 2, row * 90 + (HEIGHT - num_rows * 90) // 2, *card_size))
                if (row, col) in selected:
                    card_value = board[row][col]
                    card_text = FONT.render(str(card_value), True, WHITE)
                    screen.blit(card_text, (col * 90 + (WIDTH - num_cols * 90) // 2 + card_size[0] // 2 - card_text.get_width() // 2,
                                            row * 90 + (HEIGHT - num_rows * 90) // 2 + card_size[1] // 2 - card_text.get_height() // 2))

    pygame.display.flip()


def deselect_cards():
    pygame.time.delay(1000)  # Delay for 1 second
    selected.clear()


def check_match():
    if len(selected) == 2:
        row1, col1 = selected[0]
        row2, col2 = selected[1]
        if board[row1][col1] == board[row2][col2]:
            matched.extend(selected)
            return True
        else:
            return False
    return False


def start_game(difficulty_level):
    global num_rows, num_cols, num_pairs, total_cards, game_state
    if difficulty_level == "easy":
        num_rows = 2
        num_cols = 4
    elif difficulty_level == "medium":
        num_rows = 4
        num_cols = 4
    elif difficulty_level == "hard":
        num_rows = 4
        num_cols = 6

    num_pairs = num_rows * num_cols // 2
    total_cards = num_pairs * 2

    # Create cards
    cards.clear()
    for i in range(num_pairs):
        cards.append(i)
        cards.append(i)
    random.shuffle(cards)

    # Initialize game state
    board.clear()
    for row in range(num_rows):
        row_values = []
        for col in range(num_cols):
            if cards:
                row_values.append(cards.pop())
            else:
                break
        board.append(row_values)

    selected.clear()
    matched.clear()

    game_state = PLAYING


def show_game_over():
    screen.fill(BLACK)
    game_over_text = FONT.render("Congratulations! You won!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.draw.rect(screen, WHITE, menu_button)
    menu_text = FONT.render("Main Menu", True, BLACK)
    screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2))
    pygame.display.flip()


# Game loop
running = True
while running:
    clock.tick(FPS)

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == START:
                mouse_pos = pygame.mouse.get_pos()
                if 200 <= mouse_pos[1] <= 240:
                    start_game("easy")
                elif 250 <= mouse_pos[1] <= 290:
                    start_game("medium")
                elif 300 <= mouse_pos[1] <= 340:
                    start_game("hard")
            elif game_state == PLAYING:
                if len(selected) < 2:
                    row = (event.pos[1] - (HEIGHT - num_rows * 90) // 2) // 90
                    col = (event.pos[0] - (WIDTH - num_cols * 90) // 2) // 90
                    if (row, col) not in selected and (row, col) not in matched:
                        try:
                            board[row][col]
                            selected.append((row, col))
                            if(len(selected) == 2):
                                if(check_match()):
                                    selected.clear()
                                else:
                                    show_board()
                                    deselect_cards()
                        except IndexError:
                            continue
            elif game_state == GAME_OVER:
                if menu_button.collidepoint(event.pos):
                    game_state = START

    # Update
    if game_state == START:
        show_menu()
    elif game_state == PLAYING:
        show_board()
        if len(matched) == total_cards:
            game_state = GAME_OVER
    elif game_state == GAME_OVER:
        show_game_over()

pygame.quit()
