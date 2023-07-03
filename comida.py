import random
import math
import pygame
import time

class Comida:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.tam_perso = (10,10)
        self.frutinha = 5
        self.fruta_corpo = pygame.surface.Surface(self.tam_perso)
        self.fruta_corpo.fill((255, 30, 30))
        self.id = random.randint(0,100000)
        self.lista_pos_corpo = list()
        self.lista_pos_corpo.append([self.pos, self.fruta_corpo, self.frutinha, self.id])
        self.fruta_rect = self.fruta_corpo.get_rect(topleft = self.pos)

    def draw(self, win):
        win.blit(self.fruta_corpo, self.fruta_rect)