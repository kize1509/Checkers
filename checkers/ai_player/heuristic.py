import random
from ai_player.data_collecting import DataCollector

BLUE = (0, 0, 255)
RED = (255, 0, 0)

D_COL = DataCollector()

center_values = [(2,3),(2,4),(3, 3), (3, 4), (4, 3), (4, 4), (5, 3), (5, 4)]
red_base_positions = [(0, i) for i in range(1, 8, 2)]
blue_base_positions = [(7, i) for i in range(0, 8, 2)]
edge_positions = [(i, 0) for i in range(0, 8)] + [(i, 7) for i in range(0, 8)]
#defender positions 
red_defender_pos= [(0, i) for i in range(0, 8)] + [(1, i) for i in range(0, 8)]
blue_defender_pos= [(6, i) for i in range(0, 8)] + [(7, i) for i in range(0, 8)]
#attacking positions
red_attacking_positions = blue_defender_pos + [(5, i) for i in range (0, 8)]
blue_attacking_positions = red_defender_pos + [(2, i) for i in range(0, 8)]
#diagonal positions
main_diagonal = [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6) , (7,7)]
second_diagonal = [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]
#pattern positions 
oreo_red = [(0, 3), (1, 4), (0, 5)]
oreo_blue = [(7, 2), (6, 3), (7, 4)]
triangle_red =[(0, 1), (1, 2), (0, 3)]
triangle_blue = [(7, 4), (6, 5), (7, 6)]
bridge = {RED :[(0, 1), (0, 5)], BLUE: [(7, 2), (7, 6)]}
dog = {RED: [(0, 1), (1, 0)], BLUE: [(7, 6), (6, 7)]}


def heuristic_eval(board):
    
    red_pawns = board.red_c
    red_kings = board.red_k
    blue_pawns = board.blue_c
    blue_kings = board.blue_k
    #safe
    r_pawn, b_pawn, r_king, b_king = get_edge(board)
    #moveable
    r_mov, b_mov, r_k_mov, b_k_mov = get_moveable(board)
    #distance to prom
    red_distance, blue_distance = get_distance_to_promotion(board)
    #promotion line unnocupied fields
    red_unnocupied, blue_unnocupied = unnocupied_promotion_fields(board)
    #defender pawn number
    red_defenders, blue_defenders = get_def_pieces(board)
    #attacking pawn number
    red_atck, blue_atck = get_atck_pieces(board.board)
    #central pawn number, main diagonal, sec diagonal pawns
    red_central, red_k_central, blue_central, blue_k_central, red_main, blue_main, red_main_k, blue_main_k, secondary_red, secondary_blue, secondary_red_kings, secondary_blue_kings = get_central_main_sec_diagonal_pcs(board.board)
    #loner pawns and kings
    red_loners, blue_loners, red_loners_k, blue_loners_k = check_loner_pawns(board.board)
    #holes red, holes blue
    blue_holes = count_holes(board.board, RED)
    red_holes = count_holes(board.board, BLUE)
    #patterns
    triangle_red, triangle_blue, oreo_red, oreo_blue, dog_red, dog_blue, bridge_red, bridge_blue = check_for_patterns(board.board)
    red_corner, blue_corner, red_corner_k, blue_corner_k = check_piece_in_the_corner(board.board)

    red_val = calc(red_pawns, red_kings, r_pawn, r_king, r_mov, r_k_mov, red_distance, red_unnocupied, red_defenders, red_atck, red_central, red_k_central, red_main, red_main_k, secondary_red, secondary_red_kings, red_loners, red_loners_k, red_holes, triangle_red, oreo_red, bridge_red, dog_red, red_corner, red_corner_k)
    blue_val = calc(blue_pawns, blue_kings, b_pawn, b_king, b_mov, b_k_mov, blue_distance, blue_unnocupied, blue_defenders, blue_atck, blue_central, blue_k_central, blue_main, blue_main_k, secondary_blue, secondary_blue_kings, blue_loners, blue_loners_k, blue_holes, triangle_blue, oreo_blue, bridge_blue, dog_blue, blue_corner, blue_corner_k)


    return red_val - blue_val





def calc(pawns, kings, safe_pawns, safe_kings, moveable_pawns, moveable_kings, prom_distance, unnocupied_promotion, defenders, attackers, central_pawns, central_kings, main_pawns, main_kings, second_pawns, second_kings, loner_pawns, loner_kings, holes, triangle, oreo, bridge, dog, corner_pawns, corner_kings):
    return (
        pawns + kings + safe_pawns +  safe_kings + moveable_pawns + 7*moveable_kings - prom_distance +  unnocupied_promotion +  defenders +  attackers +  central_pawns+  central_kings+  main_pawns+  main_kings+  second_pawns+ second_kings+ loner_pawns+ loner_kings+ holes+ 5*triangle + 5*oreo+ bridge+ 5*dog+ corner_pawns+ corner_kings)



