from collisions import *
import numpy as np

class Barriers:

    def __init__(self):
        rects_data = [
            {"pos": np.array([49.95, -36.45]), "w": 47.6, "h": 5}, # h = height when viewed from ang = 0, w = width when viewed from ang = 0   
            {"pos": np.array([28.05, -54.83]), "w": 3.8, "h": 41.75},
            {"pos": np.array([50.6, -73.73]), "w": 48.9, "h": 3.95},
            {"pos": np.array([72.3, -67.65]), "w": 5.3, "h": 16.1},
            {"pos": np.array([55.35, -61.58]), "w": 39.4, "h": 4.15},
            {"pos": np.array([39.38, -56.18]), "w": 7.45, "h": 14.95},
            {"pos": np.array([54.75, -50.58]), "w": 38.2, "h": 3.75},
            {"pos": np.array([70.56, -46.8]), "w": 6.55, "h": 11.3},
            {"pos": np.array([69.15, -36.48]), "w": 9.36, "h": 8.96},
            # Add more rects data here
            {"pos": np.array([57.8, -73.78]), "w": 0.4, "h": 8.96}, # Finish line
        ]

        self.rects = [CollisionRect(**data) for data in rects_data]