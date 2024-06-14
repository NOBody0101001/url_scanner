import requests
from bs4 import BeautifulSoup
import logging
import socket
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_sql_injection(soup):
    sql_patterns = ["SELECT", "UNION", "INSERT", "UPDATE", "DELETE", "DROP"]
    if any(pattern in soup.text.upper() for pattern in sql_patterns):
        return "Olası SQL Enjeksiyonu"
    return None

def check_xss(soup):
    xss_patterns = ["<script>", "javascript:", "onerror=", "onload="]
    if any(pattern in soup.prettify().lower() for pattern in xss_patterns):
        return "Olası XSS (Cross-Site Scripting) Açığı"
    return None

def check_csrf_protection(soup):
    forms = soup.find_all('form')
    for form in forms:
        if 'csrf' not in form.prettify().lower():
            return "CSRF Koruma Eksikliği"
    return None

def check_clickjacking_protection(response):
    if "X-Frame-Options" not in response.headers:
        return "Clickjacking Koruma Eksikliği (X-Frame-Options Başlığı)"
    return None

def check_security_headers(response):
    missing_headers = []
    security_headers = {
        "Content-Security-Policy": "İçerik Güvenlik Politikası (CSP)",
        "Strict-Transport-Security": "Katı Taşıma Güvenliği (HSTS)",
        "X-Content-Type-Options": "İçerik Tipi Seçenekleri (XCTO)",
        "X-XSS-Protection": "XSS Koruması (XXSSP)",
        "Referrer-Policy": "Yönlendirme Politikası",
        "Permissions-Policy": "İzinler Politikası"
    }
    for header, name in security_headers.items():
        if response.headers.get(header) is None or response.headers.get(header).strip() == "":
            missing_headers.append(f"{name} Başlığı Eksik ({header})")
    return missing_headers

def check_https_usage(url):
    if not url.lower().startswith('https'):
        return "URL HTTPS kullanmıyor"
    return None

def check_server_information(response):
    if "Server" in response.headers:
        return f"Sunucu Bilgisi: {response.headers['Server']}"
    return None

def check_cookie_security(response):
    cookies = response.headers.get('Set-Cookie')
    if cookies:
        insecure_cookies = [cookie for cookie in cookies.split(',') if "Secure" not in cookie or "HttpOnly" not in cookie]
        if insecure_cookies:
            return "Güvensiz Çerezler Tespit Edildi (Secure ve HttpOnly bayrakları eksik)"
    return None

def port_scanner(host):
    open_ports = []
    filtered_ports = []
    closed_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 123, 135, 139, 143, 443, 445, 3389]

    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        elif result == 1:
            closed_ports.append(port)
        else:
            filtered_ports.append(port)
        sock.close()
    
    return open_ports, closed_ports, filtered_ports

def url_scanner(url):
    vulnerabilities = []
    checks = [
        ("HTTPS Kullanımı", check_https_usage, url),
        ("SQL Enjeksiyonu", check_sql_injection, None),
        ("XSS (Cross-Site Scripting)", check_xss, None),
        ("CSRF Koruma", check_csrf_protection, None),
        ("Clickjacking Koruma", check_clickjacking_protection, None),
        ("Güvenlik Başlıkları", check_security_headers, None),
        ("Sunucu Bilgisi", check_server_information, None),
        ("Çerez Güvenliği", check_cookie_security, None)
    ]

    https_vuln = check_https_usage(url)
    if https_vuln:
        vulnerabilities.append(https_vuln)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"{url} adresine erişimde hata: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Check each type of vulnerability
    for check_name, check_func, check_param in checks:
        logging.info(f"{check_name} kontrol ediliyor...")
        param = soup if check_func not in [check_clickjacking_protection, check_security_headers, check_server_information, check_cookie_security] else response
        result = check_func(param if check_param is None else check_param)
        if result:
            vulnerabilities.append((check_name, result))

    # Check for open ports
    try:
        host = url.split("//")[-1].split("/")[0]
        open_ports, closed_ports, filtered_ports = port_scanner(host)
        vulnerabilities.append(("Açık Portlar", open_ports))
        vulnerabilities.append(("Kapalı Portlar", closed_ports))
        vulnerabilities.append(("Filtreli Portlar", filtered_ports))
    except Exception as e:
        logging.error(f"Port taraması yapılamadı: {e}")

    # Print the vulnerabilities found
    if vulnerabilities:
        logging.info(f"{url} adresinde bulunan güvenlik açıkları:")
        for check_name, result in vulnerabilities:
            if isinstance(result, list):
                logging.info(f"{check_name}: {', '.join(map(str, result))}")
            else:
                logging.info(f"{check_name}: {result}")
    else:
        logging.info(f"{url} güvenli görünüyor")

def main():
    clear_terminal()

    text_art = """
             \033[31m
                     :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!                                           !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$   •   `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$   •  /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~ \033[0m

    ========================================
                Made by protocolhere :)
    ========================================
    1. URL Tarayıcı
    2. Çıkış
    ========================================
    """
    
    while True:
        print(text_art)
    
        choice = input("Lütfen bir seçenek seçin: ")
    
        if choice == "1":
            url = input("URL girin: ")
            url_scanner(url)
            another_scan = input("Başka bir tarama yapmak istiyor musunuz? (y/n): ").lower()
            if another_scan != 'y':
                break
            clear_terminal()
        elif choice == "2":
            clear_terminal()
            print("\033[33mKullandığınız için teşekkürler :)\033[0m")
            break
        else:
            print("Geçersiz seçim. Lütfen 1 veya 2 numaralı seçeneği seçin.")
            clear_terminal()

if __name__ == "__main__":
    main()
