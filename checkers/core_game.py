from models.board import Board
from models.piece import Piece
import pygame
BLUE = (0, 0, 255)
RED = (255, 0, 0)
dimensions = (740, 280, 160, 80)

class Core:
    
    
    def __init__(self, window) :
        self.board = Board()
        self.selected  = None
        self.turn = BLUE 
        self.window = window
        self.text = 'BLUE PLAYING'



    def update_game_core(self, dimensions, font_size):
        self.board.draw_all(self.window)
        self.draw_moves()
        self.draw_status(dimensions, font_size)
        pygame.display.update()
    



    def draw_moves(self):
        
        if self.selected:

            for element in self.board.moves[(self.selected.row, self.selected.col)]:
                if len(element)>1:
                    i = 0
                    for i in range(1, len(element), 2):

                        row, col = element[i]
                        x_off = col * 80
                        y_off = row * 80
                        pygame.draw.circle(self.window, (0,255,0), (x_off + 40, y_off + 40), 20)
                else:
                    if len(element) > 0:
                        row, col = element[0]
                        x_off = col * 80
                        y_off = row * 80
                        pygame.draw.circle(self.window, (0,255,0), (x_off + 40, y_off + 40), 20)

    def draw_status(self, dimensions, font_size):
        
        pygame.draw.rect(self.window, self.turn, dimensions)

        font = pygame.font.SysFont(None, font_size)  
        
        text_surface = font.render(self.text, True, (0, 0, 0)) 
        
        text_rect = text_surface.get_rect(center=(820, 320))  
        
        self.window.blit(text_surface, text_rect)


    def check_move(self, position):


        row, col = self.get_zero_place(position)
        
        for element in self.board.moves[(self.selected.row, self.selected.col)]:
            
            if len(element) > 0:
                if len(element) > 1:
                    for i in range(1, len(element), 2):
                        if element[i] == (row, col):
                            
                            if self.selected.color == BLUE and row == 0:
                                self.selected.become_ch()
                                self.board.board[self.selected.row][self.selected.col].become_ch()
                            elif self.selected.color == RED and row == 7:
                                self.selected.become_ch()
                                self.board.board[self.selected.row][self.selected.col].become_ch()

                            if len(element) > 1:
                                for item in element[:i]:
                                    x, y = item
                                    if self.board.board[x][y] != 0:
                                        if self.board.board[x][y].color == RED:
                                            self.board.red_c -= 1
                                            if self.board.board[x][y].ch:
                                                self.board.red_k -= 1
                                        else:
                                            self.board.blue_c -=1
                                            if self.board.board[x][y].ch:
                                                self.board.blue_k -= 1
                                        self.board.board[x][y] = 0
                            self.board.move(self.selected, row, col)

                            self.selected = None
                            return True
                else:
                    if element[0] == (row, col):
                        if self.selected.color == BLUE and row == 0:
                            self.selected.become_ch()
                            self.board.board[self.selected.row][self.selected.col].become_ch()
                        elif self.selected.color == RED and row == 7:
                            self.selected.become_ch()
                            self.board.board[self.selected.row][self.selected.col].become_ch()
                        self.board.move(self.selected, row, col)

                        self.selected = None
                        return True
        return False


    def get_zero_place(self, position):
        x, y = position
        i = 0
        for row in self.board.board:
            if i > 7:
                break
            j = 0
            for piece in row:
                if j > 7:
                    break
                x_offset = j * 80
                x_limit = x_offset + 80
                y_offset = i * 80
                y_limit = y_offset + 80
                if  (x<=x_limit and x>=x_offset) and (y >= y_offset and y <= y_limit):
                    
                    return (i, j)

                j +=1     
            i +=1 


    def flip_turn(self):
        
        if self.turn == BLUE:
            self.turn = RED
            self.text = 'RED PLAYING'
        else:
            self.turn = BLUE
            self.text = 'BLUE PLAYING'
    
    def end_game(self, text):
        self.turn = (255, 255, 255)
        self.text = text
    