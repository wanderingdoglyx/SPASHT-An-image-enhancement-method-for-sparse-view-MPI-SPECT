import numpy as np
import random
location_map=np.load('location_map.npy')
random_range=location_map.shape[0]


def location_coordinate():
    seed=random.randint(0,random_range-1)
    coordinate=location_map[seed]
    return coordinate
    