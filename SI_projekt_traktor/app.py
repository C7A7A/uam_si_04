from global_variables import *
from init_variables import *
from helper_functions.draw import *
import global_variables as glb

running = True

def start_screen(msg):
    end_it = False
    while not end_it:
        screen.fill(BLACK)
        start_screen_font = pygame.font.SysFont("Britannic Bold", 40)
        start_screen_text = start_screen_font.render(msg, True, (192, 0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                end_it = True

        screen.blit(start_screen_text, start_screen_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
        pygame.display.flip()

def end_screen(msg):
    end_it = False
    while not end_it:
        screen.fill(BLACK)
        start_screen_font = pygame.font.SysFont("Britannic Bold", 40)

        for index, element in enumerate(msg.split(",")):
            end_screen_text = start_screen_font.render(element, True, (192, 0, 0))
            screen.blit(end_screen_text, end_screen_text.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + (index+1)*30)))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                end_it = True


        pygame.display.flip()


def draw():
    screen.fill((200, 200, 200))
    draw_scores()
    draw_grid()
    tractor.main_goal.draw_goal(screen)
    tractor.draw_path(screen)
    tractor.draw(screen)


start_screen("Hello, click LMB to start playing!")
tractor.main_goal.create_goal(screen, pygame)
while running:
    draw()
    tractor.move(field)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.USEREVENT:
            glb.timer -= 1
            if glb.timer == 0:
                running = False
    if tractor.main_goal.is_goal_fulfilled():
        running = False

    pygame.display.flip()

end_screen(f"Congratulations,You completed the task in: {str(glb.start_timer_value - glb.timer)} seconds.")
pygame.quit()
