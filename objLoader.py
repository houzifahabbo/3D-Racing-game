import os

import pygame
from OpenGL.GL import *


class OBJ:
    """
    A class to represent a 3D object loaded from a Wavefront OBJ file.

    ...

    Attributes
    ----------
    generate_on_init : bool
        a class variable that determines whether to generate the OpenGL display list upon initialization
    vertices : list
        a list of the object's vertices
    normals : list
        a list of the object's normals
    texcoords : list
        a list of the object's texture coordinates
    faces : list
        a list of the object's faces
    gl_list : int
        the ID of the object's OpenGL display list
    position : list
        the object's position in the 3D space
    rotation : list
        the object's rotation angles
    mtl : dict
        a dictionary containing the object's materials

    Methods
    -------
    loadTexture(imagefile):
        Loads a texture from an image file.
    loadMaterial(filename):
        Loads materials from a MTL file.
    __init__(filename, swapyz=False):
        Initializes the object by loading data from an OBJ file.
    generate():
        Generates the object's OpenGL display list.
    render():
        Renders the object in the 3D space.
    move(x, y, z):
        Moves the object by a certain amount.
    rotate(yaw, pitch, roll):
        Rotates the object by certain angles.
    free():
        Deletes the object's OpenGL display list.
    calculate_center():
        Calculates the object's center point.
    get_bounding_box():
        Gets the object's bounding box.
    get_position():
        Gets the object's position.
    scale(scale):
        Scales the object by a certain factor.
    set_position(x, y, z):
        Sets the object's position.
    """

    generate_on_init = True

    @classmethod
    def loadTexture(cls, imagefile):
        """
        Loads a texture from an image file.

        Parameters:
        imagefile (str): The path to the image file.

        Returns:
        int: The ID of the generated OpenGL texture.
        """

        surf = pygame.image.load(imagefile)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return texid

    @classmethod
    def loadMaterial(cls, filename):
        """
        Loads materials from a MTL file.

        Parameters:
        filename (str): The path to the MTL file.

        Returns:
        dict: A dictionary containing the loaded materials.
        """

        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = cls.loadTexture(imagefile)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def __init__(self, filename, swapyz=False):
        """
        Initializes the object by loading data from an OBJ file.

        Parameters:
        filename (str): The path to the OBJ file.
        swapyz (bool): Whether to swap the y and z coordinates. Defaults to False.
        """

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        dirname = os.path.dirname(filename)
        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = self.loadMaterial(os.path.join(dirname, values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        if self.generate_on_init:
            self.generate()

    def generate(self):
        """
        Generates the object's OpenGL display list.
        """

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)

        for face in self.faces:
            vertices, normals, texture_coords, material = face
            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])
            glBegin(GL_POLYGON)

            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def render(self):
        """
        Renders the object in the 3D space.
        """

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glCallList(self.gl_list)
        glPopMatrix()

    def move(self, x, y, z):
        """
        Moves the object by a certain amount.

        Parameters:
        x (float): The amount to move along the x-axis.
        y (float): The amount to move along the y-axis.
        z (float): The amount to move along the z-axis.
        """

        self.position[0] += x
        self.position[1] += y
        self.position[2] += z

    def rotate(self, yaw, pitch, roll):
        """
        Rotates the object by certain angles.

        Parameters:
        yaw (float): The angle to rotate around the y-axis.
        pitch (float): The angle to rotate around the x-axis.
        roll (float): The angle to rotate around the z-axis.
        """

        self.rotation[0] += pitch
        self.rotation[1] += yaw
        self.rotation[2] += roll

    def free(self):
        """
        Deletes the object's OpenGL display list.
        """

        glDeleteLists(self.gl_list, 1)
        self.gl_list = 0

    def calculate_center(self):
        """
        Calculates the object's center point.

        Returns:
        tuple: A tuple containing the x, y, and z coordinates of the center point.
        """

        avg_x = sum(v[0] for v in self.vertices) / len(self.vertices)
        avg_y = sum(v[1] for v in self.vertices) / len(self.vertices)
        avg_z = sum(v[2] for v in self.vertices) / len(self.vertices)
        return avg_x, avg_y, avg_z

    def get_position(self):
        """
        Gets the object's position.

        This method returns the current position of the object in the 3D space.

        Returns:
        list: A list containing the x, y, and z coordinates of the object's position.
        """

        return self.position

    def scale(self, scale):
        """
        Scales the object by a certain factor.

        This method multiplies all the vertices of the object by a given scale factor. This effectively scales the size of the object in the 3D space.

        Parameters:
        scale (float): The scale factor.
        """

        self.vertices = [list(vertex) for vertex in self.vertices]
        for vertex in self.vertices:
            vertex[0] *= scale
            vertex[1] *= scale
            vertex[2] *= scale
