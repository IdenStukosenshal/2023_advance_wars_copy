import pygame
from pygame.sprite import Group

from settings import Settings
import game_function_1


settings_obj = Settings()

def vidiya_game():

    pygame.init()
    screen = pygame.display.set_mode((settings_obj.screen_w, settings_obj.screen_h))
    pygame.display.set_caption('CooL_ViDiYa_GaMe')
    clock = pygame.time.Clock()

    map_elements = Group()

    file_name = "map_1.txt"
    game_function_1.create_map(file_name, settings_obj, screen, map_elements)



    while True:
        clock.tick(settings_obj.fps)

        game_function_1.check_events()

        #screen.fill((217, 245, 254))

        game_function_1.update_screen(map_elements,)

        pygame.display.flip()


vidiya_game()

