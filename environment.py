from racetrack import Racetrack
from OpenGL.GL import *
from objLoader import OBJ
from random import uniform
class Environment:
    def get_random_coordinates_outside_track(self):
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
                z =uniform(track_bounds[1], track_bounds[3])
                if not is_inside_track(x, z, random_coords):
                    outside_coords.append((x, z))
                    break

        return outside_coords
    def draw_floor(self):
        glBegin(GL_QUADS)
        glColor3f(0, 0.5,0)
        glVertex3f(-100, -0.009, -100)
        glVertex3f(100, -0.009, -100)
        glVertex3f(100, -0.009, 100)
        glVertex3f(-100, -0.009, 100)
        glEnd()

    def draw_trees(self):
        trees = []
        random_cords = self.get_random_coordinates_outside_track()
        for x, z in random_cords:
            tree = OBJ('tree_object/Lowpoly_tree_sample.obj', swapyz=False)
            tree.move(x, 0, z)
            tree.scale(uniform(0.1, 1))
            tree.generate()
            trees.append(tree)
            if len(trees) ==20:
                break
        return trees

    def init_env(self , trees):
        for tree in trees:
            tree.render()
        Racetrack().draw()
        self.draw_floor()
