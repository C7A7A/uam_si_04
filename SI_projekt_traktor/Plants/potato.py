from Plants.plant import *


class Potato(Plant):
    #value = 10
    grow_speed = 1
    plant_type = "potato"

    def __init__(self):
        super().__init__()
        self.set_neural_picture()