def check_piece_in_the_corner(board):
    red_corner= 0
    blue_corner=0
    red_corner_k=0
    blue_corner_k = 0
    
    x,y = (0, 7) #red
    z, c = (7, 0) #blue

    if board[x][y] != 0:
        pc = board[x][y]
        if pc.color == RED:
            if pc.ch:
                red_corner_k = 1
            else:
                red_corner = 1

    if board[z][c] != 0:
        pc = board[z][c]
        if pc.color == BLUE:
            if pc.ch:
                blue_corner_k = 1
            else:
                blue_corner = 1
    return red_corner, blue_corner, red_corner_k, blue_corner_k



def check_bridge_dog(color, board, d = False):
    if d: 
        dog_col = dog[color]
        x, y = dog_col[0]
        z, c = dog_col[1]
        if board[x][y] != 0 and board[z][c] !=0:
            if board[x][y].color == color and board[z][c].color != color:
                return True
        return False

    #check for bridge

    bridge_col = bridge[color]
    x, y = bridge_col[0]
    z, c = bridge_col[1]

    if board[x][y] != 0 and board[z][c] !=0: 
        if board[x][y].color == color and board[z][c].color == color:
            return True
    return False

def check_triangle_oreo(color, x, y, board):
    if board[x][y] != 0:
        if board[x][y].color == color:
            return True
    return False

def check_for_patterns(board):
    red_tr = 1
    blue_tr = 1
    red_or= 1
    blue_or=1 
    red_d= 1
    blue_d= 1
    red_b= 1 
    blue_b = 1

    for i in range(0, 3):
        red_t_x, red_t_y = triangle_red[i]
        blue_t_x, blue_t_y = triangle_blue[i]
        red_o_x, red_o_y = oreo_red[i]
        blue_o_x, blue_o_y = oreo_blue[i]
        
        
        if not check_triangle_oreo(RED, red_t_x, red_t_y, board):
            red_tr = 0 

        if not check_triangle_oreo(BLUE, blue_t_x, blue_t_y, board):
            blue_tr = 0

        if not check_triangle_oreo(RED, red_o_x, red_o_y, board):
            red_or = 0
        
        if not check_triangle_oreo(BLUE, blue_o_x, blue_o_y, board):
            blue_or = 0
        

    if not check_bridge_dog(RED, board, True):
        red_d = 0
    
    if not check_bridge_dog(BLUE, board, True):
        blue_d = 0
    
    if not check_bridge_dog(RED, board):
        red_b = 0
    
    if not check_bridge_dog(BLUE, board):
        blue_b = 0
    
    return red_tr,blue_tr,red_or,blue_or, red_d,blue_d,red_b,blue_b


def count_holes(board, color):
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  
    
    num_holes = 0
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:  
                same_color_count = 0
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    if (0<=x<=7) and (0<=y<=7):
                        if board[x][y] != 0:
                            if 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y].color == color:
                                same_color_count += 1
                if same_color_count >= 3:
                    num_holes += 1
                    
    return num_holes


def generate_neighbours(row, col, board):
    neighbours = [ (row - 1, col - 1)
    ,(row- 1, col)
    , (row - 1, col + 1)
    , (row, col - 1)
    ,(row, col + 1)
    , (row + 1, col -1)
    ,(row + 1, col)
    , (row  +1, col +1)]
    
    loner = False
    
    for item in neighbours:
        if (0<= item[0] <= 7) and (0<=item[1]<=7):
            if board[item[0]][item[1]] != 0:
                loner = True
    return loner

def check_loner_pawns(board):
    red_loners = 0
    blue_loners = 0
    red_loners_k = 0
    blue_loners_k = 0

    for row in board:
        for item in row:
            if item != 0:
                is_loner = generate_neighbours(item.row, item.col, board)
                if is_loner:
                    if not item.ch:
                        if item.color == RED:
                            red_loners += 1
                        else:
                            blue_loners += 1
                    else:
                        if item.color == RED:
                            red_loners_k += 1
                        else:
                            blue_loners_k += 1

    
    return red_loners, blue_loners, red_loners_k, blue_loners_k


def check_if_in(board, x, y, red_num, blue_num ,red_king, blue_king):
    if board[x][y] != 0:
        pc = board[x][y]
        if not pc.ch:
            
            if pc.color == RED:
                red_num += 1
            elif pc.color == BLUE:
                blue_num +=1 
        else:
            if pc.color == RED:
                red_king += 1
            elif pc.color == BLUE:
                blue_king +=1 
    return red_num, blue_num ,red_king, blue_king

