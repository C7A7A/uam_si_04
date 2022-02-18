from Plants.plant import Plant


class Tomato(Plant):
    #value = 5
    grow_speed = 2
    plant_type = "tomato"

    def __init__(self):
        super().__init__()
        self.set_neural_picture()