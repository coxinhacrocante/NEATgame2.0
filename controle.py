import pygame

class Controle:
    def __init__(self):
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse = pygame.mouse.get_pressed()
            self.key = pygame.key.get_pressed()
    def get_entradas(self):
            return self.mouse_pos, self.mouse, self.key
    def controle_direction(self):
        if self.key[pygame.K_w] == True:
            up = True
        else: up = False
        if self.key[pygame.K_a] == True:
            left = True
        else: left = False
        if self.key[pygame.K_s] == True:
            down = True
        else: down = False
        if self.key[pygame.K_d] == True:
            right = True
        else: right = False
        return left, right, up, down