from Plants.plant import Plant


class Wheat(Plant):
    #value = 1
    grow_speed = 5
    plant_type = "wheat"

    def __init__(self):
        super().__init__()
        self.set_neural_picture()
