import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Cores
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

tile_images = {
    'X': pygame.image.load('terra.png'),
    'A': pygame.image.load('grama.png'),
    'M': pygame.image.load('pbaixo.png'),
    'G': pygame.image.load('gelo.png')
}

tile_size = 32
for key in tile_images:
    tile_images[key] = pygame.transform.scale(tile_images[key], (tile_size, tile_size))

selected_tile = 'X'

map_width, map_height = 20, 15
game_map = [['0' for _ in range(map_width)] for _ in range(map_height)]

def draw_map():
    for y in range(map_height):
        for x in range(map_width):
            tile_type = game_map[y][x]
            if tile_type in tile_images:
                screen.blit(tile_images[tile_type], (x * tile_size, y * tile_size))
            else:
                pygame.draw.rect(screen, GREY, (x * tile_size, y * tile_size, tile_size, tile_size))

def draw_palette():
    x_offset = map_width * tile_size + 20
    for i, (key, tile) in enumerate(tile_images.items()):
        screen.blit(tile, (x_offset, i * (tile_size + 10)))
        if key == selected_tile:
            pygame.draw.rect(screen, WHITE, (x_offset, i * (tile_size + 10), tile_size, tile_size), 2)

def save_map(file_name="saved_map.txt"):
    with open(file_name, 'w') as file:
        for row in game_map:
            file.write(''.join(row) + '\n')

def update_map(x, y):
    if x < map_width * tile_size:
        map_x, map_y = x // tile_size, y // tile_size
        if 0 <= map_x < map_width and 0 <= map_y < map_height:
            game_map[map_y][map_x] = selected_tile

def run():
    global selected_tile
    running = True
    mouse_pressed = False  # Rastrear se o mouse está pressionado para pintar
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                save_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Verifica se o clique foi na paleta
                if x >= map_width * tile_size:
                    selected_index = y // (tile_size + 10)
                    if selected_index < len(tile_images):
                        selected_tile = list(tile_images.keys())[selected_index]
                else:
                    mouse_pressed = True  # Ativa pintura se o clique foi no mapa
                    update_map(x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Verifica se o botão esquerdo do mouse foi solto
                    mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION and mouse_pressed:
                x, y = event.pos
                update_map(x, y)

        screen.fill(WHITE)
        draw_map()
        draw_palette()
        pygame.display.flip()

run()
pygame.quit()
sys.exit()
