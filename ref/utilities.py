
def calculate_iso_camera_offset_corrected(personagem, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, TILE_HEIGHT):
    from map_loader import to_isometric
    center_x, center_y = to_isometric(personagem.x, personagem.y)
    offset_x = SCREEN_WIDTH / 2 - (center_x + TILE_WIDTH / 2)
    offset_y = SCREEN_HEIGHT / 2 - (center_y + TILE_HEIGHT / 2)
    return offset_x, offset_y