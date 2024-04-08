
import pygame

class PersonagemAnimado:
    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.esta_movendo = False
        self.sprites = {
            'NE': [pygame.image.load('new.png'), pygame.image.load('new1.png')],
            'SE': [pygame.image.load('sew.png'), pygame.image.load('sew1.png')],
            'NO': [pygame.image.load('now.png'), pygame.image.load('now1.png')],
            'SO': [pygame.image.load('sow.png'), pygame.image.load('sow1.png')],
        }
        self.direcao_atual = 'SE'
        self.frame_atual = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.frame_rate = 300

    def atualizar(self):
        if self.esta_movendo:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_update > self.frame_rate:
                self.frame_atual = (self.frame_atual + 1) % len(self.sprites[self.direcao_atual])
                self.ultimo_update = agora

    def mover(self, direcao):
        self.esta_movendo = True
        if direcao == 'esquerda':
            self.x -= self.velocidade
            self.direcao_atual = 'NO'
        elif direcao == 'direita':
            self.x += self.velocidade
            self.direcao_atual = 'SE'
        elif direcao == 'cima':
            self.y -= self.velocidade
            self.direcao_atual = 'NE'
        elif direcao == 'baixo':
            self.y += self.velocidade
            self.direcao_atual = 'SO'

    def parar(self):
        self.esta_movendo = False

    def get_sprite_atual(self):
        return self.sprites[self.direcao_atual][self.frame_atual]
