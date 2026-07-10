import curses, os, time, random, sys, threading, requests, re

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
    stdscr.addstr(9, (curses.COLS - 30) // 2, "______________________________", curses.color_pair(3))

# --- منطق الأدوات المدمج ---
def perform_ddos(stdscr, url):
    stdscr.clear(); draw_mrx_logo(stdscr)
    stdscr.addstr(12, 2, f"Attacking: {url} ...", curses.color_pair(3))
    for i in range(101):
        bar = "#" * (i // 2)
        stdscr.addstr(14, 2, f"Progress: [{bar:<50}] {i}%")
        stdscr.refresh(); time.sleep(0.04)
    stdscr.addstr(16, 2, "TARGET DOWN!", curses.color_pair(2))
    stdscr.addstr(18, 2, "[ OK ] Return to Menu", curses.A_REVERSE)
    stdscr.getch(); os.system("python " + sys.argv[0]) # إعادة التشغيل

def perform_api(stdscr, url):
    stdscr.clear(); draw_mrx_logo(stdscr)
    try:
        res = requests.get(url if url.startswith("http") else "https://"+url, timeout=5)
        found = re.findall(r"api[_-]key['\s]*[:=]['\s]*([a-zA-Z0-9_-]+)", res.text, re.I)
        if found:
            stdscr.addstr(12, 2, f"FOUND API: {found[0]}", curses.color_pair(3))
        else:
            raise Exception("NO API FOUND")
    except:
        err = curses.newwin(3, 30, 12, (curses.COLS-30)//2)
        err.bkgd(' ', curses.color_pair(2)); err.box(); err.addstr(1, 8, "NO API FOUND!")
        err.refresh(); time.sleep(2)
    stdscr.addstr(18, 2, "[ OK ] Exit", curses.A_REVERSE)
    stdscr.getch(); os.system("python " + sys.argv[0]); sys.exit()

# --- القائمة الرئيسية ---
def main(stdscr):
    curses.curs_set(0); curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, 0); curses.init_pair(2, curses.COLOR_RED, 0); curses.init_pair(3, curses.COLOR_CYAN, 0)
    
    tools = ["TikTok Reports", "Facebook Reports", "Telegram Reports", "DDOS Attack", "Fetch API", "Gmail Spam", "Calls Spam", "SMS Spam", "EXIT"]
    sel = 0
    while True:
        stdscr.clear(); draw_mrx_logo(stdscr)
        for i, tool in enumerate(tools):
            prefix = "> " if i == sel else "  "
            stdscr.addstr(i + 11, 2, f"{prefix}{tool}", curses.A_REVERSE if i == sel else 0)
        
        k = stdscr.getch()
        if k == curses.KEY_UP and sel > 0: sel -= 1
        elif k == curses.KEY_DOWN and sel < len(tools)-1: sel += 1
        elif k in [10, 13]:
            if tools[sel] == "EXIT": sys.exit()
            elif tools[sel] == "DDOS Attack":
                # واجهة إدخال الرابط داخل نفس الملف
                curses.echo(); stdscr.addstr(22, 2, "Enter URL: "); url = stdscr.getstr(23, 2, 30).decode()
                perform_ddos(stdscr, url)
            elif tools[sel] == "Fetch API":
                curses.echo(); stdscr.addstr(22, 2, "Enter URL: "); url = stdscr.getstr(23, 2, 30).decode()
                perform_api(stdscr, url)
            else:
                stdscr.addstr(22, 2, "Coming Soon..."); stdscr.refresh(); time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
    
