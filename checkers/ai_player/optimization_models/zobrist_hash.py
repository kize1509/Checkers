import random
import json

#indexes : 1 - RED piece, 2 - BLUE piece, 3 - RED king, 4 - BLUE king

RED = (255, 0, 0)


class Zobrist:
    def __init__(self):
        self.board_size = 64
        self.piece_types = 5
        self.filename = 'KeysMem.json'
        self.h_val = 0
        self.read_from_file()

    def define_hash(self, board):
        self.h_val = 0
        for row in board:
            for item in row:
                if item != 0:
                    piece_index = self.set_index(item)
                    self.h_val ^= self.table[item.row * 8 + item.col][piece_index]
        return self.h_val
    
    
    def set_index(self, piece):
        if piece.color == RED:
            if piece.ch:
                return 3
            else:
                return 1
        else:
            if piece.ch:
                return 2
            else:
                return 4
    

    def write_to_file(self):
        with open(self.filename, 'w') as file:
            json.dump(self.table, file)

    def read_from_file(self):
        with open(self.filename, 'r') as file:
            table = json.load(file) 
            self.table= table