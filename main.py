import pygame as pg
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from camera import Camera
from objLoader import OBJ
from math import sin, cos, radians
from environment import Environment

class Floor:
    def __init__(self):
        pass

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(0, 0.5,0)
        glVertex3f(-100, -0.009, -100)
        glVertex3f(100, -0.009, -100)
        glVertex3f(100, -0.009, 100)
        glVertex3f(-100, -0.009, 100)
        glEnd()


def check_collision(car_position, trees, move_x, move_z):
    new_car_position = (car_position[0] + move_x, car_position[1], car_position[2] + move_z)
    for tree in trees:
        tp = tree.get_position()
        min_x = tp[0] - 2
        min_z = tp[2] - 2
        max_x = tp[0] + 2
        max_z = tp[2] + 2

        if (min_x < new_car_position[0] < max_x and min_z < new_car_position[2] < max_z):
            return True
    return False


def movement(car, camera, trees, state):
    keys = pg.key.get_pressed()
    rotate_angle = 0

    if keys[pg.K_w]:
        state["move_speed"] += state["acceleration"]
    elif keys[pg.K_s]:
        state["move_speed"] -= state["acceleration"]
    else:
        if state["move_speed"] > 0:
            state["move_speed"] -= state["deceleration"]
        elif state["move_speed"] < 0:
            state["move_speed"] += state["deceleration"]

    if abs(state["move_speed"]) > 0.005:  # Only allow rotation if the car is moving
        if keys[pg.K_a]:
            rotate_angle = 2  # Rotate car to the left
        elif keys[pg.K_d]:
            rotate_angle = -2  # Rotate car to the right

    state["move_speed"] = min(max(state["move_speed"], -0.3), 0.5)

    # Update the car's current angle only if rotate_angle is non-zero
    if rotate_angle != 0:
        state["current_angle"] += rotate_angle
        state["current_angle"] %= 360  # Keep the angle within [0, 360)

    # Calculate the movement based on the car's current angle
    move_x = state["move_speed"] * sin(radians(state["current_angle"]))
    move_z = state["move_speed"] * cos(radians(state["current_angle"]))

    car_position = car.get_position()

    # Check for collisions in the direction of movement
    if state["move_speed"] > 0:
        if not state["collision"][1]:
            state["collision"][0] = check_collision(car_position, trees, move_x, move_z)
            if state["collision"][0]:
                move_x = move_z = 0
                state["current_angle"] -= rotate_angle
                rotate_angle = 0
    elif state["move_speed"] < 0:
        if not state["collision"][0]:
            state["collision"][1] = check_collision(car_position, trees, move_x, move_z)
            if state["collision"][1]:
                move_x = move_z = 0
                state["current_angle"] -= rotate_angle
                rotate_angle = 0

    car.move(-move_x, 0, -move_z)
    if rotate_angle != 0:
        car.rotate(rotate_angle, 0, 0)

    # Update the camera position and orientation based on the car's position and rotation
    car_position = car.get_position()
    car_center = car.calculate_center()
    cam_distance = 10  # Distance behind the car
    cam_height = 5  # Height of the camera
    cam_x = car_position[0] + cam_distance * sin(radians(state["current_angle"]))
    cam_y = car_position[1] - cam_height
    cam_z = car_position[2] + cam_distance * cos(radians(state["current_angle"]))
    camera.set_position(-cam_x, cam_y, -cam_z)
    camera.set_yaw(-state["current_angle"])
    camera.look_at(car_center[0], cam_y, car_center[2])

