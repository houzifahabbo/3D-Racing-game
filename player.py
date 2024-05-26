import pygame as pg
from math import sin, cos, radians
import pygame.freetype
from camera import Camera


class Player():
    def __init__(self, bindings,car):
        self.bindings = bindings
        self.state = {
            "move_speed": 0,
            "acceleration": 0.01,
            "deceleration": 0.005,
            "current_angle": 0,
            "collision": [False, False]
        }
        self.car = car
        self.camera = Camera()
        self.camera.init()


    def check_collision(self, car_position, trees, move_x, move_z):
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

    def movement(self, trees):
        keys = pg.key.get_pressed()
        rotate_angle = 0
        if keys[self.bindings["forward"]]:
            self.state["move_speed"] += self.state["acceleration"]
        elif keys[self.bindings["backward"]]:
            self.state["move_speed"] -= self.state["acceleration"]
        else:
            if self.state["move_speed"] > 0:
                self.state["move_speed"] -= self.state["deceleration"]
            elif self.state["move_speed"] < 0:
                self.state["move_speed"] += self.state["deceleration"]

        if abs(self.state["move_speed"]) > 0.005:
            if keys[self.bindings["left"]]:
                rotate_angle = 2
            elif keys[self.bindings["right"]]:
                rotate_angle = -2

        self.state["move_speed"] = min(max(self.state["move_speed"], -0.3), 0.5)

        if rotate_angle != 0:
            self.state["current_angle"] += rotate_angle
            self.state["current_angle"] %= 360

        move_x = self.state["move_speed"] * sin(radians(self.state["current_angle"]))
        move_z = self.state["move_speed"] * cos(radians(self.state["current_angle"]))

        car_position = self.car.get_position()

        if self.state["move_speed"] > 0:
            if not self.state["collision"][1]:
                self.state["collision"][0] = self.check_collision(car_position, trees, move_x, move_z)
                if self.state["collision"][0]:
                    move_x = move_z = 0
                    self.state["current_angle"] -= rotate_angle
                    rotate_angle = 0
        elif self.state["move_speed"] < 0:
            if not self.state["collision"][0]:
                self.state["collision"][1] = self.check_collision(car_position, trees, move_x, move_z)
                if self.state["collision"][1]:
                    move_x = move_z = 0
                    self.state["current_angle"] -= rotate_angle
                    rotate_angle = 0

        self.car.move(-move_x, 0, -move_z)
        if rotate_angle != 0:
            self.car.rotate(rotate_angle, 0, 0)

        car_position = self.car.get_position()
        car_center = self.car.calculate_center()
        cam_distance = 10
        cam_height = 5
        cam_x = car_position[0] + cam_distance * sin(radians(self.state["current_angle"]))
        cam_y = car_position[1] - cam_height
        cam_z = car_position[2] + cam_distance * cos(radians(self.state["current_angle"]))
        self.camera.set_position(-cam_x, cam_y, -cam_z)
        self.camera.set_yaw(-self.state["current_angle"])
        self.camera.look_at(car_center[0], cam_y, car_center[2])
