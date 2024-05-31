from random import uniform

from OpenGL.GL import *

from objLoader import OBJ
from racetrack import Racetrack


class Environment:
    """
    A class to represent the game environment.

    ...

    Methods
    -------
    get_random_coordinates_outside_track():
        Generates random coordinates outside the track.
    draw_floor():
        Draws the floor of the game environment.
    draw_trees():
        Draws trees at random locations in the game environment.
    init_env(trees):
        Initializes the game environment.
    """

    def get_random_coordinates_outside_track(self):
        """
        Generates random coordinates outside the track.

        This method first defines a bounding area for the entire track, then generates random points within this area.
        It checks if each point is inside the track, and if it is, it generates a new point. This process is repeated
        until it has generated 100 points that are outside the track.

        Returns:
        list: A list of tuples, where each tuple contains the x and z coordinates of a point.
        """

        # Define the bounding area for the entire track (assuming a large enough area)
        track_bounds = (-100, -100, 200, 200)  # (xmin, ymin, xmax, ymax)

        track_coordinates = Racetrack().get_track_coordinates()

        random_coords = []

        for x, z, w, h in track_coordinates:
            # Define a bounding box around the track segment
            min_x = x - w / 2 - 5  # Extra padding outside the track
            max_x = x + w / 2 + 5
            min_z = z - h / 2 - 5
            max_z = z + h / 2 + 5

            # Add bounding box to the list
            random_coords.append((min_x, min_z, max_x, max_z))

        # Function to check if a point is inside any bounding box
        def is_inside_track(x, z, boxes):
            for (min_x, min_z, max_x, max_z) in boxes:
                if min_x <= x <= max_x and min_z <= z <= max_z:
                    return True
            return False

        # Generate random coordinates outside the track
        outside_coords = []
        for _ in range(100):  # Generate 100 random points
            while True:
                x = uniform(track_bounds[0], track_bounds[2])
                z = uniform(track_bounds[1], track_bounds[3])
                if not is_inside_track(x, z, random_coords):
                    outside_coords.append((x, z))
                    break

        return outside_coords

    def draw_floor(self):
        """
        Draws the floor of the game environment.

        This method uses OpenGL to draw a large green quad that represents the floor.
        """

        glBegin(GL_QUADS)
        glColor3f(0, 0.5, 0)
        glVertex3f(-200, -0.009, -200)
        glVertex3f(200, -0.009, -200)
        glVertex3f(200, -0.009, 200)
        glVertex3f(-200, -0.009, 200)
        glEnd()

    def draw_trees(self):
        """
        Draws trees at random locations in the game environment.

        This method first generates random coordinates outside the track using the get_random_coordinates_outside_track
        method. It then creates a tree object at each of these locations, scales it by a random factor, and adds it to
        a list. It stops after it has created 20 trees.

        Returns:
        list: A list of tree objects.
        """

        trees = []
        random_cords = self.get_random_coordinates_outside_track()
        for x, z in random_cords:
            tree = OBJ('objects/tree.obj', swapyz=False)
            tree.move(x, 0, z)
            tree.scale(uniform(0.1, 1))
            trees.append(tree)
            if len(trees) == 20:
                break
        return trees

    def init_env(self, trees):
        """
        Initializes the game environment.

        This method first renders all the trees in the environment, then draws the racetrack and the floor.

        Parameters:
        trees (list): A list of tree objects.
        """

        for tree in trees:
            tree.render()
        Racetrack().draw()
        self.draw_floor()
