from models.board import Board
from ai_player.data_collecting import DataCollector

RED = (255, 0, 0)
BLUE = (0, 0, 255)

resp_message = {
    'message': 'NOT OVER',
    'value': True
}


class Node:

    def __init__(self):
        self.value = Board()
        self.heur_value = None
        self.children = []
        self.collector = DataCollector()
    def terminal(self):
        self.collector.collect_all_moves(self.value)
        if self.value.red_c == 0:
            resp_message['message'] = "GAME OVER, BLUE WINS!"
            resp_message['value'] = True
            return resp_message
        elif self.value.blue_c == 0:
            resp_message['message'] = "GAME OVER, RED WINS!"
            resp_message['value'] = True            
            return resp_message
        elif self.check_moves(RED) == False:
            resp_message['message'] = "GAME OVER, BLUE WINS!"
            print("BLUE WINS")
            resp_message['value'] = True
            return resp_message
        elif self.check_moves(BLUE) == False:
            resp_message['message'] = "GAME OVER, RED WINS!"
            resp_message['value'] = True
            return resp_message
        else:
            resp_message['value'] = False
            return resp_message
    
    
    
    
    def check_moves(self, color):
        for row in self.value.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    if (piece.row, piece.col) in self.value.moves.keys():
                        if len(self.value.moves[(piece.row, piece.col)]) > 0:
                            return True
        return False
        



    def representation(self):
        print("\n\n-----------------")
        print("HEURISITC VALUE: ", self.heur_value )
        self.value.write_board()
        print("-----------------\n\n")