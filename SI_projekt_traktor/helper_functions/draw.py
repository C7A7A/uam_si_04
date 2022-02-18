from global_variables import *
import global_variables as glb
from init_variables import *





pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT + 1, 250)


def draw_scores():
    score_surface = score_font.render(f"Score: {glb.score}", False, BLACK)
    screen.blit(score_surface, (WIDTH * SIZE, 0))
    screen.blit(stats_font.render(f"Time left: {glb.timer}", False, BLACK), (WIDTH * SIZE, score_surface.get_rect().height))



    # traktor
    screen.blit(score_font.render(f"Data", False, BLACK), (WIDTH * SIZE, 260))
    screen.blit(stats_font.render(f"Seed type: {tractor.selected_seed} Amount: {tractor.seeds[tractor.selected_seed]}",
                                  False, BLACK), (WIDTH * SIZE, 300))
    screen.blit(stats_font.render(f"Water capacity: {tractor.water}", False, BLACK), (WIDTH * SIZE, 330))
    screen.blit(stats_font.render(f"Fertilizer capacity: {tractor.fertilizer}", False, BLACK), (WIDTH * SIZE, 360))
    screen.blit(stats_font.render(f"Plants:", False, BLACK), (WIDTH * SIZE, 420))
    for i, (key, value) in enumerate(tractor.harvested.items()):
        text_surface = stats_font.render(f"{key.__name__}: {value}", False, BLACK)
        screen.blit(text_surface, (WIDTH * SIZE, 450 + i * 30))


def draw_grid():
    for x, row in enumerate(field):
        for y, element in enumerate(row):
            screen.blit(pygame.transform.scale(fallow, (SIZE, SIZE)), (x * SIZE, y * SIZE))
            if isinstance(element, Plant) or isinstance(element, Building) or isinstance(element, Obstacle):
                element.draw(screen, x, y)

def draw_prediction(image):
    screen.blit(image, WIDTH * SIZE, 700)

