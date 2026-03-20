'''
lagerhanterare2.py: Lagerhanterare i curses med csv.
__author__  = Max Valentin
__version__ = 2.1
__email__   = max.valentin@elev.ga.dbgy.se
'''

import curses
import csv

CSV_FILE = "projekt2/db_products.csv"

COLUMN_WIDTHS = {
    "ID": 3,
    "Name": 25,
    "Description": 50,
    "Price": 10,
    "Quantity": 8
}

LABELS = [
    "       Name:  ",
    "Description:  ",
    "      Price:  ",
    "   Quantity:  "
]


MAX_LENGTHS = [35, 90, 10, 8]

def load_csv(filename):
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        print("Error: Could not find CSV file.")
        return False
    

def save_csv(filename, header, content):
    content = sort_content(content, "ID", True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(content)

def truncate(text, width):
    text = str(text)
    return text[:width - 3] + "..." if len(text) > width else text.ljust(width)

def draw_row(stdscr, y, row, selected):
    x = 2
    for i, key in enumerate(COLUMN_WIDTHS):
        cell = truncate(row[i], COLUMN_WIDTHS[key])
        stdscr.addstr(y, 0, "│")
        stdscr.addstr(y, x, cell, curses.A_REVERSE if selected else 0)
        x += COLUMN_WIDTHS[key]
        if i < len(COLUMN_WIDTHS):
            stdscr.addstr(y, x, " │ ")
            x += 3

def draw_header(stdscr):
    x = 2
    for key in COLUMN_WIDTHS:
        stdscr.addstr(2, 0, "│")
        stdscr.addstr(2, x, f"{truncate(key, COLUMN_WIDTHS[key])} │")
        x += COLUMN_WIDTHS[key]
        if key != list(COLUMN_WIDTHS)[-1]:
            stdscr.addstr(2, x, " │ ")
            x += 3

def draw_line(stdscr, y, start_sign = "─", middle_sign = "─", end_sign = "─"):
    stdscr.addstr(y, 0, start_sign + "─" * 5 + middle_sign + "─" * 27 + middle_sign + "─" * 52 + middle_sign + "─" * 12 + middle_sign + "─" * 10 + end_sign)


def product_form(stdscr, row, title):
    curses.curs_set(1)
    field = 0
    pos = len(row[1])
    feedback = ""

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title)
        draw_line(stdscr, 1)

        y0 = 3
        for i, label in enumerate(LABELS):
            value = row[i + 1]
            attr = curses.A_REVERSE if i == field else 0
            stdscr.addstr(y0 + i, 0, label + value.ljust(MAX_LENGTHS[i]), attr)

        draw_line(stdscr, y0+5)
        stdscr.addstr(y0 + 7, 0, "TAB: Next   SHIFT+TAB: Previous   ENTER: Save   ESC: Cancel")
        if feedback:
            stdscr.addstr(y0 + 8, 0, feedback, curses.color_pair(1) if curses.has_colors() else curses.A_BOLD)

        pos = min(pos, len(row[field + 1]))
        stdscr.move(y0 + field, len(LABELS[field]) + pos)
        stdscr.refresh()

        key = stdscr.get_wch()
        if key == "\t":
            field = (field + 1) % 4
            pos = len(row[field + 1])
        elif key == curses.KEY_BTAB:
            field = (field - 1) % 4
            pos = len(row[field + 1])
        elif key == "\n":
            name, desc, price, quantity = row[1], row[2], row[3], row[4]
            if not name.strip() or not desc.strip() or not price.strip() or not quantity.strip():
                feedback = "All fields must be filled!"
                continue
            curses.curs_set(0)
            return True
        elif key == "\x1b":
            curses.curs_set(0)
            return False
        elif key in ("\b", "\x7f"):
            if pos > 0:
                text = row[field + 1]
                row[field + 1] = text[:pos - 1] + text[pos:]
                pos -= 1
        elif key == curses.KEY_LEFT:
            pos = max(pos - 1, 0)
        elif key == curses.KEY_RIGHT:
            pos = min(pos + 1, len(row[field + 1]))
        elif isinstance(key, str):
            current = row[field + 1]
            if field == 2:
                if key.isdigit() or (key == "." and "." not in current):
                    if len(current) < MAX_LENGTHS[field]:
                        row[field + 1] = current[:pos] + key + current[pos:]
                        pos += 1
            elif field == 3:
                if key.isdigit():
                    if len(current) < MAX_LENGTHS[field]:
                        row[field + 1] = current[:pos] + key + current[pos:]
                        pos += 1
            else:
                if len(current) < MAX_LENGTHS[field]:
                    row[field + 1] = current[:pos] + key + current[pos:]
                    pos += 1

def create_new_product(stdscr, content):
    new_id = str(max((int(r[0]) for r in content), default=0) + 1)
    row = [new_id, "", "", "", ""]
    if product_form(stdscr, row, f"NEW PRODUCT : ID {new_id}"):
        content.append(row)

def edit_product(stdscr, row):
    temp_row = row.copy()
    if product_form(stdscr, temp_row, f"EDITING PRODUCT WITH ID: {row[0]}"):
        for i in range(1, 5):
            row[i] = temp_row[i]

