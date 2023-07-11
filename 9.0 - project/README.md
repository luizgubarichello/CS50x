# MEMORY GAME
#### Video Demo:  https://youtu.be/LPbOd7y42i8
#### Description:
A Memory Game made with Python's PyGame library.

The game starts with a menu screen displaying the difficulty options: Easy, Medium, and Hard. The player can click on one of the difficulty options to start the game. Depending on the selected difficulty, the grid size and the number of pairs will vary. Easy difficulty has a 2x4 grid, Medium has a 4x4 grid, and Hard has a 4x6 grid.

Once the game starts, the player can click on a card to reveal its value. The goal is to find matching pairs by selecting two cards at a time. If the selected cards have the same value, they remain face up, indicating a successful match. If the selected cards do not match, they are flipped back over after a brief delay. The player can continue selecting cards until all pairs have been matched.

The game provides visual feedback by highlighting the selected cards in red. When a pair is matched, the matched cards are displayed in black, distinguishing them from the unmatched cards. Once all pairs are matched, a "Congratulations! You won!" message is displayed on the screen.

The game also includes a "Main Menu" button that appears when the game is over. Clicking on this button takes the player back to the main menu, allowing them to choose a different difficulty level and start a new game.

About the code:

Most of it is about following pygame's syntax

The code begins by importing the necessary libraries: pygame for creating the game interface and random for shuffling the cards. Then, it initializes the Pygame module by calling `pygame.init()`.

The display is set up with the specified width, height, and frames per second (FPS). The Pygame display surface is created using `pygame.display.set_mode()` and given a title using `pygame.display.set_caption()`.

Next, various colors and fonts are defined using RGB values. These colors will be used for drawing the game elements on the screen. The font object is created using `pygame.font.Font()`.

The game variables are initialized, including the clock for controlling the game speed, the size of each card, and the variables for the number of rows, columns, pairs, and total cards. The cards list is created to hold the values of the cards.

The game state variables are set: `game_state` represents the current state of the game (`START`, `PLAYING`, or `GAME_OVER`), and `difficulty` stores the selected difficulty level.

The code defines a button rectangle using `pygame.Rect()` for displaying the main menu button.

The code then proceeds to define several functions.

`show_menu()` is responsible for rendering the main menu on the screen. It displays the game title, difficulty options (Easy, Medium, Hard), and updates the Pygame display using `pygame.display.flip()`.

`show_board()` renders the game board on the screen. It fills the background with black, draws the cards based on their state (matched, selected, or unselected), and updates the display using `pygame.display.flip()`.

`deselect_cards()` is called when two selected cards do not match. It delays the game for one second using `pygame.time.delay()` and then clears the selected list.

`check_match()` checks if the two selected cards match by comparing their values. If they match, the function adds them to the matched list and returns `True`. Otherwise, it returns `False`.

`start_game(difficulty_level)` sets up the game based on the selected difficulty level. It determines the number of rows, columns, pairs, and total cards, initializes the cards list with the appropriate number of pairs, shuffles them randomly, and populates the board list with the card values. The selected and matched lists are also cleared. Finally, the game state is set to PLAYING.

`show_game_over()` displays a "Congratulations! You won!" message on the screen when all pairs have been matched. It also renders the main menu button and updates the display.

The main game loop begins with `while running:`. It controls the flow of the game and continuously updates the display.

Inside the loop, `clock.tick(FPS)` is called to limit the frame rate of the game.

The loop processes user input and events using `pygame.event.get()`. If the user clicks the close button, the loop exits and the game ends. If the user clicks the mouse button, the code checks the current game state to determine the appropriate action.

If the game state is `START`, the code checks the mouse position and starts the game with the corresponding difficulty level when the player clicks on one of the options.

If the game state is `PLAYING`, the code handles the selection of cards. It checks if the player can select another card (less than two cards selected), calculates the row and column of the clicked card, and checks if the selected card is valid (not already selected or matched). If the selected cards make a pair, it checks if they match using `check_match()`. If they do, the selected list is cleared; otherwise, the board is updated using `show_board()`, and the cards are deselected after a delay using `deselect_cards()`.

If the game state is `GAME_OVER`, the code checks if the main menu button is clicked. If it is, the game state is set to `START`, and the main menu is displayed again.

Finally, inside the main game loop, the code updates the display based on the current game state. If the state is `START`, the menu is shown using `show_menu()`. If the state is `PLAYING`, the game board is displayed using `show_board()`. If the state is `GAME_OVER`, the "Congratulations" message and main menu button are shown using `show_game_over()`.

Once the main game loop is exited (when the user closes the game window), `pygame.quit()` is called to clean up the Pygame module and exit the program.

Overall, the code incorporates game states, event handling, rendering of graphics, and logic for card matching and game progression. It provides an interactive and engaging experience for players to test their memory skills.
