import pygame
from controle import Controle
import math
import time
import random

def zoom(tupla, zoom_n = 1):
    tupla = (int( tupla[0] * zoom_n ), int( tupla[1] * zoom_n))
    return tupla

class Organismo:
    def __init__(self, x, y, win_x, win_y):
        #tipos de orgãos
        self.corpo_principal = 1
        self.boca = 2
        self.escama = 3
        self.garra = 4
        
        #tipos de alimentos
        self.alimento = 5
        self.carne_fresca = 6

        #dados de player
        self.win_x = win_x
        self.win_y = win_y
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.tam_perso = zoom((10  , 10))
        self.id = random.randint(1, 100000)
        self.grid = (9, 9)

        #estatisticas de player
        self.raio_de_visao = 500
        self.vel = 9
        self.fitness = 0
        self.vida = 100
        self.fome = 100
        self.dano = 20

        #iniciação de player
        self.genoma_corpo = self.get_genoma_basic(self.grid)
        self.lista_pos_corpo = self.manifestar_genoma(self.genoma_corpo, id = self.id)
        self.retan_list = list()
        for c in range(len(self.genoma_corpo)):
            self.retan = self.lista_pos_corpo[c][1].get_rect(topleft = self.pos)
            self.retan_list.append(self.retan)
                

    def movimentar(self, left=False, right=False, up=False, down=False, controlar = False, comer = False, atacar = False):
        if controlar == True:
            con = Controle()
            left, right, up, down = con.controle_direction()

        if left == True :
            if self.pos[0] > 0:
                self.pos = (self.pos[0] - self.vel, self.pos[1])
            else:
                self.fitness -= 1
        if right == True:
            if self.pos[0] < self.win_x - self.tam_perso[0]:
                self.pos = (self.pos[0] + self.vel, self.pos[1])
            else:
                self.fitness -= 1
        if up == True: 
            if self.pos[1] > 0:
                self.pos = (self.pos[0], self.pos[1] - self.vel)
            else:
                self.fitness -= 1
        if down == True: 
            if self.pos[1] < self.win_y - self.tam_perso[1]:
                self.pos = (self.pos[0], self.pos[1] + self.vel)
            else:
                self.fitness -= 1

        self.retan_list = list()
        for c in range(len(self.genoma_corpo)):
            self.lista_pos_corpo[c][0] = self.pos
            self.retan = self.lista_pos_corpo[c][1].get_rect(topleft = self.pos)
            self.retan_list.append(self.retan)

    def get_genoma_basic(self, grid):
        lista_pos_rel = [((grid[0]-1)//2+1, (grid[1]-1)//2+1, self.corpo_principal)]
        return lista_pos_rel
    
    def manifestar_genoma(self, genoma, id):
        lista_pos_corpo = []
        for d in range(len(genoma)):
                if genoma[d][2] == self.corpo_principal:
                    gen_corpo_prin = genoma[d]

        for c in range(len(genoma)):
            pos_rel_x = genoma[c][0] - gen_corpo_prin[0]
            pos_rel_y = genoma[c][1] - gen_corpo_prin[1]
            offset_x = pos_rel_x * self.tam_perso[0]
            offset_y =  pos_rel_y * self.tam_perso[1]
            posicao = (self.pos[0] + offset_x, self.pos[1] + offset_y)


            corpo = pygame.surface.Surface(self.tam_perso)
            if genoma[c][2] == self.corpo_principal:
                corpo.fill((0, 255, 0))
            if genoma[c][2] == self.boca:
                corpo.fill((255, 0, 0))
            if genoma[c][2] == self.escama:
                corpo.fill((50, 50, 50))
            if genoma[c][2] == self.garra:
                corpo.fill((255, 255, 255))

            lista_pos_corpo.append([posicao, corpo, genoma[c][2], id])
        return lista_pos_corpo
    
    def ver(self, lista_de_organismos, lista_de_frutas = None, raio_de_visao = 200):
        self.raio_de_visao = raio_de_visao
        lista_olhos = list()
        for c in range(len(self.lista_pos_corpo)):
            if self.lista_pos_corpo[c][2] == self.corpo_principal:
                lista_olhos.append(self.lista_pos_corpo[c][0])

        if lista_de_frutas != None: 
            for c in range(len(lista_de_frutas)):
                lista_de_organismos.append(lista_de_frutas[c])
                
        
        self.visto = list()
        for c in range(len(lista_olhos)):
            x_vista = lista_olhos[c][0] + self.tam_perso[0] // 2
            y_vista = lista_olhos[c][1] + self.tam_perso[1] // 2
            dec_x_pos = list()
            dec_x_neg = list()
            dec_y_pos = list()
            dec_y_neg = list()

            for d in range(len(lista_de_organismos)):
                if lista_de_organismos[d].id == self.lista_pos_corpo[0][3]: continue
                lpc = lista_de_organismos[d].lista_pos_corpo
                tam = lista_de_organismos[d].tam_perso
                id = lista_de_organismos[d].id

                for e in range(len(lpc)):
                    if y_vista >=  lpc[e][0][1] and y_vista <= lpc[e][0][1] + tam[1]: #avistado lateralmente
                        if x_vista > lpc[e][0][0]: #avistado pela esquerda
                            dist = -abs(lpc[e][0][0] - x_vista)
                            if abs(dist) < self.raio_de_visao:
                                dec_x_neg.append((dist, lpc[e][2], id))
                        if x_vista < lpc[e][0][0]: #avistado pela direta
                            dist = abs(x_vista - lpc[e][0][0])
                            if abs(dist) < self.raio_de_visao:
                                dec_x_pos.append((dist, lpc[e][2], id))
                    if x_vista >= lpc[e][0][0] and x_vista <= lpc[e][0][0] + tam[0]: #avistando verticalmente
                        if y_vista > lpc[e][0][1]: #avistado em cima
                            dist = -abs(lpc[e][0][1] - y_vista)
                            if abs(dist) < self.raio_de_visao:
                                dec_y_neg.append((dist, lpc[e][2], id))
                        if y_vista < lpc[e][0][1]: #avistado em baixo
                            dist = abs(y_vista - lpc[e][0][1])
                            if abs(dist) < self.raio_de_visao:
                                dec_y_pos.append((dist, lpc[e][2], id))
            dec_x_neg_fin = None
            dec_x_pos_fin = None
            dec_y_neg_fin = None
            dec_y_pos_fin = None
            if len(dec_x_neg) > 0: 
                dec_x_neg_fin = dec_x_neg[0]
                for d in range(len(dec_x_neg)):
                    if dec_x_neg[d][0] > dec_x_neg_fin[0]:
                        dec_x_neg_fin = dec_x_neg[d]
            else: dec_x_neg_fin = (0, 0, 0)

            if len(dec_x_pos) > 0:
                dec_x_pos_fin = dec_x_pos[0]
                for d in range(len(dec_x_pos)):
                    if dec_x_pos[d][0] < dec_x_pos_fin[0]:
                        dec_x_pos_fin = dec_x_pos[d]
            else: dec_x_pos_fin = (0, 0, 0)

            if len(dec_y_neg) > 0:
                dec_y_neg_fin = dec_y_neg[0]
                for d in range(len(dec_y_neg)):
                    if dec_y_neg[d][0] > dec_y_neg_fin[0]:
                        dec_y_neg_fin = dec_y_neg[d]
            else: dec_y_neg_fin = (0, 0, 0)

            if len(dec_y_pos) > 0:
                dec_y_pos_fin = dec_y_pos[0]
                for d in range(len(dec_y_pos)):
                    if dec_y_pos[d][0] < dec_y_pos_fin[0]:
                        dec_y_pos_fin = dec_y_pos[d]
            else: dec_y_pos_fin = (0, 0, 0)
            
            self.vistoo = {'vista':(x_vista, y_vista), 'x_neg':dec_x_neg_fin, 'x_pos':dec_x_pos_fin, 'y_neg':dec_y_neg_fin, 'y_pos':dec_y_pos_fin}

            self.visto.append(self.vistoo)
        return self.visto

    def comer(self, lista_de_comida):
        comestiveis = [self.alimento, self.carne_fresca]
        alvos = list()
        for viu in self.visto:
            for c in range(len(comestiveis)):
                if viu['x_neg'][1] == comestiveis[c]:
                    alvos.append(viu['x_neg'])
                if viu['x_pos'][1] == comestiveis[c]:
                    alvos.append(viu['x_pos'])
                if viu['y_neg'][1] == comestiveis[c]:
                    alvos.append(viu['y_neg'])
                if viu['y_pos'][1] == comestiveis[c]:
                    alvos.append(viu['y_pos'])
        if len(alvos) != 0:
            mais_prox = alvos[0]
            for c in range(len(alvos)):
                if abs(alvos[c][0]) < abs(mais_prox[0]):
                    mais_prox = alvos[c]

            a_deletar = list()
            for c in range(len(lista_de_comida)):
                if mais_prox[2] == lista_de_comida[c].id:
                    #print(f'deletando {c}')
                    a_deletar.append(c)
                    self.fitness += 10
        
            a_deletar.sort(reverse=True)
            
            for c in a_deletar:
                del lista_de_comida[c]

    def atacar(self, lista_de_organismos, for_del):
        atingiveis = [self.boca, self.corpo_principal]
        alvos = list()
        for viu in self.visto:
            for c in range(len(atingiveis)):
                if viu['x_neg'][1] == atingiveis[c]:     
                    alvos.append(viu['x_neg'])
                if viu['x_pos'][1] == atingiveis[c]:
                    alvos.append(viu['x_pos'])
                if viu['y_neg'][1] == atingiveis[c]:
                    alvos.append(viu['y_neg'])
                if viu['y_pos'][1] == atingiveis[c]:
                    alvos.append(viu['y_pos'])

        if len(alvos) != 0:
            mais_prox = alvos[0]
            for c in range(len(alvos)):
                if abs(alvos[c][0]) < abs(mais_prox[0]):
                    mais_prox = alvos[c]
            for_del = list()
            for c in range(len(lista_de_organismos)):
                if mais_prox[2] == lista_de_organismos[c].id:
                    lista_de_organismos[c].vida -= self.dano
                    #apagando jogadores mortos
                    for d in range(len(for_del)):
                        if for_del[d][1] != lista_de_organismos[c].id:
                            if lista_de_organismos[c].vida <= 0:
                                self.fitness += 10
                                for_del.append((c, lista_de_organismos[c].id))
            for_del.sort(reverse=True)
            return for_del
        return []

    def draw(self, win, vistos = None, ver_o_visto = True):
        for c in range(len(self.lista_pos_corpo)):
            win.blit(self.lista_pos_corpo[c][1], (self.lista_pos_corpo[c][0][0], self.lista_pos_corpo[c][0][1]))

        if vistos != None and ver_o_visto == True:
            for vistoss in vistos:
                for visto in vistoss:
                    if visto['x_neg'] != None:
                        pygame.draw.line(win, (255, 255, 255), visto['vista'], (visto['vista'][0] + visto['x_neg'][0], visto['vista'][1]))
                    else:
                        pygame.draw.line(win, (150, 150, 150), visto['vista'], (visto['vista'][0] - self.raio_de_visao, visto['vista'][1]))
                    if visto['x_pos'] != None:
                        pygame.draw.line(win, (255, 255, 255), visto['vista'], (visto['vista'][0] + visto['x_pos'][0], visto['vista'][1]))
                    else:
                        pygame.draw.line(win, (150, 150, 150), visto['vista'], (visto['vista'][0] + self.raio_de_visao, visto['vista'][1]))
                    if visto['y_neg'] != None:
                        pygame.draw.line(win, (255, 255, 255), visto['vista'], (visto['vista'][0] , visto['vista'][1] + visto['y_neg'][0]))
                    else:
                        pygame.draw.line(win, (150, 150, 150), visto['vista'], (visto['vista'][0], visto['vista'][1] - self.raio_de_visao))
                    if visto['y_pos'] != None:
                        pygame.draw.line(win, (255, 255, 255), visto['vista'], (visto['vista'][0], visto['vista'][1] + visto['y_pos'][0]))
                    else:
                        pygame.draw.line(win, (150, 150, 150), visto['vista'], (visto['vista'][0], visto['vista'][1] + self.raio_de_visao))