def get_central_main_sec_diagonal_pcs(board):
    red_central = 0
    blue_central = 0
    red_k_central = 0
    blue_k_central = 0
    red_main = 0
    blue_main = 0
    red_main_k = 0
    blue_main_k = 0
    secondary_red= 0
    secondary_blue = 0
    secondary_red_kings = 0
    secondary_blue_kings = 0


    for i in range(0, 8):
        x, y = center_values[i]
        z, c = main_diagonal[i]
        f, h = second_diagonal[i]


        red_central, blue_central, red_k_central, blue_k_central = check_if_in(board, x, y, red_central, blue_central, red_k_central, blue_k_central)
        red_main, blue_main, red_main_k, blue_main_k = check_if_in(board, z, c, red_main, blue_main, red_main_k, blue_main_k)
        secondary_red, secondary_blue, secondary_red_kings, secondary_blue_kings = check_if_in(board, f, h, secondary_red, secondary_blue, secondary_red_kings, secondary_blue_kings)

    return red_central, red_k_central, blue_central, blue_k_central, red_main, blue_main, red_main_k, blue_main_k, secondary_red, secondary_blue, secondary_red_kings, secondary_blue_kings



def get_atck_pieces(board):
    blue_attackers = 0
    red_attackers = 0

    for i in range(0, 24):
        x, y = blue_attacking_positions[i]
        z, c = red_attacking_positions[i]

        if board[x][y] != 0:
            pc = board[x][y]
            if pc.color == BLUE and not pc.ch:
                blue_attackers += 1
        
        if board[z][c] != 0:
            pc  = board[z][c]
            if pc.color == RED and not pc.ch:
                red_attackers += 1

        return red_attackers, blue_attackers

def get_def_pieces(board):
    red_defenders = 0
    blue_defenders = 0

    for i in range(0, 16):
        x, y = red_defender_pos[i]  
        z, c = blue_defender_pos[i]

        if board.board[x][y] != 0:
            if board.board[x][y].color == RED and not board.board[x][y].ch:
                red_defenders += 1
        if board.board[z][c] != 0:
            if board.board[z][c].color == BLUE and not board.board[z][c].ch:
                blue_defenders += 1
    

    return red_defenders, blue_defenders


def get_distance_to_promotion(board):
    red_distance = 0
    blue_distance = 0

    for row in board.board:
        for piece in row:
            if piece != 0:
                if piece.color == RED and not piece.ch:
                    dist = 7 - piece.row
                    red_distance += dist
                elif piece.color == BLUE and not piece.ch:
                    dist = piece.row - 0
                    blue_distance += dist
    return red_distance, blue_distance


def get_moveable(board):
    mov_r = 0
    mov_b = 0
    mov_r_k = 0
    mov_b_k = 0
    
    D_COL.collect_all_moves(board)
    for row in board.board:
        for piece in row:
            moveable_piece = False
            if piece != 0:
                
                for moveset in board.moves[(piece.row, piece.col)]:
                    if len(moveset) == 1:
                        moveable_piece = True
                if moveable_piece and piece.color == RED:
                    if  piece.ch:
                        mov_r_k += 1
                    else:
                        mov_r +=1
                elif moveable_piece and piece.color == BLUE:
                    if  piece.ch:
                        mov_b_k += 1
                    else:
                        mov_b +=1
    return mov_r, mov_b, mov_r_k, mov_b_k



def get_edge(board):
    r_pawn = 0
    r_king = 0
    b_pawn = 0
    b_king = 0


    for row in board.board:
        for piece in row:
            
            if piece != 0:
                coordinates = (piece.row, piece.col)
                if piece.color == RED and (coordinates in edge_positions):
                
                    if piece.ch:
                        r_king += 1
                    else:
                        r_pawn +=1
                elif piece.color == BLUE and (coordinates in edge_positions):
                
                    if piece.ch:
                        b_king += 1
                    else:
                        b_pawn +=1
                

    return r_pawn, b_pawn, r_king, b_king


def unnocupied_promotion_fields(board):
    blue_prom_unnocupied = 0
    red_prom_unnocupied = 0
    for i in range(4):
        x, y = blue_base_positions[i]
        c, z = red_base_positions[i]
        if board.board[x][y] == 0:
            red_prom_unnocupied += 1
        if board.board[z][c] == 0:
            blue_prom_unnocupied += 1
    return red_prom_unnocupied, blue_prom_unnocupied
                

