import pygame
import sys

# Inicialização do Pygame
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Cores
WHITE = (255, 255, 255)

tile_terra = pygame.image.load('terra.png')
tile_grama = pygame.image.load('grama.png')
tile_pbaixo = pygame.image.load('tile2.png')
tile_gelo = pygame.image.load('gelo.png')
# Dimensões dos tiles
TILE_WIDTH, TILE_HEIGHT = tile_terra.get_width(), tile_terra.get_height()

# Função para carregar o mapa de um arquivo
def carregar_mapa(arquivo):
    with open(arquivo, 'r') as f:
        mapa = [line.strip() for line in f.readlines()]
    return mapa

mapa = carregar_mapa("mapa.txt")
map_width, map_height = len(mapa[0]), len(mapa)

def to_isometric(x, y):
    iso_x = x * TILE_WIDTH / 2 - y * TILE_WIDTH / 2
    iso_y = x * TILE_HEIGHT / 2 + y * TILE_HEIGHT / 2
    return iso_x, iso_y

def draw_map(offset_x, offset_y):
    for y, linha in enumerate(mapa):
        for x, char in enumerate(linha):
            tile_type = char[0]
            try:
                tile_height = int(char[1])  # Assume que a altura é o segundo caractere
            except IndexError:
                tile_height = 0  # Se não houver segundo caractere, assume-se altura 0

            if tile_type == 'X':
                tile_image = tile_terra
            elif tile_type == 'A':
                tile_image = tile_grama
            elif tile_type == 'M':
                tile_image = tile_pbaixo
            elif tile_type == 'G':
                tile_image = tile_gelo
            else:
                continue
            
            iso_x, iso_y = to_isometric(x, y)
            
            screen.blit(tile_image, (int(iso_x + offset_x), int(iso_y + offset_y)))

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

def calculate_iso_camera_offset_corrected(personagem):
    center_x, center_y = to_isometric(personagem.x, personagem.y)
    offset_x = SCREEN_WIDTH / 2 - (center_x + TILE_WIDTH / 2)
    offset_y = SCREEN_HEIGHT / 2 - (center_y + TILE_HEIGHT / 2)
    return offset_x, offset_y

def draw_player(offset_x, offset_y, personagem):
    sprite_atual = personagem.get_sprite_atual()
    iso_x, iso_y = to_isometric(personagem.x, personagem.y)
    screen.blit(sprite_atual, (int(iso_x + offset_x), int(iso_y + offset_y)))

jogador = PersonagemAnimado(5, 5, 0.1)

def run_corrected():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jogador.mover('esquerda')
        elif keys[pygame.K_RIGHT]:
            jogador.mover('direita')
        elif keys[pygame.K_UP]:
            jogador.mover('cima')
        elif keys[pygame.K_DOWN]:
            jogador.mover('baixo')
        else:
            jogador.parar()

        jogador.atualizar()
        screen.fill(WHITE)
        offset_x, offset_y = calculate_iso_camera_offset_corrected(jogador)
        draw_map(offset_x, offset_y)
        draw_player(offset_x, offset_y, jogador)

        pygame.display.flip()
        clock.tick(60)

run_corrected()
