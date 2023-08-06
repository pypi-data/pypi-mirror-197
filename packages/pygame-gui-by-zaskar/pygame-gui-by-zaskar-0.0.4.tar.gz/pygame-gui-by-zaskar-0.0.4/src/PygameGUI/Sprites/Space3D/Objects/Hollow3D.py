from .Object3D import Object3D


class Hollow3D(Object3D):
    def __init__(self, render, vertices='', edges='', **kwargs):
        super().__init__(render, vertices=vertices, edges=edges, **kwargs)
