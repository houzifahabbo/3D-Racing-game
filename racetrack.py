from road import Road


class Racetrack:
    """
    A class to represent a racetrack in a racing game.

    ...

    Attributes
    ----------
    x : float
        the x-coordinate of the racetrack's position
    y : float
        the y-coordinate of the racetrack's position
    z : float
        the z-coordinate of the racetrack's position
    yaw : float
        the yaw angle of the racetrack (rotation around the y-axis)
    pitch : float
        the pitch angle of the racetrack (rotation around the x-axis)
    roll : float
        the roll angle of the racetrack (rotation around the z-axis)

    Methods
    -------
    draw_straight_borders(start_x, start_z, length, width, rotated):
        Draws straight borders of the racetrack.
    draw_curve_borders(radius, angle, start_x, start_z, length, quadrant):
        Draws curved borders of the racetrack.
    draw_start_finish_line(start_x, start_z, length, width, rotated):
        Draws the start and finish line of the racetrack.
    get_track_coordinates():
        Returns a list of tuples, where each tuple contains the x and z coordinates, and the width and height of a segment of the track.
    is_inside_track(x, y, boxes):
        Checks if a given point is inside the track.
    draw():
        Calls the other methods to draw the entire track.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the racetrack object.
        """

        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def draw_straight_borders(self, start_x, start_z, length, width, rotated):
        """
        Draws straight borders of the racetrack.

        Parameters:
        start_x (float): The starting x-coordinate of the border.
        start_z (float): The starting z-coordinate of the border.
        length (float): The length of the border.
        width (float): The width of the border.
        rotated (bool): A flag indicating whether the border is rotated.
        """
        step = 5.0
        if not rotated:
            i = 0.0
            while i < length:
                segment_length = min(step, length - i)
                if int(i) % 10 == 0:
                    Road(segment_length, 0.5, [start_x, 0, start_z + i], (1, 0, 0)).draw()
                    Road(segment_length, 0.5, [start_x + width, 0, start_z + i], (1, 0, 0)).draw()
                Road(segment_length, 0.5, [start_x, 0, start_z + i], (1, 1, 1)).draw()
                Road(segment_length, 0.5, [start_x + width, 0, start_z + i], (1, 1, 1)).draw()
                i += step
            Road(length, width, [start_x, -0.007, start_z], (0.5, 0.5, 0.5)).draw()
        else:
            i = 0.0
            while i < width:
                segment_length = min(step, width - i)
                if int(i) % 10 == 0:
                    Road(0.5, segment_length, [start_x + i, -0.004, start_z], (1, 0, 0)).draw()
                    Road(0.5, segment_length, [start_x + i, -0.004, start_z + length], (1, 0, 0)).draw()
                Road(0.5, segment_length, [start_x + i, -0.004, start_z], (1, 1, 1)).draw()
                Road(0.5, segment_length, [start_x + i, -0.004, start_z + length], (1, 1, 1)).draw()
                i += step
            Road(length, width, [start_x, -0.006, start_z], (0.5, 0.5, 0.5)).draw()

    def draw_curve_borders(self, radius, angle, start_x, start_z, length, quadrant):
        """
        Draws curved borders of the racetrack.

        Parameters:
        radius (float): The radius of the curve.
        angle (float): The angle of the curve.
        start_x (float): The starting x-coordinate of the border.
        start_z (float): The starting z-coordinate of the border.
        length (float): The length of the border.
        quadrant (int): The quadrant of the curve.
        """
        for i in range(0, angle, 10):
            Road(0.5, 0.5, [start_x, -0.007, start_z], (1, 1, 1)).draw_curve(radius + length, angle, quadrant)
            Road(0.5, 0.5, [start_x, -0.007, start_z], (1, 0, 0)).draw_curve(radius, angle, quadrant)
        Road(length, 0.5, [start_x, -0.008, start_z], (0.5, 0.5, 0.5)).draw_curve(radius, angle, quadrant)

    def draw_start_finish_line(self, start_x, start_z, length, width, rotated):
        """
        Draws the start and finish line of the racetrack.

        Parameters:
        start_x (float): The starting x-coordinate of the line.
        start_z (float): The starting z-coordinate of the line.
        length (float): The length of the line.
        width (float): The width of the line.
        rotated (bool): A flag indicating whether the line is rotated.
        """
        i = 0
        if not rotated:
            while i <= width:
                Road(1, 0.5, [start_x + i, -0.005, start_z], (1, 1, 1)).draw()
                Road(1, 0.5, [start_x + i, -0.005, start_z + length], (0, 0, 0)).draw()
                Road(1, 0.5, [start_x + i + 0.5, -0.005, start_z + length], (1, 1, 1)).draw()
                Road(1, 0.5, [start_x + i + 0.5, -0.005, start_z], (0, 0, 0)).draw()
                i += 1
        else:
            while i <= length:
                Road(1, 0.5, [start_x, -0.005, start_z + i], (1, 1, 1)).draw()
                Road(1, 0.5, [start_x + width, -0.005, start_z + i], (0, 0, 0)).draw()
                Road(1, 0.5, [start_x + width, -0.005, start_z + i + 0.5], (1, 1, 1)).draw()
                Road(1, 0.5, [start_x, -0.005, start_z + i + 0.5], (0, 0, 0)).draw()
                i += 1

    def get_track_coordinates(self):
        """
        Returns a list of tuples, where each tuple contains the x and z coordinates, and the width and height of a segment of the track.

        Returns:
        list: A list of tuples, where each tuple contains the x and z coordinates, and the width and height of a segment of the track.
        """
        # Coordinates extracted from the draw method
        coordinates = [
            (-5, -6, 1, 9),  # Start/finish line
            (-5, -30, 30, 10),  # Straight border
            (6.5, -30, 10, 2),  # Curve border
            (19, -30, 10, 4),  # Curve border
            (20, -60, 30, 10),  # Straight border
            (31.5, -60, 10, 2),  # Curve border
            (44, -60, 10, 3),  # Curve border
            (44, -59, 10, 20),  # Straight border
            (64, -47.5, 10, 1),  # Curve border
            (65, -47.5, 50, 10),  # Straight border
            (64, 2.5, 10, 4),  # Curve border
            (61.5, 3.5, 10, 2.5),  # Straight border
            (6.5, 3.5, 10, 55),  # Straight border
            (6.5, 2.5, 10, 3),  # Curve border
            (-5, 0, 2.5, 10)  # Straight border
        ]

        return coordinates

    def draw(self):
        """
        Calls the other methods to draw the entire track.
        """
        self.draw_start_finish_line(-5, -6, 1, 9, False)
        self.draw_straight_borders(-5, -30, 30, 10, False)
        self.draw_curve_borders(1, 180, 6.5, -30, 10, 2)
        self.draw_curve_borders(1, 180, 19, -30, 10, 4)
        self.draw_straight_borders(20, -60, 30, 10, False)
        self.draw_curve_borders(1, 180, 31.5, -60, 10, 2)
        self.draw_curve_borders(1, 90, 44, -60, 10, 3)
        self.draw_straight_borders(44, -59, 10, 20, True)
        self.draw_curve_borders(1, 90, 64, -47.5, 10, 1)
        self.draw_straight_borders(65, -47.5, 50, 10, False)
        self.draw_curve_borders(1, 90, 64, 2.5, 10, 4)
        self.draw_straight_borders(61.5, 3.5, 10, 2.5, True)
        self.draw_straight_borders(6.5, 3.5, 10, 55, True)
        self.draw_curve_borders(1, 90, 6.5, 2.5, 10, 3)
        self.draw_straight_borders(-5, 0, 2.5, 10, False)
