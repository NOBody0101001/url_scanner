import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_sql_injection(soup):
    sql_patterns = ["SELECT", "UNION", "INSERT", "UPDATE", "DELETE", "DROP"]
    if any(pattern in soup.text.upper() for pattern in sql_patterns):
        return "Possible SQL Injection"
    return None

def check_xss(soup):
    if "<script>" in soup.prettify().lower():
        return "Possible XSS"
    return None

def check_csrf_protection(soup):
    forms = soup.find_all('form')
    for form in forms:
        if 'csrf' not in form.prettify().lower():
            return "Missing CSRF Protection"
    return None

def check_clickjacking_protection(response):
    if "X-Frame-Options" not in response.headers:
        return "Missing Clickjacking Protection (X-Frame-Options)"
    return None

def check_security_headers(response):
    missing_headers = []
    security_headers = {
        "Content-Security-Policy": "CSP",
        "Strict-Transport-Security": "HSTS",
        "X-Content-Type-Options": "XCTO",
        "X-XSS-Protection": "XXSSP",
        "Referrer-Policy": "Referrer Policy",
        "Permissions-Policy": "Permissions Policy"
    }
    for header, name in security_headers.items():
        if (response.headers.get(header) is None or 
            response.headers.get(header).strip() == ""):
            missing_headers.append(f"Missing {name} Header ({header})")
    return missing_headers

def check_https_usage(url):
    if not url.lower().startswith('https'):
        return "URL does not use HTTPS"
    return None

def url_scanner(url):
    vulnerabilities = []

    https_vuln = check_https_usage(url)
    if https_vuln:
        vulnerabilities.append(https_vuln)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Check each type of vulnerability
    for check in [check_sql_injection, check_xss, check_csrf_protection, check_clickjacking_protection]:
        result = check(soup if check != check_clickjacking_protection else response)
        if result:
            vulnerabilities.append(result)

    # Check security headers
    vulnerabilities.extend(check_security_headers(response))

    # Print the vulnerabilities found
    if vulnerabilities:
        logging.info(f"Vulnerabilities found in {url}:")
        for vulnerability in vulnerabilities:
            logging.info(vulnerability)
    else:
        logging.info(f"{url} appears to be secure")

# Main function to display the menu and handle user input
def main():
    text_art = """
       \033[31m      :::!~!!!!!:.
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
    
    choice = input("Please select an option: ")
    
    if choice == "1":
        url = input("Enter the URL: ")
        url_scanner(url)
    else:
        print("Invalid choice. Please select option 1.")

if __name__ == "__main__":
    main()
