import numpy as np
import pyautogui as gui

import time

from PIL.Image import Image
from mouseinfo import screenshot

import local_types
import config_parser
from globals import Constants, Globals

def visualize_field(field: local_types.Field):
    visualisation = []
    for row in field.cells:
        vis_row = []
        for cell in row:
            if cell.marked:
                vis_row.append("v")
                continue
            if not cell.opened:
                vis_row.append("█")
                continue
            if not cell.number:
                vis_row.append("░")
                continue
            else:
                vis_row.append(str(cell.number))
        visualisation.append(vis_row)
    for row in visualisation:
        print(" ".join(row))


class Scanner:
    def wait_for_game(self, sleep_time: float = 0.3):
        coords = config_parser.get_window_coords()
        while True:
            screenshot = gui.screenshot()
            color = screenshot.getpixel(coords.to_tuple())
            if np.all(np.array(color) == np.array(Constants.window_top_color)):
                print("game found")
                return
            time.sleep(sleep_time)

    def scan_cell(self, coords: local_types.Vector2, shot: Image = None) -> local_types.Cell:
        _cell = local_types.Cell()
        _cell.screen_coords = coords
        scan_start_coords = local_types.Vector2(coords.x + Globals.cell_scan_offset, coords.y + Globals.cell_scan_offset)
        screenshot = shot or gui.screenshot()
        samples = set()
        for x in range(int(Globals.cell_scan_range)):
            for y in range(int(Globals.cell_scan_range)):
                color = screenshot.getpixel(local_types.Vector2(scan_start_coords.x + x, scan_start_coords.y + y).to_tuple())
                if np.any(np.all(Constants.closed_cell_colors == np.array(color), axis = 1)):
                    return _cell
                if color not in samples: samples.add(color)
        _cell.opened = True
        for k in Constants.number_colors:
            number_color = Constants.number_colors[k]
            if number_color in samples:
                _cell.number = k
                return _cell
        return _cell

    def count_field(self) -> local_types.Field:
        start_time = time.time()
        start_coords = config_parser.get_game_coords()
        screenshot = gui.screenshot()
        color = np.array(screenshot.getpixel(start_coords.to_tuple()))
        prev_color = color
        if np.any(np.all(Constants.closed_cell_colors == color, axis = 1)):
            print("closed cell found")
        field = local_types.Field()
        field.init_empty(config_parser.get_field_size().x, config_parser.get_field_size().y)
        for y in range(config_parser.get_field_size().y):
            field.get_cell(local_types.Vector2(0, y)).screen_coords.x = start_coords.x
        # Rows
        x = start_coords.x
        cx = 1
        while cx < config_parser.get_field_size().x:
            x += 1
            row_coords = local_types.Vector2(x, start_coords.y)
            row_color = np.array(screenshot.getpixel(row_coords.to_tuple()))
            if np.all(row_color == prev_color):
                continue
            if np.any(np.all(Constants.closed_cell_colors == row_color, axis = 1)):
                for y in range(config_parser.get_field_size().y):
                    field.get_cell(local_types.Vector2(cx, y)).screen_coords.x = row_coords.x
                prev_color = row_color
                cx += 1
        print("Horizontal counting done")
        for x in range(config_parser.get_field_size().x):
            print(field.get_cell(local_types.Vector2(x, 0)).screen_coords.x)
        for x in range(config_parser.get_field_size().x):
            field.get_cell(local_types.Vector2(x, 0)).screen_coords.y = start_coords.y
        prev_color = color
        y = start_coords.y
        cy = 1
        while cy < config_parser.get_field_size().y:
            y += 1
            column_coords = local_types.Vector2(start_coords.x, y)
            column_color = np.array(screenshot.getpixel(column_coords.to_tuple()))
            if np.all(column_color == prev_color):
                continue
            if np.any(np.all(Constants.closed_cell_colors == column_color, axis = 1)):
                for x in range(config_parser.get_field_size().x):
                    field.get_cell(local_types.Vector2(x, cy)).screen_coords.y = column_coords.y
                prev_color = column_color
                cy += 1
        print("Vertical counting done")
        for y in range(config_parser.get_field_size().y):
            print(field.get_cell(local_types.Vector2(0, y)).screen_coords.y)
        completion_time = time.time() - start_time
        print("Completion time: ", completion_time)
        Globals.cell_pixel_size = field.get_cell(local_types.Vector2(1, 0)).screen_coords.x - field.get_cell(local_types.Vector2(0, 0)).screen_coords.x
        Globals.cell_scan_range = Globals.cell_pixel_size // 3
        Globals.cell_scan_offset = (Globals.cell_pixel_size - Globals.cell_scan_range) // 2
        return field

    def update_field_full(self, field: local_types.Field):
        shot = gui.screenshot()
        for x in range(config_parser.get_field_size().x):
            for y in range(config_parser.get_field_size().y):
                field_cell = field.get_cell(local_types.Vector2(x, y))
                if field_cell.opened:
                    continue
                tmp_cell = self.scan_cell(field_cell.screen_coords, shot)
                field_cell.opened = tmp_cell.opened
                field_cell.number = tmp_cell.number

    def update_field_proximity(self, field: local_types.Field, center: local_types.Vector2):
        shot = gui.screenshot()
        for radius in range(0, config_parser.get_field_size().x):
            current_upd = 0
            if radius == 0:
                field_cell = field.get_cell(center)
                if field_cell.opened or field_cell.marked:
                    continue
                current_upd += 1
                cell = self.scan_cell(field_cell.screen_coords, shot)
                if not cell.opened:
                    continue
                field_cell.opened = cell.opened
                field_cell.number = cell.number
            else:
                # Top row
                y = center.y + radius
                for x in range(center.x - radius, center.x + radius + 1):
                    field_cell = field.get_cell(local_types.Vector2(x, y))
                    if field_cell is None:
                        continue
                    if field_cell.opened or field_cell.marked:
                        continue
                    cell = self.scan_cell(field_cell.screen_coords, shot)
                    if not cell.opened:
                        continue
                    field_cell.opened = cell.opened
                    field_cell.number = cell.number
                    current_upd += 1
                # Bottom row
                y = center.y - radius
                for x in range(center.x - radius, center.x + radius + 1):
                    field_cell = field.get_cell(local_types.Vector2(x, y))
                    if field_cell is None:
                        continue
                    if field_cell.opened or field_cell.marked:
                        continue
                    cell = self.scan_cell(field_cell.screen_coords, shot)
                    if not cell.opened:
                        continue
                    field_cell.opened = cell.opened
                    field_cell.number = cell.number
                    current_upd += 1
                # Left
                x = center.x - radius
                for y in range(center.y - radius + 1, center.y + radius):
                    field_cell = field.get_cell(local_types.Vector2(x, y))
                    if field_cell is None:
                        continue
                    if field_cell.opened or field_cell.marked:
                        continue
                    cell = self.scan_cell(field_cell.screen_coords, shot)
                    if not cell.opened:
                        continue
                    field_cell.opened = cell.opened
                    field_cell.number = cell.number
                    current_upd += 1
                x = center.x + radius
                for y in range(center.y - radius + 1, center.y + radius):
                    field_cell = field.get_cell(local_types.Vector2(x, y))
                    if field_cell is None:
                        continue
                    if field_cell.opened or field_cell.marked:
                        continue
                    cell = self.scan_cell(field_cell.screen_coords, shot)
                    if not cell.opened:
                        continue
                    field_cell.opened = cell.opened
                    field_cell.number = cell.number
                    current_upd += 1
            if not current_upd:
                print(radius)
                return
        print("Full proximity scan complete")





        # for proximity in range(3, config_parser.get_field_size().x * 2 + 1, 2):
        #     radius = (proximity - 1) // 2
        #     for x in range(center.x - radius, center.x + radius + 1):
        #         if x < 0 or x >= config_parser.get_field_size().x:
        #             continue
        #         for y in range(center.y - radius, center.y + radius + 1):
        #             if y < 0 or y >= config_parser.get_field_size().y:
        #                 continue
        #             field_cell = field.get_cell(local_types.Vector2(x, y))
        #             if field_cell.opened or field_cell in updated or field_cell.marked:
        #                 continue
        #             updated.add(field_cell)
        #             current_upd += 1
        #             tmp_cell = self.scan_cell(field_cell.screen_coords, shot)
        #             field_cell.opened = tmp_cell.opened
        #             field_cell.number = tmp_cell.number
        #     if current_upd == prev_upd:
        #         return
        #     prev_upd = current_upd
