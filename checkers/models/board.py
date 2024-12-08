import pygame
from .piece import Piece
from termcolor import colored

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

ROWS = 8

class Board:
    def __init__(self):
        self.board = []
        self.selected_current = None
        self.blue_c = self.red_c = 12
        self.blue_k = self.red_k = 0
        self.moves = {}

        self.create_board()

    def draw_rect(self, window):
        window.fill(BLACK)

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BLUE, (row * 80,  col * 80, 80, 80))


    def create_board(self):
        for row in range(ROWS):
            
            self.board.append([])
            
            for col in range(ROWS):
                if (col % 2 == 0 and row % 2 == 1) or (col % 2 == 1 and row % 2 == 0):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4: 
                        self.board[row].append(Piece(row, col, BLUE))
                    else: 
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


    def draw_all(self, win):
        self.draw_rect(win)
        for row in range(ROWS):
            for col in range(ROWS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_circle(win)


    def move(self, piece, row, column):
        self.board[piece.row][piece.col], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.col]
        piece.move(row, column)

        if row == 0 or row == ROWS - 1:
            piece.become_ch()
            if piece.color == BLUE:
                self.blue_k += 1
            else:
                self.red_k += 1


    def get_piece(self, row, col):
        return self.board[row][col]


    def write_board(self):
        for row in self.board:
            for elem in row:
                if elem == 0:
                    print("0", end=' ')
                elif elem.color == BLUE:
                    print(colored('P', 'blue'), end=' ')
                elif elem.color == RED:
                    print(colored('C', 'red'), end=' ')
            print('')
    
    
    
    def display_moves(self):
        for key in self.moves.keys():
            print("KEY : " ,key, ' MOVES: ', self.moves.get(key))
