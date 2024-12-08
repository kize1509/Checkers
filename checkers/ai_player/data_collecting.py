from models.piece import Piece


RED = (255, 0, 0)
BLUE = (0, 0, 255)


class DataCollector:
    
    def __init__(self):
        self.playbook_red = {}
        self.playbook_blue = {}
        self.current_play = 1
        
    def collect_all_moves(self, board):
        
        for row in board.board:

            for square in row:
                if square != 0:   
                    board.moves[(square.row, square.col)] = self.calculate_moves(square, board)        

            blue_plays = {}
            red_plays = {}

            for position in board.moves:
                x, y = position
                values = board.moves[position]
                if board.board[x][y] != 0:

                    if board.board[x][y].color == BLUE:
                        blue_plays[(x,y)]= values
                    else:
                        red_plays[(x,y)] = values 
                
            self.playbook_blue = blue_plays
            self.playbook_red = red_plays

    

    def calculate_moves(self, piece, board):
        return self.calculate_diagonal_positions(piece, board)      
    
    
    def check_existing_pos(self, row, col):
        if( 0<=row<=7) and(0<=col<=7):
            return True
        return False




    def check_diagonal(self, board, direction, current_piece, num, recurent = False, mov = []):
        moves = []
        next_node_row = current_piece.row + direction
        next_node_col = current_piece.col + num
       
        


        if self.check_existing_pos(next_node_row, next_node_col):
            if board.board[next_node_row][next_node_col] == 0:
                if not recurent:
                    moves.append([(next_node_row, next_node_col)])
                else:
                    return moves
                
            elif board.board[next_node_row][next_node_col].color != current_piece.color:
                next_node_row += direction
                next_node_col += num
                if self.check_existing_pos(next_node_row, next_node_col):
                    if board.board[next_node_row][next_node_col] == 0:
                        
                        if not recurent:

                            moves.append([(next_node_row-direction, next_node_col-num), (next_node_row, next_node_col)])
                        
                        else:
                            moves.append((next_node_row-direction, next_node_col-num))
                            moves.append((next_node_row, next_node_col))

                        next_node = Piece(next_node_row, next_node_col, current_piece.color)
                        m1 = self.check_diagonal(board, direction, next_node, num, True, moves)
                        m2 = self.check_diagonal(board, direction, next_node, num*-1, True, moves)
                        
                        if not recurent:
                            moves[-1].extend(m1)
                            moves[-1].extend(m2)
                        else:
                            moves.extend(m1)
                            moves.extend(m2)
                       
                        return moves
        return moves

    def calculate_diagonal_positions(self, piece, board):
        moves = []
        if piece.color == BLUE or piece.ch:
            moves1 = self.check_diagonal(board, -1, piece, -1)
            moves2 = self.check_diagonal(board, -1, piece, 1)
            moves = moves1 + moves2 
        

        if piece.color == RED or piece.ch:
            moves1 = self.check_diagonal(board, 1, piece, -1)
            moves2 = self.check_diagonal(board, 1, piece, 1)
            moves = moves + moves1 + moves2
        
        return moves



    def present_move(self):
        print("PLAY NUMBER: ", self.current_play, "\n", "BLUE PLAYBOOK: \n" , self.playbook_blue, "\nRED PLAYBOOK: \n", self.playbook_red , "\n---------------------------------\n")

    def increment_the_play(self):
        self.current_play += 1