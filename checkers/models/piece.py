import pygame

BLUE = (0, 0, 255)
crown = pygame.transform.scale(pygame.image.load('./asset data/crown.png'), (45, 25))

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.ch = False

        if self.color == BLUE:
            self.direction = -1

        else: 
            self.direction = 1

        
        self.x = 0
        self.y = 0
        self.get_position()


    def get_position(self):
        self.x = 80 * self.col + 80 // 2
        self.y = 80 * self.row + 80 // 2

    def become_ch(self):
        self.ch = True


    def draw_circle(self, win):
        pygame.draw.circle(win, (255,255,255), (self.x, self.y), 32)
        pygame.draw.circle(win, self.color, (self.x, self.y), 30)
        if self.ch:
            win.blit(crown, (self.x - crown.get_width()//2, self.y - crown.get_height()//2))
        


    def move(self, row, column):
        self.row = row
        self.col = column
        self.get_position()


    

    def __tostring__(self):
        return str(self.color)