def movement2(car, camera, trees, state):
    #use arrow keys to move the car
    keys = pg.key.get_pressed()
    rotate_angle = 0
    #USE ARROW KEYS TO MOVE THE CAR
    if keys[pg.K_UP]:
        state["move_speed"] += state["acceleration"]
    elif keys[pg.K_DOWN]:
        state["move_speed"] -= state["acceleration"]
    else:
        if state["move_speed"] > 0:
            state["move_speed"] -= state["deceleration"]
        elif state["move_speed"] < 0:
            state["move_speed"] += state["deceleration"]

    if abs(state["move_speed"]) > 0.005:  # Only allow rotation if the car is moving
        if keys[pg.K_LEFT]:
            rotate_angle = 2  # Rotate car to the left
        elif keys[pg.K_RIGHT]:
            rotate_angle = -2  # Rotate car to the right

    state["move_speed"] = min(max(state["move_speed"], -0.3), 0.5)

    # Update the car's current angle only if rotate_angle is non-zero
    if rotate_angle != 0:
        state["current_angle"] += rotate_angle
        state["current_angle"] %= 360  # Keep the angle within [0, 360)

    # Calculate the movement based on the car's current angle
    move_x = state["move_speed"] * sin(radians(state["current_angle"]))
    move_z = state["move_speed"] * cos(radians(state["current_angle"]))

    car_position = car.get_position()

    # Check for collisions in the direction of movement
    if state["move_speed"] > 0:
        if not state["collision"][1]:
            state["collision"][0] = check_collision(car_position, trees, move_x, move_z)
            if state["collision"][0]:
                move_x = move_z = 0
                state["current_angle"] -= rotate_angle
                rotate_angle = 0
    elif state["move_speed"] < 0:
        if not state["collision"][0]:
            state["collision"][1] = check_collision(car_position, trees, move_x, move_z)
            if state["collision"][1]:
                move_x = move_z = 0
                state["current_angle"] -= rotate_angle
                rotate_angle = 0

    car.move(-move_x, 0, -move_z)
    if rotate_angle != 0:
        car.rotate(rotate_angle, 0, 0)

    # Update the camera position and orientation based on the car's position and rotation
    car_position = car.get_position()
    car_center = car.calculate_center()
    cam_distance = 10  # Distance behind the car
    cam_height = 5  # Height of the camera
    cam_x = car_position[0] + cam_distance * sin(radians(state["current_angle"]))
    cam_y = car_position[1] - cam_height
    cam_z = car_position[2] + cam_distance * cos(radians(state["current_angle"]))
    # camera.set_position(-cam_x, cam_y, -cam_z)
    # camera.set_yaw(-state["current_angle"])
    # camera.look_at(car_center[0], cam_y, car_center[2])

def drawText(x, y, text):
    font = pg.font.Font(None, 25)
    textSurface = font.render(text, True, (0,0,0), (255,255,255))
    textData = pg.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def init():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Racing Game")

    glClearColor(0.53, 0.81, 0.98, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    # Setup light 0
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (10, 10, 10, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    # Setup light 1 for additional lighting
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, (-10, 10, -10, 1.0))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.6, 0.6, 0.6, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.8, 0.8, 0.8, 1.0))

    glShadeModel(GL_SMOOTH)

def main():
    init()
    clock = pg.time.Clock()
    camera = Camera()
    camera.init()
    trees = Environment().draw_trees()
    car = OBJ('car_object/Sedan.obj', swapyz=False)
    car2 = OBJ('car_object/Sedan.obj', swapyz=False)
    timer = 0

    car.rotate(180, 0, 0)
    car2.rotate(180, 0, 0)
    car2.move(5, 0, 0)
    # car.move(60, 0,10)
    # camera.move(-60, 0, -10)
    car2.generate()
    car.generate()

    # State dictionary to maintain state across function calls
    state = {
        "move_speed": 0.0,
        "acceleration": 0.01,
        "deceleration": 0.005,
        "current_angle": 0.0,
        "collision": [False, False]
    }
    state2 = {
        "move_speed": 0.0,
        "acceleration": 0.01,
        "deceleration": 0.005,
        "current_angle": 0.0,
        "collision": [False, False]
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                car.free()
                car2.free()
                for tree in trees:
                    tree.free()
                pg.quit()
                sys.exit()
        timer += clock.get_time()
        movement(car, camera, trees, state)
        movement2(car2, camera, trees, state2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.apply()
        Environment().init_env(trees)

        glColor3f(1, 1, 1)
        car.render()
        car2.render()
        print(car.get_position())
        if int(car.get_position()[2]) == -6:
            timer = 0
        drawText(0, 0, "Time: " + str(timer // 10000) + ":" + str((timer // 1000) % 10) + str((timer // 100) % 10) + "." + str((timer // 10) % 10) + str(timer % 10) + "s")
        pg.display.flip()
        clock.tick(60)
        # pg.time.wait(10)


if __name__ == "__main__":
    main()
