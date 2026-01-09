from scanner import *
from local_types import *
import pyautogui as gui
import config_parser

from globals import Globals

sc = Scanner()
sc.wait_for_game()
field = sc.count_field()

clicked = set()

def set_flags():
    for y, row in enumerate(field.cells):
        for x, cell in enumerate(row):
            if cell.number <= 0:
                continue
            adjacent = [field.get_cell(_) for _ in field.get_adjacent(Vector2(x, y))]
            opened = field.count_open(adjacent)
            if cell.number == len(adjacent) - opened:
                for _cell in adjacent:
                    if not _cell.opened and not _cell.marked:
                        gui.rightClick(_cell.screen_coords.x + Globals.cell_scan_offset, _cell.screen_coords.y + Globals.cell_scan_offset)
                        _cell.mark()

def is_candidate(pos: Vector2):
    adjacent = [field.get_cell(_) for _ in field.get_adjacent(pos)]
    marked = field.count_marked(adjacent)
    opened = field.count_open(adjacent)
    if field.get_cell(pos).number == marked and marked + opened < len(adjacent) and field.get_cell(pos).opened and field.get_cell(pos) not in clicked\
            :
        print(f"Candidate: {len(adjacent)}:{opened}:{marked} - {pos.x}, {pos.y}")
        return True
    return False

def calculate_candidate() -> tuple[Cell, Vector2] | None:
    for y, row in enumerate(field.cells):
        for x, cell in enumerate(row):
            if is_candidate(Vector2(x, y)):
                clicked.add(cell)
                return cell, Vector2(x, y)
    return None

starter_coords = Vector2(7, 7)
starter_cell = field.get_cell(starter_coords)
gui.click(starter_cell.screen_coords.x + Globals.cell_scan_offset, starter_cell.screen_coords.y + Globals.cell_scan_offset)

delay = config_parser.get_animation_delay()
time.sleep(delay * 2)

sc.update_field_proximity(field, starter_coords)
while True:
    set_flags()
    candidate = calculate_candidate()
    if candidate is not None:
        coords = candidate[0].screen_coords
        gui.middleClick(coords.x + Globals.cell_scan_offset, coords.y + Globals.cell_scan_offset)
        time.sleep(delay)
        sc.update_field_proximity(field, candidate[1])
    else: exit(-1)
    visualize_field(field)
    sc.wait_for_game()
