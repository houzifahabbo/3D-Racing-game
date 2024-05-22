import pygame as pg
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from camera import Camera
from cube import Cube
from car import Car
from objLoader import OBJ
from math import *

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

# def movment(car, camera):



import pygame as pg
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from camera import Camera
from cube import Cube
from car import Car
from objLoader import OBJ
from math import sin, cos, radians

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

import pygame as pg
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from camera import Camera
from cube import Cube
from car import Car
from objLoader import OBJ
from math import sin, cos, radians

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
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))  # Ambient light
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))  # Diffuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

    camera = Camera()
    camera.init()

    floor = Floor()
    car = OBJ('car_object/Sedan.obj', swapyz=False)
    car.rotate(180, 0, 0)
    car.generate()

    move_speed = 0.0
    acceleration = 0.01
    deceleration = 0.005
    current_angle = 0.0  # Track the car's current rotation

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                car.free()
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        move_x = move_y = move_z = 0
        rotate_angle = 0

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
            rotate_angle = 2  # Rotate car to the left
        elif keys[pg.K_d]:
            rotate_angle = -2  # Rotate car to the right

        move_speed = min(max(move_speed, -0.3), 0.3)

        # Update the car's current angle
        current_angle += rotate_angle
        current_angle %= 360  # Keep the angle within [0, 360)

        # Calculate the movement based on the car's current angle
        move_x = move_speed * sin(radians(current_angle))
        move_z = move_speed * cos(radians(current_angle))

        car.move(-move_x, 0, -move_z)
        camera.move(move_x, 0, move_z)
        car.rotate(rotate_angle, 0, 0)


        # Update the camera position and orientation based on the car's position and rotation
        car_center = car.calculate_center()
        cam_distance = 10  # Distance behind the car
        cam_height = 5  # Height of the camera

        cam_x = car_center[0] - cam_distance * sin(radians(current_angle))
        cam_y = car_center[1] + cam_height
        cam_z = car_center[2] - cam_distance * cos(radians(current_angle))

        # camera.set_position(cam_x, cam_y, cam_z)
        camera.look_at(cam_x, cam_y, cam_z)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.apply()
        floor.draw()
        car.render()

        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()

