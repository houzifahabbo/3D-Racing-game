import pygame as pg
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *


class Cube:
    faces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (5, 7, 2, 1), (4, 0, 3, 6))
    vertices = [[1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1]]

    def __init__(self):
        pass

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(1, 0, 0)
        for face in self.faces:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def move(self, x, y, z):
        for vertex in self.vertices:
            vertex[0] += x
            vertex[1] += y
            vertex[2] += z

def calculate_cube_center(cube):
    # Calculate average of vertices along each axis
    avg_x = sum(v[0] for v in cube.vertices) / len(cube.vertices)
    avg_y = sum(v[1] for v in cube.vertices) / len(cube.vertices)
    avg_z = sum(v[2] for v in cube.vertices) / len(cube.vertices)
    return avg_x, avg_y, avg_z
