import sys
import requests
import re

def fetch_api(url):
    try:
        # إضافة https إذا لم تكن موجودة
        if not url.startswith("http"):
            url = "https://" + url
            
        print(f"[*] Connecting to {url}...")
        response = requests.get(url, timeout=10)
        content = response.text
        
        # البحث عن أنماط تشبه مفاتيح الـ API (مثل API_KEY, SECRET_KEY)
        # هذا نمط بحث عام، يمكنك تعديله حسب نوع الـ API الذي تبحث عنه
        api_patterns = [
            r"api[_-]key['\s]*[:=]['\s]*([a-zA-Z0-9_-]+)",
            r"secret['\s]*[:=]['\s]*([a-zA-Z0-9_-]+)",
            r"token['\s]*[:=]['\s]*([a-zA-Z0-9_-]+)"
        ]
        
        found = False
        for pattern in api_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                print(f"[!] Found Potential API: {match}")
                found = True
        
        if not found:
            print("[-] No API key found in standard patterns.")
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fetch_api(sys.argv[1])
    else:
        print("Usage: python api.py <url>")
      
