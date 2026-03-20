import curses

board = '''┌───┬───┐\n│   │   │'''
def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, board)
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
