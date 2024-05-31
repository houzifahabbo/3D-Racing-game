from OpenGL.GL import *
from OpenGL.GLU import *


class Camera:
    """
    A class to represent a camera in a 3D environment.

    ...

    Attributes
    ----------
    x : float
        the x-coordinate of the camera's position
    y : float
        the y-coordinate of the camera's position
    z : float
        the z-coordinate of the camera's position
    yaw : float
        the yaw angle of the camera (rotation around the y-axis)
    pitch : float
        the pitch angle of the camera (rotation around the x-axis)
    roll : float
        the roll angle of the camera (rotation around the z-axis)

    Methods
    -------
    init(aspect_ratio):
        Initializes the camera's projection and modelview matrices.
    set_yaw(yaw):
        Sets the camera's yaw angle.
    look_at(target_x, target_y, target_z):
        Makes the camera look at a specific point in the 3D space.
    set_position(x, y, z):
        Sets the camera's position.
    apply():
        Applies the camera's transformations to the OpenGL context.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the camera object.
        """

        self.x = 0
        self.y = -5
        self.z = -10
        self.yaw = 0
        self.pitch = 20
        self.roll = 0

    def init(self, aspect_ratio):
        """
        Initializes the camera's projection and modelview matrices.

        Parameters:
        aspect_ratio (float): The aspect ratio of the viewport.
        """

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, aspect_ratio, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_yaw(self, yaw):
        """
        Sets the camera's yaw angle.

        Parameters:
        yaw (float): The new yaw angle.
        """

        self.yaw = yaw

    def look_at(self, target_x, target_y, target_z):
        """
        Makes the camera look at a specific point in the 3D space.

        Parameters:
        target_x (float): The x-coordinate of the target point.
        target_y (float): The y-coordinate of the target point.
        target_z (float): The z-coordinate of the target point.
        """

        gluLookAt(self.x, self.y, self.z, target_x, target_y, target_z, 0, 1, 0)

    def set_position(self, x, y, z):
        """
        Sets the camera's position.

        Parameters:
        x (float): The new x-coordinate of the camera's position.
        y (float): The new y-coordinate of the camera's position.
        z (float): The new z-coordinate of the camera's position.
        """

        self.x = x
        self.y = y
        self.z = z

    def apply(self):
        """
        Applies the camera's transformations to the OpenGL context.
        """

        glLoadIdentity()
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)
        glTranslatef(self.x, self.y, self.z)
