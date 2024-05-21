import pygame as pg
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from camera import Camera
from cube import Cube

class Floor:
    def __init__(self):
        pass

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(0, 1, 0)
        glVertex3f(-50, 0, -50)
        glVertex3f(50, 0, -50)
        glVertex3f(50, 0, 50)
        glVertex3f(-50, 0, 50)
        glEnd()

    def move(self, x, y, z):
        pass

    def rotate(self, yaw, pitch, roll):
        pass

    def apply(self):
        glBegin(GL_QUADS)
        glVertex3f(-50, 0, -50)
        glVertex3f(50, 0, -50)
        glVertex3f(50, 0, 50)
        glVertex3f(-50, 0, 50)
        glEnd()


def main():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)

    camera = Camera()
    camera.init()

    cube = Cube()
    floor = Floor()

    move_speed = 0.0
    acceleration = 0.01
    deceleration = 0.005

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        move_x = move_y = move_z = 0

        if keys[pg.K_w]:
            move_speed += acceleration
        elif keys[pg.K_s]:
            move_speed -= acceleration
        else:
            if move_speed > 0:
                move_speed -= deceleration
            elif move_speed < 0:
                move_speed += deceleration

        if keys[pg.K_a]:
            move_x += move_speed
        elif keys[pg.K_d]:
            move_x -= move_speed
        move_speed = min(max(move_speed, -0.3), 0.3)
        # Apply speed to movement
        move_z = move_speed
        cube.move(-move_x, 0, -move_z)
        camera.move(move_x, 0, move_z)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.apply()

        floor.draw()
        cube.draw()

        pg.display.flip()
        pg.time.wait(10)


if __name__ == "__main__":
    main()

