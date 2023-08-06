from .Object3D import Object3D


class Solid3D(Object3D):
    def __init__(self, render, vertices='', faces='', **kwargs):
        super().__init__(render, vertices=vertices, faces=faces, **kwargs)
        self.draw_vertices = False
        self.draw_edges = False