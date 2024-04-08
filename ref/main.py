import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, TILE_WIDTH, TILE_HEIGHT
from map_loader import carregar_mapa, draw_map, to_isometric
from personagem import PersonagemAnimado
from utilities import calculate_iso_camera_offset_corrected

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    mapa = carregar_mapa("mapa.txt")
    jogador = PersonagemAnimado(5, 5, 0.1)

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
        offset_x, offset_y = calculate_iso_camera_offset_corrected(jogador, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        draw_map(screen, mapa, offset_x, offset_y)
        sprite_atual = jogador.get_sprite_atual()
        iso_x, iso_y = to_isometric(jogador.x, jogador.y)
        screen.blit(sprite_atual, (int(iso_x + offset_x), int(iso_y + offset_y)))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    run_game()