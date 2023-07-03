import pygame 
import time
import random
import math 
import os
import neat
import glob
from controle import Controle
from comida import Comida
from organismo import Organismo

WIN_X = 1600
WIN_Y = 900
GEN = 0

pygame.init()
pygame.font.init()
fonte_init = pygame.font.SysFont('comicsans', 20)


############## desenho

def draw_window(win, fruits, organs, vistos, gen):
    win.fill((0,0,0))
    for c in range(len(organs)):
        organs[c].draw(win, vistos)
    for c in range(len(fruits)):
        fruits[c].draw(win)
    pygame.display.update()

################ loop principal

def main(genomes, config):
    global GEN 
    GEN += 1
    nets = []
    ge = []
    org = []
    fruits = []

    for xx, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        org.append(Organismo(random.randint(0, WIN_X - 10), random.randint(0, WIN_Y - 10), WIN_X, WIN_Y))
        g.fitness = 0
        ge.append(g)
        
    len_fruits = 20
    for c in range(len_fruits):
        fruits.append(Comida(random.randint(0, WIN_X - 10), random.randint(0, WIN_Y - 10)))

    win  = pygame.display.set_mode((WIN_X, WIN_Y))
    pygame.display.set_caption('Se liga papai')
    clock = pygame.time.Clock()
    
    controlar = False
    id_org_mov = 0
    score = 0
    run = True
    visto = None

    while run:
        clock.tick(400)
        score += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(fruits) < len_fruits:
            fruits.append(Comida(random.randint(0, WIN_X - 10), random.randint(0, WIN_Y - 10)))


        vez_controlada = False
        entradas = Controle()
        mouse_pos, mouse, key = entradas.get_entradas()

        vistos = list()
        for_del = list()
        for c in range(len(org)):
            if c > len(org) - 1: continue 
            #------ controle de personagem
            if mouse[0] == True and vez_controlada == False:
                if org[c].retan.collidepoint(mouse_pos):
                    print(org[c].retan)
                    print(org[c].pos)
                    controlar = True
                    id_org_mov = c
                    vez_controlada = True
                else:
                    controlar = False

            visto = org[c].ver(org[:], fruits)
            vistos.append(visto)
            visto = visto[0]#temporário

            ge[c].fitness = org[c].fitness

            output = nets[c].activate((visto['vista'][0], visto['vista'][1], visto['x_neg'][0], visto['x_neg'][1], visto['x_pos'][0], visto['x_pos'][1],
                                                  visto['y_neg'][0], visto['y_neg'][1], visto['y_pos'][0], visto['y_pos'][1]))
            
            
            if output[0] > 0.5: left = True
            else: left = False
            if output[1] > 0.5: right = True
            else: right = False
            if output[2] > 0.5: up = True
            else: up = False
            if output[3] > 0.5: down = True
            else: down = False
            if output[4] > 0.5: comer = True
            else: comer = False
            if output[5] > 0.5: atacar = True
            else: atacar = False

            if comer == True:
                org[c].comer(fruits) 
            if atacar == True:
                for_del += org[c].atacar(org, for_del)

            #----- movimentação de personagem
            if c == id_org_mov and controlar == True:
                con_det = True
            else:
                con_det = False

            org[c].movimentar(left = left, right = right, up = up, down = down, controlar=con_det, comer = comer, atacar = atacar)

        draw_window(win = win, fruits = fruits, organs = org, vistos = vistos, gen = GEN)

        for_del.sort(reverse=True)
        for d in for_del:
            org.pop(d[0])

        if score > 200: break
    


        
################# parte do run (parece um decorador para o NEAT)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    '''para salvar o jogador vencedor depois é apenas necessários usar o picle, pois os dados podem ser salvos como json'''
    winner = p.run(main,  5000)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedfoward.txt')
    run(config_path)