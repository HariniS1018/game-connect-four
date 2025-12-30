import numpy as np  # for creating matrix of zeros representing the board
import pygame  # for game development
import sys  # to get the system info
import math  # for performing some mathematical operations

pygame.init() #initializing pygame module
myfont = pygame.font.SysFont("monospace", 50) #selecting the font of the game
print(myfont)
PINK = (255,228,181) # board colour
WHITE = (0,139,0) # background colour
BLACK = (255,255,255) # coin1 colour
AMBER = (20,20,20)# coin2 colour

ROW_COUNT = 6 # declaring no. of rows and columns in board
COLUMN_COUNT = 7


def create_board():  # fn to create board for playing
  board = np.zeros((ROW_COUNT, COLUMN_COUNT))  
  # initial state of board, matrix[6,7] of zeros
  return board


def drop_piece(board, row, column, piece): 
  # fn to drop piece on the players' desired position.
  board[row][column] = piece


def is_valid_location(board, column):
  # check if the top row of that particular column is 	#zero else the column is filled and the player should 	#select a different position. This is invalid location.
  return board[ROW_COUNT - 1][column] == 0


def get_next_open_door(board,column): 
  # check if the particular position in that row is  empty or not
  for r in range(ROW_COUNT):
    if board[r][column] == 0:
      return r

def print_board(board):
  print(np.flip(board,0))
  # to consider the position of index[0][0] as the last row and first column and position from down to up

def winning_move(board, piece): 
  # check for spaces around  the last piece
  # check for horizontal positions
  for c in range(COLUMN_COUNT - 3):
    for r in range(ROW_COUNT):
      if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
        return True

  # check for vertical positions
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT - 3):
      if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
        return True

  # check for positively sloped diagonals
  for c in range(COLUMN_COUNT - 3):
    for r in range(ROW_COUNT - 3):
      if board[r][c] == piece and board[r + 1][c + 1]  == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
        return True

  # check for negatively sloped diagonals
  for c in range(COLUMN_COUNT - 3):
    for r in range(3, ROW_COUNT):
      if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
        return True

def draw_board(board):
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      pygame.draw.rect(screen, PINK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)) 
    pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE /2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
      
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      if board[r][c] == 1:
        pygame.draw.circle(screen, BLACK, (int(c * 
          SQUARESIZE + SQUARESIZE / 
          2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
      elif board[r][c] == 2:
        pygame.draw.circle(screen, AMBER, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
  pygame.display.update()

board = create_board()
print(board) #before flipping
print_board(board)  # after flipping
game_over = False  # means the player not having 4 in a row
turn = 0  
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 15)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


while not game_over: 
  # loop runs till the game_over is F & comes out when T ask
  # for player 1 input
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    if event.type == pygame.MOUSEMOTION:
      pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
      posx = event.pos[0]
      if turn == 0:
        pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE / 2)), RADIUS)
      else:
        pygame.draw.circle(screen, AMBER, (posx, int(SQUARESIZE / 2)), RADIUS)
      pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
      pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))

      # ask for player 1 input
      if turn == 0:
        posx = event.pos[0]
        column = int(math.floor(posx / SQUARESIZE))
        if is_valid_location(board, column):
          row = get_next_open_door(board, column)
          drop_piece(board, row, column, 1)
          if winning_move(board, 1):
            label = myfont.render("!!PLAYER 1 WINS!!", 1, AMBER)
            screen.blit(label, (40, 10))
            game_over = True

        # ask for player 2 input
        else:
          posx = event.pos[0]
          column = int(math.floor(posx / SQUARESIZE))
          if is_valid_location(board, column):
            row = get_next_open_door(board, column)
            drop_piece(board, row, column, 2)
            if winning_move(board, 2):
              label = myfont.render("!!PLAYER 2 WINS!!", 1, AMBER)
              screen.blit(label, (40, 10))
              game_over = True

        # print(board) before flipping
        print_board(board)
        draw_board(board)  # after flipping

        turn += 1
        turn = turn % 2  # like odd or even funtion alternates between zeros
        
        # here the players are alternated.
        if game_over:
          pygame.time.wait(3000)
