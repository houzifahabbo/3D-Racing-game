from OpenGL.GL import *
from objLoader import OBJ

class Car:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.obj = OBJ('car_object/Sedan.obj', swapyz=True)

    def loadObj(self):
        self.obj.generate()
        self.obj.render()

    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def get_position(self):
        return self.x, self.y, self.z

    def rotate(self, yaw, pitch, roll):
        self.yaw += yaw
        self.pitch += pitch
        self.roll += roll

    def apply(self):
        glLoadIdentity()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)