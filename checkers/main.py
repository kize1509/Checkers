import pygame
from pygame.locals import *
from models.board import Board
from core_game import Core
from ai_player.data_collecting import DataCollector
from ai_player.playing_mechanics import PlayerAi
from timeout_handler import function_with_timeout
from timeout_handler import FunctionTimeoutError
from ai_player.Node import Node
import time 
from models.piece import Piece
pygame.init()

WIDTH  = 1000
HEIGHT = 640
DIMENSIONS = (740, 280, 160, 80)
FONT_SIZE = 26
ROWS = 8
COLUMNS = 8
BLUE = (0, 0, 255)
YELLOW = (255, 255, 153)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FRAMES = 60

WIN  = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption('CHECKERS GAME')

def get_ch(position, board):
    x, y = position
    i = 0
    for row in board.board:
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
                return piece

            j +=1     
        i +=1 

def simulate_mouse_down(x, y, button=1):
    event = pygame.event.Event(MOUSEBUTTONDOWN, pos=(x, y), button=button)
    pygame.event.post(event)


def overwrite_core_board(board_core, board_node, core):

    for i in range(0, 8, 1):
        for j in range(0, 8, 1):

            if board_node[i][j] == 0:
                board_core[i][j] = 0
            elif board_node[i][j] != 0:
                
                row, col = board_node[i][j].row, board_node[i][j].col
                color = board_node[i][j].color
                
                board_core[i][j] = Piece(row, col, color)         
                board_core[i][j].ch = board_node[i][j].ch

    core.flip_turn()


def main_loop():
    run = True
    dat_col = DataCollector()
    clock = pygame.time.Clock()
    core = Core(WIN)
    ai_player = PlayerAi()
    i  = 0
    rootNode = Node()
    
    rootNode.value = core.board

    while run:
        clock.tick(FRAMES)
        if core.turn == RED:

            start = time.time()
            next_node = ai_player.play(core, rootNode)  

            if next_node:

                overwrite_core_board(core.board.board, next_node.value.board, core)

                core.board.moves, core.board.blue_c, core.board.red_c, core.board.blue_k, core.board.red_k = next_node.value.moves, next_node.value.blue_c, next_node.value.red_c, next_node.value.blue_k, next_node.value.red_k
                end = time.time()
                print("PLAY DONE IN ", end - start)

                i += 1
            term = rootNode.terminal()

            if term['value']:
                core.end_game(term['message'])
                run = False
                dimensions = (700, 280, 300, 80)
                ai_player.trans_map.write_map()
                core.update_game_core(dimensions, FONT_SIZE)
                time.sleep(3)
                return
    
        

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            if event.type  == pygame.MOUSEBUTTONDOWN :
                

                if core.turn == BLUE:
                    
                    position = pygame.mouse.get_pos()
                    x, y = position
                    if x <= 640:
                        
                        piece = get_ch(position, core.board)

                        if piece and piece.color == core.turn:

                            core.selected = piece
                            dat_col.collect_all_moves(core.board)
                        elif core.selected and piece == 0:
                            moved = core.check_move(position)
                            term = rootNode.terminal()
                            if moved:
                                core.flip_turn()
                            

                            if term['value']:
                                dimensions = (700, 280, 300, 80)
                                run = False
                                core.end_game(term['message'])
                                ai_player.trans_map.write_map()
                                core.update_game_core(dimensions, FONT_SIZE)
                                time.sleep(3)

                                return
                            

                            if i % 2 == 0 and i != 0:
                                dat_col.increment_the_play()
                            

        core.update_game_core(DIMENSIONS, FONT_SIZE)

    pygame.quit()

main_loop()
