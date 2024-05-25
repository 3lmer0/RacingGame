from collisions import *
import numpy as np

class Barriers:

    def __init__(self):
        rect1 = CollisionRect(
            pos = np.array([0.0, 0.0]),
            w = 50,
            h = 50
        )

