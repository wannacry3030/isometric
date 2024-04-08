
import pygame
from config import TILE_WIDTH, TILE_HEIGHT

# Dicionário para associar caracteres a imagens de tiles
tile_images = {
    'X': pygame.image.load('terra.png'),
    'A': pygame.image.load('grama.png'),
    'M': pygame.image.load('tile2.png'),
    'G': pygame.image.load('gelo.png'),
}

def carregar_mapa(arquivo):
    with open(arquivo, 'r') as f:
        mapa = [line.strip() for line in f.readlines()]
    return mapa

def to_isometric(x, y):
    iso_x = x * TILE_WIDTH / 2 - y * TILE_WIDTH / 2
    iso_y = x * TILE_HEIGHT / 2 + y * TILE_HEIGHT / 2
    return iso_x, iso_y

def draw_map(screen, mapa, offset_x, offset_y):
    for y, linha in enumerate(mapa):
        for x, char in enumerate(linha):
            tile_type = char[0]
            try:
                tile_height = int(char[1])  # Assume que a altura é o segundo caractere
            except IndexError:
                tile_height = 0  # Se não houver segundo caractere, assume-se altura 0

            if tile_type in tile_images:
                tile_image = tile_images[tile_type]
                iso_x, iso_y = to_isometric(x, y)
                screen.blit(tile_image, (int(iso_x + offset_x), int(iso_y + offset_y)))
