import pygame
import pathlib

pygame.init()
pygame.font.init()
VIDEO_INFO = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = VIDEO_INFO.current_w, VIDEO_INFO.current_h - 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
stats_font = pygame.font.SysFont('Times New Roman', 25)
score_font = pygame.font.SysFont('Times New Roman', 25, bold=True)
goal_font = pygame.font.SysFont('Times New Roman', 35, bold=True)

pygame.display.set_caption("TRAKTOR ROLNIK SIMULATOR", "WRRR")
clock = pygame.time.Clock()



### Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

### Game variables
SIZE = 48
WIDTH = 10
HEIGHT = 10
FPS = 10
stats = dict()
score = 0
start_timer_value = 1500
timer = start_timer_value

### pictograms
# tractor
tractor_icon = pygame.transform.scale(pygame.image.load('icons/tractor.png'), (SIZE, SIZE))
# water
water = pygame.transform.scale(pygame.image.load("icons/water.png"), (10,10))
## plants
# grown
wheat_icon = pygame.transform.scale(pygame.image.load('icons/plants/wheat.png'), (SIZE, SIZE))
potato_icon = pygame.transform.scale(pygame.image.load('icons/plants/potato.png'), (SIZE, SIZE))
carrot_icon = pygame.transform.scale(pygame.image.load('icons/plants/carrot.png'), (SIZE, SIZE))
tomato_icon = pygame.transform.scale(pygame.image.load('icons/plants/tomato.png'), (SIZE, SIZE))
fallow_icon = pygame.transform.scale(pygame.image.load('icons/plants/fallow.png'), (SIZE, SIZE))
# small
wheat_icon_small = pygame.transform.scale(pygame.image.load('icons/plants/growing/wheat_small.png'), (SIZE, SIZE))
potato_icon_small = pygame.transform.scale(pygame.image.load('icons/plants/growing/potato_small.png'), (SIZE, SIZE))
carrot_icon_small = pygame.transform.scale(pygame.image.load('icons/plants/growing/carrot_small.png'), (SIZE, SIZE))
tomato_icon_small = pygame.transform.scale(pygame.image.load('icons/plants/growing/tomato_small.png'), (SIZE, SIZE))
# medium
wheat_icon_medium = pygame.transform.scale(pygame.image.load('icons/plants/growing/wheat.png'), (SIZE, SIZE))
potato_icon_medium = pygame.transform.scale(pygame.image.load('icons/plants/growing/potato.png'), (SIZE, SIZE))
carrot_icon_medium = pygame.transform.scale(pygame.image.load('icons/plants/growing/carrot.png'), (SIZE, SIZE))
tomato_icon_medium = pygame.transform.scale(pygame.image.load('icons/plants/growing/tomato.png'), (SIZE, SIZE))
#fallow
fallow_fertilized = pygame.transform.scale(pygame.image.load('icons/plants/fallow_fertilized.png'), (SIZE, SIZE))
fallow = pygame.transform.scale(pygame.image.load('icons/plants/fallow.png'), (SIZE, SIZE))

## neural networks
path = pathlib.Path("Zdjecia_testowe")
neural_potato = list(path.glob('ziemniak/*'))
neural_carrot = list(path.glob('marchew/*'))
neural_tomato = list(path.glob('pomidor/*'))
neural_wheat = list(path.glob('pszenica/*'))