def view_details(stdscr, row, content):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"SHOWING PRODUCT WITH ID: {row[0]}")
        draw_line(stdscr, 1)
        stdscr.addstr(3, 0, f"       Name:  {row[1]}")
        stdscr.addstr(4, 0, f"Description:  {row[2]}")
        stdscr.addstr(5, 0, f"      Price:  {row[3]} kr")
        stdscr.addstr(6, 0, f"   Quantity:  {row[4]}")
        draw_line(stdscr, 8)
        stdscr.addstr(10, 0, "Enter: Edit   Del: Delete   Esc: Back")
        stdscr.refresh()

        key = stdscr.get_wch()
        if key == "\n":
            edit_product(stdscr, row)
        elif key == curses.KEY_DC:
            if confirm_delete(stdscr, row[1]):
                content.remove(row)
                break
        elif key == "\x1b":
            break

def confirm_delete(stdscr, name):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, max(0,(55-len(name))//2), f'Are you sure you want to delete "{name}"? This action cannot be undone.')
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    selected = 0
    while True:
        attr_nej = curses.color_pair(1) | (curses.A_REVERSE if selected == 0 else 0)
        attr_ja = curses.color_pair(2) | (curses.A_REVERSE if selected == 1 else 0)
        stdscr.addstr(2, 44, "CANCEL", attr_nej)
        stdscr.addstr(2, 64, "CONFIRM", attr_ja)
        stdscr.refresh()
        key = stdscr.get_wch()
        if key in (curses.KEY_LEFT, curses.KEY_RIGHT):
            selected = 1 - selected
        elif key in ("\n", 10, 13):
            return selected == 1
        elif key == "\x1b":
            return False

def confirm_quit(stdscr):
    no_list = [ " _   _  ____  ",
               r"| \ | |/ __ \ ",
               r"|  \| | |  | |",
                "| . ` | |  | |",
               r"| |\  | |__| |",
               r"|_| \_|\____/ "]
    yes_list = [ "__     ________  _____ ",
                r"\ \   / /  ____|/ ____|",
                r" \ \_/ /| |__  | (___  ",
                r"  \   / |  __|  \___ \ ",
                "   | |  | |____ ____) |",
                "   |_|  |______|_____/ ",]
    
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 45, "Are you sure you want to quit?")
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    selected = 0
    while True:
        attr_no = curses.color_pair(1) | (curses.A_REVERSE if selected == 0 else 0)
        attr_yes = curses.color_pair(2) | (curses.A_REVERSE if selected == 1 else 0)
        for i, j in enumerate(no_list):
            stdscr.addstr(i+2, 36, j, attr_no)
        for i, j in enumerate(yes_list):
            stdscr.addstr(i+2, 64, j, attr_yes)

        stdscr.refresh()
        key = stdscr.get_wch()
        if key in (curses.KEY_LEFT, curses.KEY_RIGHT):
            selected = 1 - selected
        elif key in ("\n", 10, 13):
            return selected == 1
        elif key == "\x1b":
            return False

def sort_content(content, sortingtype, ascending=True):
    index_map = {"ID":0, "Price":3, "Quantity":4}
    idx = index_map.get(sortingtype)
    if sortingtype == "Price":
        return sorted(content, key=lambda r: float(r[idx]) if r[idx] else 0.0, reverse=not ascending)
    else:
        return sorted(content, key=lambda r: int(r[idx]) if r[idx] else 0, reverse=not ascending)

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    
    sorting_by = "ID"
    ascending_text = "Ascending"
    ascending = True

    data = load_csv(CSV_FILE)
    if data == False:
        quit()
    header, content = data[0], data[1:]

    selected, start = 0, 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"LAGERHANTERARE   ↑/↓ Move   ENTER: View   N: New   S: Save   ESC: Quit   Showing items by: {sorting_by} ({ascending_text})")
        draw_line(stdscr, 1, "┌", "┬", "┐")
        draw_header(stdscr)
        draw_line(stdscr, 3, "├", "┼", "┤")
        sorting_list = ["Sort by:", "", "1: ID", "2: Price", "3: Quantity", "", "R: Reverse order"]
        for idx, item in enumerate(sorting_list):
            stdscr.addstr(3+idx, 113, item)

        y = 4
        for i in range(start, len(content)):
            draw_row(stdscr, y, content[i], i == selected)
            y += 1
            if y > curses.LINES - 2:
                break
            
        draw_line(stdscr, 14, "└", "┴", "┘")
        
        key = stdscr.get_wch()
        if key in (curses.KEY_UP, curses.KEY_BTAB) and selected > 0:
            selected -= 1
            if selected < start: start -= 1
        elif key in (curses.KEY_DOWN, "\t") and selected < len(content)-1:
            selected += 1
            if selected >= start + curses.LINES - 6: start += 1
        elif key == "\n":
            view_details(stdscr, content[selected], content)
        elif key in ("n","N"):
            create_new_product(stdscr, content)
        elif key in ("s","S"):
            save_csv(CSV_FILE, header, content)
        elif key in ("r", "R"):
            if ascending:
                ascending = False
                ascending_text = "Descending"
            else:
                ascending = True
                ascending_text = "Ascending"
            selected, start = 0, 0
            content = sort_content(content, sorting_by, ascending)
        elif key=="1" and sorting_by != "ID":
            content = sort_content(content,"ID", ascending)
            sorting_by = "ID"
            selected, start = 0, 0
        elif key=="2" and sorting_by != "Price":
            content = sort_content(content,"Price", ascending)
            sorting_by = "Price"
            selected, start = 0, 0
        elif key=="3" and sorting_by != "Quantity":
            content = sort_content(content,"Quantity", ascending)
            sorting_by = "Quantity"
            selected, start = 0, 0
        elif key == "\x1b":
            if confirm_quit(stdscr):
                break

curses.wrapper(main)
