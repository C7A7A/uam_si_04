from global_variables import *
import random


class Plant:
    value = 1
    grow_speed = 0
    is_growing = False
    plant_type = "plant"

    def __init__(self):
        self.grow_lvl = 0
        self.watered = False
        self.fertilized = False
        self.is_growing = False
        self.icon = eval(f'{self.__class__.__name__.lower()}_icon')
        self.neural_picture = None

    def draw(self, screen, x, y):
        screen.blit(self.icon, (x * SIZE, y * SIZE))
        #screen.blit(pygame.transform.scale(pygame.image.load(self.neural_picture), (SIZE, SIZE)), (x * SIZE, y * SIZE))
        # if self.watered:
        #     screen.blit(water, ((x * SIZE) + 2, (y * SIZE) + 2))

    def grow(self):
        self.is_growing = True
        # se walnąłem 30/speed bo grow_speed jest odwrotnie proporcjonalny
        # do ilości ruchów traktorka jakie potrzeba żeby dana roślina urosłą
        fully_grown_lvl = int(30 / self.grow_speed)
        if self.watered:
            water_boost = 0.7
            fully_grown_lvl = int(fully_grown_lvl * water_boost)

        if 0 <= self.grow_lvl < (fully_grown_lvl / 2):
            self.icon = eval(f'{self.__class__.__name__.lower()}_icon_small')
        elif (fully_grown_lvl / 2) <= self.grow_lvl < fully_grown_lvl:
            self.icon = eval(f'{self.__class__.__name__.lower()}_icon_medium')
        elif self.grow_lvl >= fully_grown_lvl:
            self.is_growing = False
            self.icon = eval(f'{self.__class__.__name__.lower()}_icon')

    def set_neural_picture(self):
        self.neural_picture = random.choice(eval(f'neural_{self.plant_type}'))

    # funkcje wywolywane przez traktor
    def water(self):
        self.watered = True

    def fertilize(self):
        self.fertilized = True
        self.icon = fallow_fertilized


