import pygame as pg
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *

class Camera:
    def __init__(self):
        self.x = 0
        self.y = -5
        self.z = -10
        self.yaw = 0
        self.pitch = 20
        self.roll = 0

    def init(self):
        glMatrixMode(GL_PROJECTION)
        gluPerspective(50, (800/600), 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def rotate(self, yaw, pitch, roll):
        self.yaw += yaw
        self.pitch += pitch
        self.roll += roll

    def look_at(self, target_x, target_y, target_z):
        gluLookAt(self.x, self.y, self.z, target_x, target_y, target_z, 0, 1, 0)

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def apply(self):
        glLoadIdentity()  # Reset transformations
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)
        glTranslatef(self.x, self.y, self.z)
