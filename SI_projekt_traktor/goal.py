from global_variables import *
import global_variables as glb
import random


class Goal:
    def __init__(self):
        self.goal = {}


    def create_goal(self, screen, pygame):
        VIDEO_INFO = pygame.display.Info()
        SCREEN_WIDTH, SCREEN_HEIGHT = VIDEO_INFO.current_w, VIDEO_INFO.current_h - 60
        # ilosci poszczegolnych upraw ustawiane z lapki
        amounts = {
            "carrot": random.randint(7, 10),
            "wheat": random.randint(7, 10),
            "tomato": random.randint(7, 10),
            "potato": random.randint(7, 10)
        }
        end_it = False
        while not end_it:
            screen.fill(BLACK)
            start_screen_font = pygame.font.SysFont("Britannic Bold", 40)
            amount_font = pygame.font.SysFont("Arial", 30)
            start_screen_text = start_screen_font.render("Crops to collect", True, (192, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    end_it = True

            screen.blit(start_screen_text, start_screen_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - (SCREEN_HEIGHT - 200))))
            x = 300
            for key in amounts:
                amount_txt = amount_font.render(key.capitalize() + ": " + str(amounts[key]), True, (192, 0, 0))
                screen.blit(amount_txt, amount_txt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - (SCREEN_HEIGHT - x))))
                x += 100
            pygame.display.flip()

        self.goal = amounts

    def edit_goal(self, type, amount):
        if self.goal[type] - amount <= 0:
            self.goal[type] = 0
        else:
            self.goal[type] -= amount

    def draw_goal(self, screen):
        goal = self.goal
        stats_font = pygame.font.SysFont('Times New Roman', 25)
        score_font = pygame.font.SysFont('Times New Roman', 25, bold=True)
        goal_font = pygame.font.SysFont('Times New Roman', 35, bold=True)

        screen.blit(goal_font.render(f"Goal", False, (218,165,32)), (WIDTH * SIZE, 70))
        i = 1
        for key in goal:
            text_surface = stats_font.render(f"{key.capitalize()}: {goal[key]}", False, BLACK)
            screen.blit(text_surface, (WIDTH * SIZE, 80 + i * 30))
            i += 1

    def is_goal_fulfilled(self):
        for key in self.goal:
            if self.goal[key] > 0:
                return False
        return True

    def next_goal(self):
        return max(self.goal, key=self.goal.get)


