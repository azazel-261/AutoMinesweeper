import numpy as np

class Constants:
    closed_cell_colors = np.array([[162, 209, 73], [170, 215, 81]])
    opened_cell_colors = np.array([[229, 194, 159], [215, 184, 153]])

    window_top_color = np.array([74, 117, 44])

    number_colors = {
        1: (25, 118, 210),
        2: (56, 142, 60),
        3: (211, 47, 47),
        4: (123, 31, 162),
        5: (255, 143, 0),
        6: (0, 151, 167),
        7: (66, 66, 66),
        8: (164, 151, 137),
    }

class Globals:
    cell_pixel_size = 0
    cell_scan_range = 0
    cell_scan_offset = 0