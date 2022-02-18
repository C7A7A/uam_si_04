from Plants.plant import Plant


class Fallow(Plant):
    #value = 0
    grow_speed = 0
    plant_type = "fallow"

    def __init__(self):
        super().__init__()
