from global_variables import *


class Building():
    value = 1000000
    def __init__(self, image):
        icon = pygame.image.load(f'icons/buildings/{image}.png')
        self.icon = pygame.transform.scale(icon, (SIZE - 2, SIZE -2))

    def draw(self, screen, x, y):
        screen.blit(self.icon, (x * SIZE, y * SIZE))
