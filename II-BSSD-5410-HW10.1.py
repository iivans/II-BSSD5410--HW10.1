import pygame as pg
import sys
import time
from pygame.locals import *
import random

# Global variables
XO = 'O'
winner = None
draw = None
width = 400
height = 400
white = (255, 255, 255)
line_color = (0, 0, 0)
board = [[None] * 3 for _ in range(3)]
MAX = 1000
MIN = -1000

# Stats 
draws = 0
mmx = 0
ran = 0

# Initialize Pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("My Tic Tac Toe")
initiating_window = pg.image.load("modified_cover.png")
x_img = pg.image.load("X_modified.png")
y_img = pg.image.load("o_modified.png")
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))

def game_initiating_window():
    screen.blit(initiating_window, (0, 0))
    pg.display.update()
    time.sleep(0.1)
    screen.fill(white)
    pg.event.clear()
    draw_lines()
    draw_status()

def draw_lines():
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)

def draw_status():
    global draw, ran, mmx, draws
    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        if winner == 'x':
            ran += 1
            message = winner.upper() + " won! (Random)"
        else:
            mmx += 1
            message = winner.upper() + " won! (Minimax)"
    if draw:
        draws += 1
        message = "Game Draw!"
    
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win(ret_val=False):
    global board, winner, draw

    # RIGHT HERE IF YOU SWAP THE DRAW LOGIC 
    # AND THE WIN LOGIC IN THE MAIN FUNCTION 
    # DRAWS WONT COUNT TOWARDS THE games_played

    #Win Logic
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row + 1) * height / 3 - height / 6), (width, (row + 1) * height / 3 - height / 6), 4)
            break
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0), ((col + 1) * width / 3 - width / 6, height), 4)
            break
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    #Draw Logic
    if all([all(row) for row in board]) and winner is None:
        draw = True
    if ret_val:
        if draw:
            draw = None
            return True
        else:
            return False
        
    draw_status()

def drawXO(row, col):
    global board, XO

    if row == 1:
        posx = 30
    elif row == 2:
        posx = width / 3 + 30
    elif row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30
    elif col == 2:
        posy = height / 3 + 30
    elif col == 3:
        posy = height / 3 * 2 + 30

    board[row - 1][col - 1] = XO

    if XO == 'x':
        screen.blit(x_img, (posy, posx))
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'

    pg.display.update()

def random_move():
    valid_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
    if valid_moves:
        move = random.choice(valid_moves)
        drawXO(move[0] + 1, move[1] + 1)  # Convert 0-based index to 1-based index
        check_win()

def minimax_move():
    best_val = MIN
    best_move = None

    # Iterate through the board to find the best move using minimax
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:  
                board[row][col] = 'o'  
                move_val = minimax(board, 0, False, MIN, MAX)  
                board[row][col] = None  

                
                if move_val > best_val:
                    best_val = move_val
                    best_move = (row, col)


    if best_move:
        drawXO(best_move[0] + 1, best_move[1] + 1)  # Convert 0-based index to 1-based index
        check_win()


def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)
    if abs(score) == 10 or check_win(True):
        return score
    if is_max:
        best = MIN
        for row in range(1, 4):
            for col in range(1, 4):
                if board[row-1][col-1] is None:
                    board[row-1][col-1] = 'o'
                    best = max(best, minimax(board, depth+1, False, alpha, beta))
                    alpha = max(alpha, best)
                    board[row-1][col-1] = None
                    if beta <= alpha:
                        break
        return best
    else:
        best = MAX
        for row in range(1, 4):
            for col in range(1, 4):
                if board[row-1][col-1] is None:
                    board[row-1][col-1] = 'x'
                    best = min(best, minimax(board, depth+1, True, alpha, beta))
                    beta = min(beta, best)
                    board[row-1][col-1] = None
                    if beta <= alpha:
                        break
        return best

def evaluate(b):
    player = 'o'
    opponent = 'x'
    for row in range(0, 3):
        if b[row][0] == b[row][1] == b[row][2]:
            if b[row][0] == player:
                return +10
            elif b[row][0] == opponent:
                return -10

    for col in range(0, 3):
        if b[0][col] == b[1][col] == b[2][col]:
            if b[0][col] == player:
                return +10
            elif b[0][col] == opponent:
                return -10

    if b[0][0] == b[1][1] == b[2][2]:
        if b[0][0] == player:
            return +10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] == b[2][0]:
        if b[0][2] == player:
            return +10
        elif b[0][2] == opponent:
            return -10

    return 0

def reset_game():
    global board, winner, XO, draw
    time.sleep(0.1)
    XO = 'o'
    draw = None  # Reset draw to None
    winner = None  # Reset winner to None
    board = [[None] * 3 for _ in range(3)]  # Clear the board
    game_initiating_window()

# This from my testing ensures only 200 games played. 
def main():
    game_initiating_window()
    games_played = 0  # Track games played within the main function

    while games_played < 200:
        play_game_turn()  # Handle both Minimax and Random player's moves
        
        if game_ended():  # Check if the game ended 
            games_played += 1
            reset_game()

    # After 200 games, print the final stats and exit
    end_game()


def play_game_turn():

    minimax_move()
    if game_ended():  # Skip random move if the game already ended
        return

    random_move()


def game_ended():
    return winner is not None or draw is not None


def end_game():
    print(f"200 games played. Exiting...")
    print(f"Draws: {draws}, Minimax Wins: {mmx}, Random Wins: {ran}")
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
