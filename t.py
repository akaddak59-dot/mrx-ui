import curses
import os
import time
import random
import sys

def draw_matrix(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    for _ in range(8):
        stdscr.clear()
        for i in range(h - 1):
            line = "".join([chr(random.randint(33, 126)) for _ in range(w - 1)])
            try: stdscr.addstr(i, 0, line, curses.color_pair(1))
            except: pass
        stdscr.refresh()
        time.sleep(0.04)

def draw_mrx_logo(stdscr):
    logo = [
        r" /$$      /$$ /$$$$$$$  /$$   /$$",
        r"| $$$    /$$$| $$__  $$| $$  / $$",
        r"| $$$$  /$$$$| $$  \ $$|  $$/ $$/",
        r"| $$ $$/$$ $$| $$$$$$$/ \  $$$$/ ",
        r"| $$  $$$| $$| $$__  $$  >$$  $$ ",
        r"| $$\  $ | $$| $$  \ $$ /$$/\  $$",
        r"| $$ \/  | $$| $$  | $$| $$  \ $$",
        r"|__/     |__/|__/  |__/|__/  |__/"
    ]
    for i, line in enumerate(logo):
        stdscr.addstr(i, (curses.COLS - len(line)) // 2, line, curses.color_pair(2) | curses.A_BOLD)

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    draw_matrix(stdscr)
    curses.curs_set(1)

    user_val, pass_val = "", ""
    sel = 0

    # --- تسجيل الدخول ---
    while True:
        stdscr.clear()
        stdscr.addstr(5, 10, f"Username: {user_val} {'<' if sel == 0 else ''}")
        stdscr.addstr(6, 10, f"Password: {'*' * len(pass_val)} {'<' if sel == 1 else ''}")
        stdscr.addstr(8, 10, "[ OK ]" if sel != 2 else "[>OK<]", curses.A_REVERSE if sel == 2 else 0)
        stdscr.addstr(8, 20, "[ NO ]" if sel != 3 else "[>NO<]", curses.A_REVERSE if sel == 3 else 0)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and sel > 0: sel -= 1
        elif key == curses.KEY_DOWN and sel < 3: sel += 1
        elif key == curses.KEY_LEFT and sel == 3: sel = 2
        elif key == curses.KEY_RIGHT and sel == 2: sel = 3

        elif key in [10, 13]:
            if sel == 2:
                if user_val.upper() == "MRX" and pass_val.upper() == "KAIL":
                    break
                else:
                    err_win = curses.newwin(3, 30, (curses.LINES-3)//2, (curses.COLS-30)//2)
                    err_win.bkgd(' ', curses.color_pair(2))
                    err_win.box()
                    err_win.addstr(1, 4, "WRONG PASSWORD/USER!")
                    err_win.refresh()
                    time.sleep(1)
                    user_val, pass_val = "", ""
            elif sel == 3: sys.exit()

        elif key in [8, 127]:
            if sel == 0: user_val = user_val[:-1]
            elif sel == 1: pass_val = pass_val[:-1]
        elif 32 <= key <= 126 and sel < 2:
            if sel == 0: user_val += chr(key)
            elif sel == 1: pass_val += chr(key)

    # --- القائمة الرئيسية ---
    tools = [
        {"name": "TikTok Reports", "cmd": "python tek.py"},
        {"name": "Facebook Reports", "cmd": "python fes.py"},
        {"name": "Telegram Reports", "cmd": "python tej.py"},
        {"name": "DDOS Attack", "cmd": "python ddos.py"},
        {"name": "Fetch API", "cmd": "python api.py"},
        {"name": "Gmail Spam", "cmd": "python gmail.py"},
        {"name": "Calls Spam", "cmd": "python calls.py"},
        {"name": "SMS Spam", "cmd": "python sms.py"},
        {"name": "EXIT", "cmd": "exit"}
    ]

    tool_sel = 0
    curses.curs_set(0)
    while True:
        stdscr.clear()
        draw_mrx_logo(stdscr)
        for i, tool in enumerate(tools):
            attr = curses.A_REVERSE if i == tool_sel else 0
            color = curses.color_pair(2) if tool["name"] == "EXIT" else curses.color_pair(3)
            prefix = "> " if i == tool_sel else "  "
            stdscr.addstr(i + 9, 2, f"{prefix}{tool['name']}", attr | color)

        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and tool_sel > 0: tool_sel -= 1
        elif key == curses.KEY_DOWN and tool_sel < len(tools) - 1: tool_sel += 1
        elif key in [10, 13]:
            if tools[tool_sel]["name"] == "EXIT": sys.exit()
            else:
                curses.endwin()
                os.system(tools[tool_sel]["cmd"])
                input("\nPress Enter to return...")
                curses.wrapper(main)
                break

if __name__ == "__main__":
    curses.wrapper(main)
