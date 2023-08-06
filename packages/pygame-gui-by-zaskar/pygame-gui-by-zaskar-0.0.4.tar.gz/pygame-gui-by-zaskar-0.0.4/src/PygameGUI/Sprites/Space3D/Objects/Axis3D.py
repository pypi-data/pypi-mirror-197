from .Hollow3D import Hollow3D
import numpy as np


class Axis3D(Hollow3D):
    def __init__(self, render):
        super().__init__(render, [(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, -1, 1)], [(0, 1), (0, 2), (0, 3)])
        self.color_edges = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]).astype(np.uint32)
        self.draw_vertices = False
        self.label = 'XYZ'
