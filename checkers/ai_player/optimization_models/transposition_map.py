import json


class TranspositionMap:
    def __init__(self):
        self.read_map()
        

    def save(self, hash_val, depth, eval):
        self.map[hash_val] = (depth, eval)
    

    def get(self, hash_val, depth):
        if hash_val in self.map:
            s_depth, evaluation = self.map[hash_val]
            if s_depth >= depth:
                return evaluation
        return None
    
    def write_map(self):
        with open('GameMem.json', 'w') as json_file:
            json.dump(self.map, json_file, indent=4)

    def read_map(self):
        with open('GameMem.json', 'r') as json_file:
            self.map = json.load(json_file)
