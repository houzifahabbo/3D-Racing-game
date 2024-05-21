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
        self.pitch = 30
        self.roll = 0

    def init(self):
        glMatrixMode(GL_PROJECTION)
        gluPerspective(50, (800/600), 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # self.apply()

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



    def apply(self):
        glLoadIdentity()  # Reset transformations
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)
        glTranslatef(self.x, self.y, self.z)

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


class Floor:
    def __init__(self):
        pass

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(0, 1, 0)
        glVertex3f(-10, 0, -10)
        glVertex3f(10, 0, -10)
        glVertex3f(10, 0, 10)
        glVertex3f(-10, 0, 10)
        glEnd()

    def move(self, x, y, z):
        pass

    def rotate(self, yaw, pitch, roll):
        pass

    def apply(self):
        glBegin(GL_QUADS)
        glVertex3f(-10, 0, -10)
        glVertex3f(10, 0, -10)
        glVertex3f(10, 0, 10)
        glVertex3f(-10, 0, 10)
        glEnd()

def main():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)

    camera = Camera()
    camera.init()

    cube = Cube()
    floor = Floor()
    move_rate = 0.1

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        move_x = move_y = move_z = 0

        if keys[pg.K_w]:
            move_z = move_rate
        if keys[pg.K_s]:
            move_z = -move_rate
        if keys[pg.K_a]:
            move_x = move_rate
        if keys[pg.K_d]:
            move_x = -move_rate

        camera.move(move_x, 0, move_z)
        cube.move(-move_x, 0, -move_z)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.apply()  # Apply camera transformations

        floor.draw()
        cube.draw()

        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()
