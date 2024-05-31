from math import sin, cos, radians

from OpenGL.GL import *


class Road:
    """
    A class to represent a road in a racing game.

    ...

    Attributes
    ----------
    length : float
        the length of the road
    width : float
        the width of the road
    position : list
        the position of the road in the 3D space
    color : list
        the color of the road

    Methods
    -------
    draw():
        Draws the road.
    draw_curve(radius, angle, quadrant):
        Draws a curved road.
    """

    def __init__(self, length, width, position, color):
        """
        Constructs all the necessary attributes for the road object.

        Parameters:
        length (float): The length of the road.
        width (float): The width of the road.
        position (list): The position of the road in the 3D space.
        color (list): The color of the road.
        """

        self.length = length
        self.width = width
        self.position = position
        self.color = color

    def draw(self):
        """
        Draws the road.

        This method uses OpenGL to draw a quad that represents the road.
        """

        glBegin(GL_QUADS)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glVertex3f(self.position[0], self.position[1], self.position[2])
        glVertex3f(self.position[0] + self.width, self.position[1], self.position[2])
        glVertex3f(self.position[0] + self.width, self.position[1], self.position[2] + self.length)
        glVertex3f(self.position[0], self.position[1], self.position[2] + self.length)
        glEnd()

    def draw_curve(self, radius, angle, quadrant):
        """
        Draws a curved road.

        This method uses OpenGL to draw a curved road. The curve is defined by a radius and an angle, and it is drawn in a specific quadrant.

        Parameters:
        radius (float): The radius of the curve.
        angle (float): The angle of the curve.
        quadrant (int): The quadrant of the curve.
        """

        angle_start = angle_end = 0
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_QUAD_STRIP)
        if quadrant == 4:
            angle_start = 0
            angle_end = angle
        elif quadrant == 3:
            angle_start = 90
            angle_end = 90 + angle
        elif quadrant == 2:
            angle_start = 180
            angle_end = 180 + angle
        elif quadrant == 1:
            angle_start = 270
            angle_end = 270 + angle

        for i in range(angle_start, angle_end + 1, 10):
            theta = radians(i)
            x_inner = radius * cos(theta) + self.position[0]
            z_inner = radius * sin(theta) + self.position[2]
            x_outer = (radius + self.length) * cos(theta) + self.position[0]
            z_outer = (radius + self.length) * sin(theta) + self.position[2]
            glVertex3f(x_inner, self.position[1], z_inner)
            glVertex3f(x_outer, self.position[1], z_outer)
        glEnd()
