from .Object3D import Object3D


class Dot3D(Object3D):
    def __init__(self, render, vertices='', edges='', **kwargs):
        super().__init__(render, vertices=vertices, edges=edges, **kwargs)
        self.draw_edges = False
        self.draw_faces = False
