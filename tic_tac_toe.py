import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 500
GRID_SIZE = BOARD_SIZE // 3
LINE_WIDTH = 15
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
CIRCLE_RADIUS = GRID_SIZE // 3
CIRCLE_COLOR = (0, 0, 255)  # Blue
CROSS_COLOR = (255, 0, 0)   # Red
BG_COLOR = (28, 170, 156)   # Teal
LINE_COLOR = (23, 145, 135) # Darker teal
TEXT_COLOR = (255, 255, 255) # White

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Game state
board = [[None for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_over = False
winner = None

# Fonts
font = pygame.font.SysFont('Arial', 40)
restart_font = pygame.font.SysFont('Arial', 24)

def draw_board():
    # Draw grid lines
    pygame.draw.line(screen, LINE_COLOR, (WIDTH//2 - BOARD_SIZE//2, HEIGHT//2 - BOARD_SIZE//6), 
                    (WIDTH//2 + BOARD_SIZE//2, HEIGHT//2 - BOARD_SIZE//6), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH//2 - BOARD_SIZE//2, HEIGHT//2 + BOARD_SIZE//6), 
                    (WIDTH//2 + BOARD_SIZE//2, HEIGHT//2 + BOARD_SIZE//6), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH//2 - BOARD_SIZE//6, HEIGHT//2 - BOARD_SIZE//2), 
                    (WIDTH//2 - BOARD_SIZE//6, HEIGHT//2 + BOARD_SIZE//2), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH//2 + BOARD_SIZE//6, HEIGHT//2 - BOARD_SIZE//2), 
                    (WIDTH//2 + BOARD_SIZE//6, HEIGHT//2 + BOARD_SIZE//2), LINE_WIDTH)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                  (WIDTH//2 - BOARD_SIZE//2 + col * GRID_SIZE + GRID_SIZE//2, 
                                   HEIGHT//2 - BOARD_SIZE//2 + row * GRID_SIZE + GRID_SIZE//2), 
                                  CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                # Draw X (two crossing lines)
                start_x = WIDTH//2 - BOARD_SIZE//2 + col * GRID_SIZE + GRID_SIZE//4
                start_y = HEIGHT//2 - BOARD_SIZE//2 + row * GRID_SIZE + GRID_SIZE//4
                end_x = start_x + GRID_SIZE//2
                end_y = start_y + GRID_SIZE//2
                pygame.draw.line(screen, CROSS_COLOR, (start_x, start_y), (end_x, end_y), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (end_x, start_y), (start_x, end_y), CROSS_WIDTH)

def draw_status():
    # Clear status area
    pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, 100))
    
    if game_over:
        if winner:
            text = f"Player {winner} wins!"
        else:
            text = "Game ended in a draw!"
    else:
        text = f"Player {current_player}'s turn"
    
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 50))
    screen.blit(text_surface, text_rect)
    
    # Draw restart button
    if game_over:
        pygame.draw.rect(screen, (50, 50, 50), (WIDTH//2 - 75, HEIGHT - 80, 150, 50))
        restart_text = restart_font.render("Restart Game", True, TEXT_COLOR)
        screen.blit(restart_text, (WIDTH//2 - 70, HEIGHT - 70))

def check_win():
    global winner, game_over
    
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            game_over = True
            return
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            game_over = True
            return
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        game_over = True
        return
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        game_over = True
        return
    
    # Check for draw
    if all(board[row][col] is not None for row in range(3) for col in range(3)):
        game_over = True

def restart_game():
    global board, current_player, game_over, winner
    board = [[None for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_board()
    draw_status()

# Draw the initial board
draw_board()
draw_status()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            
            # Calculate which cell was clicked
            row = (mouseY - (HEIGHT//2 - BOARD_SIZE//2)) // GRID_SIZE
            col = (mouseX - (WIDTH//2 - BOARD_SIZE//2)) // GRID_SIZE
            
            # Make sure the click is within the board
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None:
                board[row][col] = current_player
                
                # Check for win or draw
                check_win()
                
                # Switch player
                current_player = 'O' if current_player == 'X' else 'X'
                
                # Redraw the board
                draw_figures()
                draw_status()
        
        # Handle restart button click
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouseX, mouseY = event.pos
            if WIDTH//2 - 75 <= mouseX <= WIDTH//2 + 75 and HEIGHT - 80 <= mouseY <= HEIGHT - 30:
                restart_game()
    
    pygame.display.update()