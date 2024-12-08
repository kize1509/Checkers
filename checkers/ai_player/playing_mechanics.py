import copy
from models.piece import Piece
from ai_player.Node import Node
from ai_player.data_collecting import DataCollector
from ai_player.heuristic import heuristic_eval
from ai_player.optimization_models.zobrist_hash import Zobrist
from ai_player.optimization_models.transposition_map import TranspositionMap


BLUE = (0, 0, 255)
RED = (255, 0, 0)
GAME_STAGES = {'EARLY' : 4, 'MID' : 5, 'LATE' : 6}
INITIAL_PIECES = 24



class PlayerAi:
    
    def __init__(self):

        self.selected  = None
        self.turn = RED 
        self.root = Node()
        self.zobrist = Zobrist()
        self.trans_map = TranspositionMap()



    def board_analisys(self, core_board):
       
        current_pieces = core_board.blue_c + core_board.red_c

        stage_index = INITIAL_PIECES - current_pieces
        if stage_index < 6:
            return GAME_STAGES['EARLY']
        elif 12>=stage_index>=6:
            return GAME_STAGES['MID']
        else:
            return GAME_STAGES['LATE']


    def play(self, core, rootNode):
        
        
        self.root = rootNode
        self.root.value.blue_c, self.root.value.red_c, self.root.value.blue_k, self.root.value.red_k = core.board.blue_c, core.board.red_c, core.board.blue_k, core.board.red_k
        self.copy_table(core.board.board, self.root.value.board)
        
        print('\n------------COMING IN NODE------------\n')
        self.root.value.write_board()
        self.generate_children(self.root, True)
        self.root.value.display_moves()
        print('\n---------------------------------------\n')
        
        depth = self.board_analisys(self.root.value)

        eval, next_node = self.minimax(self.root, depth, -float('inf'), float('inf'), True)
        
        print('\n------------COMING OUT NODE------------\n')
        if next_node is not None:
            next_node.value.write_board()
            next_node.value.display_moves()
        else:
            print("No valid moves available!")

        print('\n---------------------------------------\n')

        return next_node 
    

    def generate_children(self, node, maximizer):
            
        color = RED    
        if not maximizer:
             color = BLUE

        collector = DataCollector()
        collector.collect_all_moves(node.value)
        if maximizer:

            moves_dict = copy.deepcopy(collector.playbook_red)
        else:
            moves_dict = copy.deepcopy(collector.playbook_blue) 
        
        nodes = []
        for row in node.value.board:
            
            for piece in row:

                if piece != 0:
                    
                    if piece.color == color:
                        if moves_dict.get((piece.row, piece.col)):
                            
                        
                            for move_set in moves_dict.get((piece.row, piece.col)):
                                
                                copied_piece = Piece(piece.row, piece.col, piece.color)
                                copied_piece.ch = piece.ch
                                nodes_from_piece = self.simulate_moves(copied_piece, move_set, node.value)
                                                        
                                nodes.extend(nodes_from_piece)
        node.children = nodes

    

    def copy_table(self, board_org, board_copy):
        for i in range(0, 8):
            for j in range(0, 8):
                if board_org[i][j] == 0:
                    board_copy[i][j] = 0
                else:
                    piece = board_org[i][j]
                    board_copy[i][j] = Piece(piece.row, piece.col, piece.color)
                    board_copy[i][j].ch = piece.ch


    def simulate_moves(self, current_piece, move_set, board):
        
        
        nodes = []
        if len(move_set) > 1:
            for i in range(1, len(move_set), 2):

                row, col = move_set[i]
                
                if (0<=row<=7) and (0<=col<=7):


                    new_node = Node()

                    self.copy_table(board.board, new_node.value.board)
        
                    new_node.value.blue_c, new_node.value.red_c, new_node.value.blue_k, new_node.value.red_k = board.blue_c, board.red_c, board.blue_k, board.red_k
                    new_node.value.moves = {}
                    piece_for_move = new_node.value.get_piece(current_piece.row, current_piece.col) 
                    
                    for del_item in move_set[:i]:
                        r, c = del_item
                        if new_node.value.board[r][c] != 0:
                            pc = new_node.value.board[r][c]
                            if pc.color == RED:
                                new_node.value.red_c -= 1
                                if pc.ch:
                                      new_node.value.red_k -= 1
                            else:
                                new_node.value.blue_c -= 1
                                if pc.ch:
                                      new_node.value.blue_k -= 1
                        
                        new_node.value.board[r][c] = 0

                    new_node.value.move(piece_for_move, row, col)
                    nodes.append(new_node)
        
        else:
            if len(move_set) == 1:
                row, col = move_set[0]
                if (0<=row<=7) and (0<=col<=7):
                    new_node = Node()
                
                    self.copy_table(board.board, new_node.value.board)

                    new_node.value.blue_c, new_node.value.red_c, new_node.value.blue_k, new_node.value.red_k = board.blue_c, board.red_c, board.blue_k, board.red_k

                    piece_for_move = new_node.value.get_piece(current_piece.row, current_piece.col) 
                    new_node.value.moves = {}
                    new_node.value.move(piece_for_move, row, col)
                    


                    nodes.append(new_node)

            
        return nodes
    

    

    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or node.terminal()['value']:
            return heuristic_eval(node.value), node

        h_val = self.zobrist.define_hash(node.value.board)
        evaluation = self.trans_map.get(h_val, depth)

        if evaluation is not None:
            return evaluation, node

        if maximizingPlayer:
            maxEval = -float('inf')
            best_child = None
            self.generate_children(node, maximizingPlayer)
            for child in node.children:
                eval_score, _ = self.minimax(child, depth - 1, alpha, beta, False)
                if eval_score > maxEval:
                    maxEval = eval_score
                    best_child = child
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self.trans_map.save(h_val, depth, maxEval)
            return maxEval, best_child
        else:
            minEval = float('inf')
            best_child = None
            self.generate_children(node, maximizingPlayer)
            for child in node.children:
                eval_score, _ = self.minimax(child, depth - 1, alpha, beta, True)
                if eval_score < minEval:
                    minEval = eval_score
                    best_child = child
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.trans_map.save(h_val, depth, minEval)
            return minEval, best_child