import global_variables as glb
from global_variables import *
from Plants.carrot import Carrot
from Plants.potato import Potato
from Plants.tomato import Tomato
from Plants.wheat import Wheat
from Plants.fallow import Fallow
from Plants.plant import Plant
from Buildings.building import Building
from Buildings.fertilizer import Fertilizer
from Buildings.seeds import Seeds
from Buildings.water import Water
from Buildings.crops import Crops
from Obstacles.obstacle import Obstacle
from Obstacles.stone import Stone
import math
import collections
import random
from goal import Goal
from queue import PriorityQueue
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree as tr
import tensorflow as tf
import pickle
import numpy as np


class Tractor:
    crops_capacity = 20
    fertilizer_capacity = 20
    water_capacity = 20
    seed_capacity = 20

    def __init__(self, data):
        self.x = 0
        self.y = 0
        self.crops = 0
        self.water = 0
        self.fertilizer = 0
        self.seeds = {
            'potato': 0,
            'carrot': 0,
            'tomato': 0,
            'wheat': 0
        }
        self.harvested = {
            Carrot: 0,
            Wheat: 0,
            Potato: 0,
            Tomato: 0
        }
        self.selected_seed = 'potato'
        self.watered_fields = {}
        self.fertilized_fields = {}
        self.plants_data = data
        self.building_positions = {
            "crops": (WIDTH // 2, WIDTH // 2),
            "water": (WIDTH // 2 - 1, WIDTH // 2),
            "fertilizer": (WIDTH // 2, WIDTH // 2 - 1),
            "seeds": (WIDTH // 2 - 1, WIDTH // 2 - 1)
        }
        self.icon = tractor_icon
        self.path = []
        self.orientation = 0
        self.prediction = None
        self.main_goal = Goal()
        self.decision_tree = self.import_decision_tree()
        self.neural_model = self.import_neural_model()

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.icon, (SIZE, SIZE)), (self.x * SIZE, self.y * SIZE))
        self.draw_prediction(screen)

    def draw_path(self, screen):
        # if len(self.path) > 0:
        #     for i in self.path:
        #         pygame.draw.rect(screen,GREEN,
        #                          pygame.Rect(i['state']['x'] * SIZE + SIZE/2, i['state']['y'] * SIZE + SIZE/2, 10, 10))
        pass

    @staticmethod
    def grow_timer(field):
        for row in field:
            for item in row:
                if isinstance(item, Plant) and not isinstance(item, Fallow) and item.is_growing:
                    item.grow_lvl += 1
                    item.grow()

    def rotate(self):
        if self.orientation == 0:
            self.icon = tractor_icon
        elif self.orientation == 90:
            self.icon = pygame.transform.rotate(tractor_icon, -90)
        elif self.orientation == 180:
            self.icon = pygame.transform.flip(tractor_icon, True, False)
        elif self.orientation == 270:
            self.icon = pygame.transform.rotate(pygame.transform.flip(tractor_icon, False, True), 90)

    def right(self, field):
        self.orientation = (self.orientation + 90) % 360
        self.rotate()
        self.grow_timer(field)

    def left(self, field):
        self.orientation = (self.orientation - 90) % 360
        self.rotate()
        self.grow_timer(field)

    def forward(self, field):
        if self.orientation == 0:
            if self.x < WIDTH - 1:
                self.x += 1
        elif self.orientation == 90:
            if self.y < HEIGHT - 1:
                self.y += 1
        elif self.orientation == 180:
            if self.x > 0:
                self.x -= 1
        elif self.orientation == 270:
            if self.y > 0:
                self.y -= 1
        self.grow_timer(field)

    def harvest(self, field):
        if isinstance(field[self.x][self.y], Plant) and not field[self.x][self.y].is_growing:
            if self.crops < self.crops_capacity:
                self.harvested[field[self.x][self.y].__class__] += 1
                field[self.x][self.y] = Fallow()
                self.crops += 1
                self.grow_timer(field)

    def water_field(self, field):
        if isinstance(field[self.x][self.y], Plant) and self.water >= 1 and not field[self.x][self.y].watered:
            str = "{},{}".format(self.x, self.y)
            self.watered_fields.update({str: [True, "czas nawodnienia w krokach", field[self.x][self.y].plant_type]})
            self.water -= 1
            field[self.x][self.y].water()
            self.grow_timer(field)

    def fertilize_field(self, field):
        if isinstance(field[self.x][self.y], Plant) and self.fertilizer >= 1 and not field[self.x][self.y].fertilized:
            str = "{},{}".format(self.x, self.y)
            self.fertilized_fields.update({str: [True, "czas nawodnienia w krokach", field[self.x][self.y].plant_type]})
            field[self.x][self.y].fertilize()
            self.fertilizer -= 1
            self.grow_timer(field)

    def refill_seeds(self, field):
        if isinstance(field[self.x][self.y], Seeds):
            self.selected_seed = self.main_goal.next_goal()
            for seed in self.seeds:
                if seed != self.selected_seed:
                    self.seeds.update({seed: 0})
            self.seeds.update({self.selected_seed: self.seed_capacity})
            self.grow_timer(field)

    def refill_water(self, field):
        if isinstance(field[self.x][self.y], Water):
            self.water = Tractor.water_capacity

    def refill_fertilizer(self, field):
        if isinstance(field[self.x][self.y], Fertilizer):
            self.fertilizer = Tractor.fertilizer_capacity

    def put_in_magazine(self, field):
        if isinstance(field[self.x][self.y], Crops):
            for crop, num in self.harvested.items():
                glb.score += crop.value * num
                glb.stats[str(crop.__name__).lower()] += num
                self.harvested[crop] = 0
                self.main_goal.edit_goal(str(crop.__name__).lower(), num)
            self.crops = 0
            self.grow_timer(field)

    def plant_seeds(self, field):
        if isinstance(field[self.x][self.y], Plant):
            if self.seeds[self.selected_seed] and field[self.x][self.y].fertilized:
                field[self.x][self.y] = eval(self.selected_seed.capitalize())()
                field[self.x][self.y].grow()
                self.seeds[self.selected_seed] -= 1
            self.grow_timer(field)

    def succ(self, state, field):
        def edit_succ(action, **kwargs):
            a = {"state": dict(state)}
            for key, val in kwargs.items():
                a['state'][str(key)] = val
            a['action'] = action
            return a

        x, y, orient, fert, harv, wat, seed, crop = state['x'], state['y'], state['orientation'], state['fertilizer'], \
                                                    state[
                                                        'harvested'], state['water'], state['seeds'], state['crops']

        curr = field[x][y]

        ans = []
        forward = None
        if orient == 0 and x + 1 < WIDTH and not isinstance(field[x + 1][y], Obstacle):
            forward = edit_succ(self.forward, x=x + 1)
        elif orient == 90 and y + 1 < HEIGHT and not isinstance(field[x][y + 1], Obstacle):
            forward = edit_succ(self.forward, y=y + 1)
        elif orient == 180 and x - 1 >= 0 and not isinstance(field[x - 1][y], Obstacle):
            forward = edit_succ(self.forward, x=x - 1)
        elif orient == 270 and y - 1 >= 0 and not isinstance(field[x][y - 1], Obstacle):
            forward = edit_succ(self.forward, y=y - 1)
        if forward is not None:
            ans.append(forward)
        ans.append(edit_succ(self.right, orientation=(orient + 90) % 360))
        ans.append(edit_succ(self.left, orientation=(orient - 90) % 360))
        if isinstance(curr, Fertilizer):
            ans.append(edit_succ(self.refill_fertilizer, fertilizer=Tractor.fertilizer_capacity))
        elif isinstance(curr, Seeds):
            ans.append(edit_succ(self.refill_seeds, seeds=Tractor.seed_capacity))
        elif isinstance(curr, Water):
            ans.append(edit_succ(self.refill_water, water=Tractor.water_capacity))
        elif isinstance(curr, Crops) and not crop:
            ans.append(edit_succ(self.put_in_magazine, crops=True))
        elif not harv and isinstance(curr, Plant) and not isinstance(curr, Fallow) and not curr.is_growing \
                and seed > 0 and self.crops < Tractor.crops_capacity and wat > 0 and fert > 0:
            ans.append(edit_succ(self.ai_field, harvested=curr.plant_type))
        return ans

    def goal_fertilizer(self, state):
        if state['fertilizer'] == Tractor.fertilizer_capacity:
            return True
        return False

    def goal_seeds(self, state):
        if state['seeds'] == Tractor.seed_capacity:
            return True
        return False

    def goal_crops(self, state):
        if state['crops']:
            return True
        return False

    def goal_water(self, state):
        if state['water'] == Tractor.water_capacity:
            return True
        return False

    def goal_harvest(self, state):
        if state['harvested'] == self.main_goal.next_goal():
            return True
        return False

    def ai_field(self, field):
        self.neural_predict(field)
        self.harvest(field)
        self.fertilize_field(field)
        self.plant_seeds(field)
        self.water_field(field)

    def calculate_path(self, field):
        start = {
            "state": {
                "x": self.x,
                "y": self.y,
                "orientation": self.orientation,
                "fertilizer": self.fertilizer,
                "seeds": self.seeds[self.selected_seed],
                "water": self.water,
                "crops": False,
                "harvested": None,
            },
            "action": None,
            "parent": None,
            "priority": 0}

        new_goal = self.goal_crops if self.crops >= self.main_goal.goal[self.main_goal.next_goal()] else self.decide()
        self.path = self.a_star(new_goal, field, start, self.succ)

    def move(self, field):
        if len(self.path):
            # self.path.pop(0)['action'](field)
            self.path.pop(0)(field)
        else:
            self.calculate_path(field)

    def heuristics(self, elem, goal):
        x = elem['state']['x']
        y = elem['state']['y']
        if goal == self.goal_fertilizer:
            dest = self.building_positions['fertilizer']
        elif goal == self.goal_water:
            dest = self.building_positions['water']
        elif goal == self.goal_seeds:
            dest = self.building_positions['seeds']
        elif goal == self.goal_crops:
            dest = self.building_positions['crops']
        else:
            dest = (self.x, self.y)

        return manhattan((x, y), dest)
        # return int(math.dist((self.x, self.y), (x, y)))

    def priority(self, node, field, goal):
        x = node['state']['x']
        y = node['state']['y']
        if node['action'] == self.forward:
            value = field[x][y].value
        else:
            value = 0
        p = self.heuristics(node, goal) + value + 1
        node['priority'] = p + node['parent']['priority']

    def a_star(self, goal, field, start, succ):
        q = PriorityQueue()
        q.put((0, id(start), start))
        explored = []
        while not q.empty():
            elem = q.get()[2]
            if goal(elem['state']):
                arr = []
                while elem['parent']:
                    # arr.insert(0, elem)
                    arr.insert(0, elem['action'])
                    elem = elem['parent']
                return arr
            explored.append(elem['state'])
            for successor in succ(elem['state'], field):
                new_node = {'state': successor['state'], 'action': successor['action'], 'parent': elem}
                self.priority(new_node, field, goal)
                if new_node['state'] not in [nd[2]['state'] for nd in q.queue] and new_node['state'] not in explored:
                    q.put((new_node['priority'], id(new_node), new_node))
        return []

    def import_decision_tree(self):
        with open('tree_classifier.pkl', 'rb') as file:
            return pickle.load(file)

    def import_neural_model(self):
        return tf.keras.models.load_model('model')

    def decide(self):
        current = [[self.water, self.fertilizer, self.seeds[self.selected_seed], self.crops,
                    manhattan((self.x, self.y), self.building_positions["crops"])]]
        return eval(f'self.goal_{self.decision_tree.predict(current)[0]}')

    def neural_predict(self, field):
        plant = field[self.x][self.y]
        class_names = ['carrot', 'tomato', 'wheat', 'potato']
        img = tf.keras.preprocessing.image.load_img(
            plant.neural_picture, target_size=(180, 180))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        prediction = self.neural_model.predict(img_array)
        score = tf.nn.softmax(prediction[0])
        # print(f'Klasa: {plant.plant_type}\tPredykcja: {class_names[np.argmax(score)]} z pewnością: {np.max(score)}')
        self.prediction = {"label": class_names[np.argmax(score)], "score": np.max(score), "img": plant.neural_picture}

    def draw_prediction(self, screen):
        if self.prediction is not None:
            screen.blit(pygame.transform.scale(pygame.image.load(self.prediction['img']), (250, 250)),
                        (WIDTH * SIZE + 350, 200))
            label_surface = score_font.render(
                f"Prediction: {self.prediction['label']}, score: {self.prediction['score']}", False, BLACK)
            screen.blit(label_surface, (WIDTH * SIZE + 350, 150))


def manhattan(src, dest):
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])
