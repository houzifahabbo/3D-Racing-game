from math import sin, cos, radians

import pygame as pg
import pygame.freetype

from camera import Camera


class Player:
    """
    A class to represent a player in the game.

    ...

    Attributes
    ----------
    bindings : dict
        a dictionary containing the key bindings for the player's controls
    state : dict
        a dictionary containing the player's current state
    car : OBJ
        the car object that the player is controlling
    camera : Camera
        the camera object that follows the player's car
    lap_count : int
        the number of laps that the player has completed
    has_lap_counted : bool
        a flag indicating whether the lap count has been updated
    timer : int
        a timer for tracking the time elapsed since the last lap
    rank : str
        the player's current rank in the race
    move_sound : Sound
        the sound effect for the car's movement
    idle_sound : Sound
        the sound effect for the car's idle state
    start_sound : Sound
        the sound effect for the car's start state
    collision_sound : Sound
        the sound effect for the car's collision state

    Methods
    -------
    update_lap_count(timer):
        Updates the player's lap count based on their position on the track.
    check_collision(car_position, trees, move_x, move_z):
        Checks if the player's car has collided with a tree.
    movement(trees):
        Updates the player's movement based on their current state and the key bindings.
    check_rank(player2):
        Checks and updates the player's rank based on their lap count and timer.
    """

    def __init__(self, bindings, car, aspect_ratio=400 / 600):
        """
        Constructs all the necessary attributes for the player object.

        Parameters:
        bindings (dict): The key bindings for the player's controls.
        car (OBJ): The car object that the player is controlling.
        aspect_ratio (float): The aspect ratio of the player's screen. Defaults to 400 / 600.
        """

        self.bindings = bindings
        self.state = {
            "move_speed": 0,
            "acceleration": 0.02,
            "deceleration": 0.008,
            "current_angle": 0,
            "collision": [False, False]
        }
        self.car = car
        self.camera = Camera()
        self.camera.init(aspect_ratio)
        self.lap_count = 0
        self.has_lap_counted = True
        self.timer = 0
        self.rank = ''
        self.move_sound = pygame.mixer.Sound('sound_effects/car_moving.wav')
        self.move_sound.set_volume(0.2)
        self.idle_sound = pygame.mixer.Sound('sound_effects/car_idle.wav')
        self.idle_sound.set_volume(0.03)
        self.start_sound = pygame.mixer.Sound('sound_effects/car_start.wav')
        self.start_sound.set_volume(0.05)
        self.collision_sound = pygame.mixer.Sound('sound_effects/collision.wav')
        self.collision_sound.set_volume(0.2)

    def update_lap_count(self, timer):
        """
        Updates the player's lap count based on their position on the track.

        Parameters:
        timer (int): The current game timer.
        """

        if timer - self.timer > 30000:
            self.timer = 0
            self.has_lap_counted = False

        if -5 < self.car.get_position()[0] < 5 and not self.has_lap_counted and -6.5 < self.car.get_position()[2] < -6:
            self.lap_count += 1
            self.has_lap_counted = True
            self.timer = timer

    def check_collision(self, car_position, trees, move_x, move_z):
        """
        Checks if the player's car has collided with a tree.

        Parameters:
        car_position (tuple): The current position of the car.
        trees (list): A list of tree objects.
        move_x (float): The x-coordinate of the car's movement vector.
        move_z (float): The z-coordinate of the car's movement vector.

        Returns:
        bool: True if the car has collided with a tree, False otherwise.
        """

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
        """
        Updates the player's movement based on their current state and the key bindings.

        Parameters:
        trees (list): A list of tree objects.
        """

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
        if 0.1 > self.state["move_speed"] and self.state["collision"] == [False, False]:
            self.move_sound.stop()
            self.idle_sound.play()
        elif self.state["collision"][0] == True or self.state["collision"][1] == True:
            self.move_sound.stop()
            self.collision_sound.play()
        else:
            self.idle_sound.stop()
            self.move_sound.play()

    def check_rank(self, player2):
        """
        Checks and updates the player's rank based on their lap count and timer.

        Parameters:
        player2 (Player): The other player in the game.
        """

        if self.lap_count > player2.lap_count:
            self.rank = '1st'
            player2.rank = '2nd'
        elif self.lap_count < player2.lap_count:
            self.rank = '2nd'
            player2.rank = '1st'
        else:
            if self.timer > player2.timer:
                self.rank = '1st'
                player2.rank = '2nd'
            elif self.timer < player2.timer:
                self.rank = '2nd'
                player2.rank = '1st'
            else:
                self.rank = 'Tie'
                player2.rank = 'Tie'
