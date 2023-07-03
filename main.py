import numpy as np
import pygame
import sys
import math

# Define color constants
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define the number of rows and columns on the board
ROW_COUNT = 6
COL_COUNT = 7

def create_board():
    """
    Create an empty game board using NumPy.
    """
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board

def drop_piece(board, row, col, piece):
    """
    Drop a game piece (1 or 2) at the specified position on the board.
    """
    board[row][col] = piece

def is_valid_location(board, col):
    """
    Check if a column is a valid choice for placing a game piece.
    """
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    """
    Get the next available row in a column for placing a game piece.
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """
    Print the current state of the game board.
    """
    print(np.flip(board, 0))

def winning_move(board, piece):
    """
    Check if a player has won the game by connecting four game pieces.
    """
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    """
    Draw the game board using the Pygame library.
    """
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    pygame.display.update()

# Create an empty game board
board = create_board()
print_board(board)

# Initialize game state variables
game_over = False
turn = 0

# Initialize Pygame
pygame.init()

# Set the size of each square on the game board
SQUARE_SIZE = 100

# Calculate the width and height of the game window
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE

# Create the game window
size = width, height

RADIUS = int(SQUARE_SIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

# Initialize the font for displaying game over messages
myfont = pygame.font.SysFont("monospace", 75)


# Game loop
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # Draw a moving game piece at the current mouse position
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Place a game piece at the selected column
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            if turn == 0:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 Wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            else:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 Wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)

            draw_board(board)

            # Switch turns between players
            turn += 1
            turn = turn % 2

            if game_over:
                # Pause the game for 1.4 seconds before closing the window
                pygame.time.wait(1400)
