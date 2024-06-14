import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_sql_injection(soup):
    sql_patterns = ["SELECT", "UNION", "INSERT", "UPDATE", "DELETE", "DROP"]
    if any(pattern in soup.text.upper() for pattern in sql_patterns):
        return "Olası SQL Enjeksiyonu"
    return None

def check_xss(soup):
    if "<script>" in soup.prettify().lower():
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
        if (response.headers.get(header) is None or 
            response.headers.get(header).strip() == ""):
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
            vulnerabilities.append(result)

    # Print the vulnerabilities found
    if vulnerabilities:
        logging.info(f"{url} adresinde bulunan güvenlik açıkları:")
        for vulnerability in vulnerabilities:
            logging.info(vulnerability)
    else:
        logging.info(f"{url} güvenli görünüyor")

# Main function to display the menu and handle user input
def main():
    text_art = """
      \033[31m       :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
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
    1. url scanner
    ========================================
    """
    
    print(text_art)
    
    choice = input("Lütfen bir seçenek seçin: ")
    
    if choice == "1":
        url = input("URL girin: ")
        url_scanner(url)
    else:
        print("Geçersiz seçim. Lütfen 1 numaralı seçeneği seçin.")

if __name__ == "__main__":
    main()
