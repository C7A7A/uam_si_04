from Plants.plant import Plant


class Carrot(Plant):
    #value = 3
    grow_speed = 3
    plant_type = "carrot"

    def __init__(self):
        super().__init__()
        self.set_neural_picture()
