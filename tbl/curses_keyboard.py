"""
Curses keyboard handling.

To test keyboard response, run `python -m tbl.curses_keyboard`; press q to exit.
"""

#-------------------------------------------------------------------------------

import curses
import logging

#-------------------------------------------------------------------------------

ESC = 27

KEYS = {
      0:    "C-SPACE",
      1:    "C-a",
      2:    "C-b",
      3:    "C-c",
      4:    "C-d",
      5:    "C-e",
      6:    "C-f",
      7:    "C-g",
      9:    "TAB",
     10:    "RETURN",
     11:    "C-k",
     12:    "C-l",
     14:    "C-n",
     15:    "C-o",
     16:    "C-p",
     17:    "C-q",
     18:    "C-r",
     19:    "C-s",
     20:    "C-t",
     21:    "C-u",
     22:    "C-v",
     23:    "C-w",
     24:    "C-x",
     25:    "C-y",
     26:    "C-z",
     27:    "ESC",
     32:    "SPACE",
    127:    "BACKSPACE",
    258:    "DOWN",
    259:    "UP",
    260:    "LEFT",
    261:    "RIGHT",
    262:    "HOME",
    265:    "F1",
    266:    "F2",
    267:    "F3",
    268:    "F4",
    269:    "F5",
    270:    "F6",
    271:    "F7",
    272:    "F8",
    273:    "F9",
    274:    "F10",
    275:    "F11",
    276:    "F12",
    330:    "DELETE",
    338:    "PAGEDOWN",
    339:    "PAGEUP",
    343:    "ENTER",
    360:    "END",
    393:    "S-LEFT",
    402:    "S-RIGHT",
}        

META_KEYS = {
     98:    "M-LEFT",   # M-b
    102:    "M-RIGHT",  # M-f 
}

def get_key(stdscr):
    meta = False
    while True:
        c = stdscr.getch()
        if c == ESC:
            if meta:
                return "M-ESC"
            else:
                meta = True
                continue
        elif c == curses.ERR:
            # Not sure why we get these.
            continue
        elif c == curses.KEY_RESIZE:
            sy, sx = stdscr.getmaxyx()
            return "RESIZE", (sx, sy)
        elif c == curses.KEY_MOUSE:
            _, x, y, _, state = curses.getmouse()
            # FIXME: Not sure if we have buttons 2/3 right.
            if state & curses.BUTTON1_CLICKED:
                key = "LEFTCLICK"
            elif state & curses.BUTTON1_DOUBLE_CLICKED:
                key = "LEFTDBLCLICK"
            elif state & curses.BUTTON2_CLICKED:
                key = "RIGHTCLICK"
            elif state & curses.BUTTON2_DOUBLE_CLICKED:
                key = "RIGHTDBLCLICK"
            elif state & curses.BUTTON3_CLICKED:
                key = "MIDDLECLICK"
            elif state & curses.BUTTON3_DOUBLE_CLICKED:
                key = "MIDDLEDBLCLICK"
            else:
                # Discard other messages, e.g. press/release.
                continue
            if state & curses.BUTTON_SHIFT:
                key = "S-" + key
            if state & curses.BUTTON_ALT:
                key = "M-" + key
            # FIXME: OS/X seems to produce press and release events for CTRL
            # mouse clicks, but not clicked events.
            if state & curses.BUTTON_CTRL:
                key = "C-" + key
            return "MOUSE", (key, x, y)

        try:
            return (META_KEYS if meta else KEYS)[c], None
        except KeyError:
            pass
                
        if 0 <= c < 128:
            key = chr(c)
            if meta:
                key = "M-" + key
            return key, None
        else:
            logging.warning("unrecognized key code: {}".format(c))



#-------------------------------------------------------------------------------
# Testing

def main():
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    # curses.cbreak()
    curses.raw()
    curses.curs_set(False)
    curses.mousemask(
        curses.BUTTON1_CLICKED | curses.BUTTON1_DOUBLE_CLICKED)

    try:
        history = []
        while True:
            key, arg = get_key(stdscr)
            k = "{!r}, {!r}".format(key, arg)
            history.append(k)
            if len(history) > 10:
                history.pop(0)
            stdscr.clear()
            for i in range(len(history)):
                stdscr.addstr(i, 2, history[i])
            if key == "q" or key == 113:
                break
    finally:
        curses.curs_set(True)
        curses.noraw()
        # curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    main()
