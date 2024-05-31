from collisions import *
import numpy as np

class Barriers:

    def __init__(self):
        rect1 = CollisionRect(

            pos = np.array([49.95, -36.45]),
            w = 47.6,   #Height when viewed from ang = 0
            h = 5       #Width when viewed from ang = 0    
        )

        rect2 = CollisionRect(

            pos = np.array([28.05, -54.83]),
            w = 3.8, 
            h = 41.75 
        )

        rect3 = CollisionRect(

            pos = np.array([50.6, -73.73]),
            w = 48.9,
            h = 3.95
        )

        rect4 = CollisionRect(

            pos = np.array([72.3, -67.65]), 
            w = 5.3,
            h = 16.1
        )

        rect5 = CollisionRect(
            pos = np.array([55.35, -61.58]),
            w = 39.4,
            h = 4.15
        )

        rect6 = CollisionRect(
            
            pos = np.array([39.38, -56.18]),
            w = 7.45,
            h = 14.95
        )

        rect7 = CollisionRect(

            pos = np.array([54.75, -50.58]),
            w = 38.20,
            h = 3.75
        )

        rect8 = CollisionRect(
            pos = np.array([70.56, -46.80]),
            w = 6.55,
            h = 11.3
        )

        rect9 = CollisionRect(
            pos = np.array([69.15, -36.48]),
            w = 9.36,
            h = 8.96
        )


        self.rects = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9]

        self.finishLine = CollisionRect(
            pos = np.array([57.8, -73.78]),
            w = 0.4,
            h = 3.85
        )