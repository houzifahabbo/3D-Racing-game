from road import Road


class Racetrack:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def draw_straight_borders(self, start_x, start_z, length, width, rotated):
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
        for i in range(0, angle, 10):
            Road(0.5, 0.5, [start_x, -0.007, start_z], (1, 1, 1)).draw_curve(radius + length, angle, quadrant)
            Road(0.5, 0.5, [start_x, -0.007, start_z], (1, 0, 0)).draw_curve(radius, angle, quadrant)
        Road(length, 0.5, [start_x, -0.008, start_z], (0.5, 0.5, 0.5)).draw_curve(radius, angle, quadrant)

    def draw_start_finish_line(self, start_x, start_z, length, width, rotated):
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

        # # striped white and red lines for start/finish line
        # i = 0.0
        # while i < width:
        #     Roads(1, 0.5, [-4.5+i, 0.002, -5 ], (0,0,0)).draw()
        #     Roads(1, 0.5, [-4+i, 0.002, -5], (1,1,1)).draw()
        #     Roads(1, 0.5, [-4.5+i, 0.002, -6 ], (1,1,1)).draw()
        #     Roads(1, 0.5, [-4+i, 0.002, -6], (0,0,0)).draw()

    def get_track_coordinates(self):
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

    def is_inside_track(x, y, boxes):
        for (min_x, min_y, max_x, max_y) in boxes:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

    # Generate random coordinates outside the track
    def draw(self):
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
