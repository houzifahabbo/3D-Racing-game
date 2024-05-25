from OpenGL.GL import *
from borders import Roads
from math import sin, cos, radians

# borders_data = \
#     [[-5, 0, -5, 0.5, 5,'red'],
#      [-5, 0, 0, 0.5, 5, 'white'] ,
#      [-5, 0, 5, 0.5, 5, 'red' ] ,
#      [5, 0, 5, 0.5, 5, 'red'],
#      [5, 0, 0, 0.5, 5, 'white'],
#      [5, 0, -5, 0.5, 5, 'red'], ]


class Racetrack:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def draw_straight_borders(self,start_x,start_z,length,width, rotated):
        if not rotated:
            for i in range(0, length, 5):
                if i % 10 == 0:
                    Roads(5, 0.5, [start_x, 0, start_z + i], 'red').draw()
                    Roads(5, 0.5, [start_x + width , 0, start_z + i], 'red').draw()
                Roads(5, 0.5, [start_x, 0, start_z + i], 'white').draw()
                Roads(5, 0.5, [start_x + width, 0, start_z + i], 'white').draw()
            glColor3f(0.5, 0.5, 0.5)
            glBegin(GL_QUAD_STRIP)
            for i in range(0, length + 1, 5):
                glVertex3f(start_x, -0.001, start_z + i)
                glVertex3f(start_x + width, -0.002, start_z + i)
            glEnd()

        else:
            for i in range(0, width, 5):
                if i % 10 == 0:
                    Roads(0.5, 5, [start_x + i, 0, start_z], 'red').draw()
                    Roads(0.5, 5, [start_x + i, 0, start_z + length], 'red').draw()
                Roads(0.5, 5, [start_x + i, 0, start_z], 'white').draw()
                Roads(0.5, 5, [start_x + i, 0, start_z + length], 'white').draw()
            glColor3f(0.5, 0.5, 0.5)
            glBegin(GL_QUAD_STRIP)
            for i in range(0, width + 1, 5):
                glVertex3f(start_x + i, -0.001, start_z)
                glVertex3f(start_x + i, -0.002, start_z + length)
            glEnd()

    # def draw_curve_borders(self, radius, angle, start_x, start_z, length, width, flipped):
    #     for i in range(0, angle, 10):
    #         if flipped:
    #             Border(0.5, 0.5, [start_x, -0.003, start_z], 'white').draw_curve(radius - length, angle)
    #             Border(0.5, 0.5, [start_x, -0.003, start_z], 'red').draw_curve(-radius, angle)
    #         else:
    #             Border(0.5, 0.5, [start_x, -0.003, start_z], 'white').draw_curve(radius - width, angle)
    #             Border(0.5, 0.5, [start_x, -0.003, start_z], 'red').draw_curve(-radius, angle)
    #
    #     glColor3f(0.5, 0.5, 0.5)
    #     glBegin(GL_QUAD_STRIP)
    #     for i in range(0, angle + 1, 10):
    #         for i in range(0, angle + 1, 10):
    #             theta = radians(i)
    #             x_inner = radius * cos(theta) + start_x
    #             z_inner = radius * sin(theta) + start_z
    #             x_outer = (radius + length) * cos(theta) + start_x
    #             z_outer = (radius + length) * sin(theta) + start_z
    #             if flipped:
    #                 x_outer = (radius + width) * cos(theta) + start_x
    #                 z_outer = (radius + width) * sin(theta) + start_z
    #             glVertex3f(x_inner, -0.004, z_inner)
    #             glVertex3f(x_outer, -0.005, z_outer)
    #     glEnd()

    def draw_curve_borders(self, radius, angle, start_x, start_z, length, quadrant):
        for i in range(0, angle, 10):
            Roads(0.5, 0.5, [start_x, -0.003, start_z], 'white').draw_curve(radius + length, angle, quadrant)
            Roads(0.5, 0.5, [start_x, -0.003, start_z], 'red').draw_curve(radius, angle, quadrant)

        glColor3f(0.5, 0.5, 0.5)
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
            x_inner = radius * cos(theta) + start_x
            z_inner = radius * sin(theta) + start_z
            x_outer = (radius + length) * cos(theta) + start_x
            z_outer = (radius + length) * sin(theta) + start_z
            glVertex3f(x_inner, -0.004, z_inner)
            glVertex3f(x_outer, -0.005, z_outer)
        glEnd()



    def draw(self):
        self.draw_straight_borders(-5, -30, 35, 10,False)
        self.draw_curve_borders(1, 180, 6.5,-30, 10, 2)
        self.draw_curve_borders(1, 180, 19, -30, 10,4)
        self.draw_straight_borders(20, -60, 30, 10,False)
        self.draw_curve_borders(1, 180, 31.5, -60, 10,  2)
        self.draw_curve_borders(1, 90, 44, -60, 10, 3)
        self.draw_straight_borders(44, -59, 10, 20,True)
        self.draw_curve_borders(1, 90, 64, -47.5, 10, 1)
        self.draw_straight_borders(65, -47.5, 50, 10,False)
        self.draw_curve_borders(1, 90, 64, 2.5, 10, 4)
        self.draw_straight_borders(6.5, 3.5, 10, 60,True)
        self.draw_curve_borders(1, 90, 6.5, 2.5, 10, 3)

