import itertools
import requests
import csv
import smtplib
import time
from email.mime.text import MIMEText

# ==============================
# BANNER
# ==============================
def banner():
    print(r"""
  ____                              _              _   _ _       _       
 |  _ \  ___  _ __ ___   ___  _ __ (_) ___  _ __  | | | (_)_ __ | | __  
 | | | |/ _ \| '_ ` _ \ / _ \| '_ \| |/ _ \| '_ \ | |_| | | '_ \| |/ /  
 | |_| | (_) | | | | | | (_) | | | | | (_) | | | ||  _  | | |_) |   <   
 |____/ \___/|_| |_| |_|\___/|_| |_|_|\___/|_| |_||_| |_|_| .__/|_|\_\  
                                                        |_|            

        Domaine Hippie v1.0
        Domain Hunting & Typosquatting Tool
        ----------------------------------- 
        Desenvolvido por F. Hgo Viana
    """)

def loading():
    print("[+] Inicializando módulos...")
    time.sleep(1)
    print("[+] Carregando engine de variações...")
    time.sleep(1)
    print("[+] Iniciando scanner...\n")
    time.sleep(1)


# ==============================
# CONFIG EMAIL (SOMENTE SENDER)
# ==============================
SENDER_EMAIL = "XXXXXXXXX@gmail.com"
SENDER_PASSWORD = "XXXXXXXXXXXXXX"


# ==============================
# CHAR MAP
# ==============================
CHAR_MAP = {
    "a": ["4"],
    "b": ["8", "6"],
    "c": [],
    "d": [],
    "e": ["3"],
    "f": [],
    "g": ["9"],
    "h": [],
    "i": ["1", "l"],
    "j": [],
    "k": [],
    "l": ["1", "i"],
    "m": ["nn", "rn"],
    "n": ["m"],
    "o": ["0"],
    "p": [],
    "q": ["9"],
    "r": [],
    "s": ["5"],
    "t": ["7"],
    "u": ["v"],
    "v": ["u"],
    "w": ["vv"],
    "x": [],
    "y": [],
    "z": ["2"]
}

# ==============================
# TLDs
# ==============================
TLDS = [
    ".com", ".com.br", ".net", ".org",
    ".info", ".biz",
    ".xyz", ".top", ".online", ".site",
    ".store", ".tech", ".club", ".vip",
    ".app", ".dev", ".cloud",
    ".co", ".io", ".ai",
    ".net.br", ".org.br"
]


# ==============================
# ENVIO DE EMAIL
# ==============================
def send_email(domain, status, final_url, receivers):
    subject = f"[ALERTA] Domínio ativo encontrado: {domain}"

    body = f"""
Domínio ativo detectado!

Domínio: {domain}
Status: {status}
URL final: {final_url}
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(receivers)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(
                SENDER_EMAIL,
                receivers,
                msg.as_string()
            )

        print(f"[EMAIL ENVIADO] {domain}")

    except Exception as e:
        print(f"[ERRO EMAIL] {e}")


# ==============================
# GERA VARIAÇÕES
# ==============================
def generate_all_variations(word):
    char_options = []

    for char in word:
        replacements = CHAR_MAP.get(char, [])
        char_options.append([char] + replacements)

    for combo in itertools.product(*char_options):
        yield "".join(combo)


# ==============================
# CHECK DOMÍNIO
# ==============================
def check_domain(domain):
    urls = [
        f"https://{domain}",
        f"http://{domain}"
    ]

    for url in urls:
        try:
            r = requests.get(
                url,
                timeout=5,
                allow_redirects=True
            )
            return r.status_code, r.url
        except:
            continue

    return None, None


# ==============================
# MAIN
# ==============================
def main():
    banner()
    loading()

    # INPUT EMAILS
    receivers = input("Digite os e-mails separados por vírgula: ").split(",")
    receivers = [r.strip() for r in receivers if "@" in r]

    # INPUT KEYWORDS
    keywords = input("Digite palavras separadas por vírgula: ").split(",")
    keywords = [k.strip().lower() for k in keywords]

    sent_domains = set()

    with open("resultado.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["dominio", "status", "final_url"])

        for keyword in keywords:
            print(f"\n[+] Processando: {keyword}")

            for variation in generate_all_variations(keyword):
                for tld in TLDS:
                    domain = variation + tld

                    status, final_url = check_domain(domain)

                    print(f"{domain} -> {status}")

                    writer.writerow([domain, status, final_url])

                    if status == 200 and domain not in sent_domains:
                        send_email(domain, status, final_url, receivers)
                        sent_domains.add(domain)

    print("\n[+] CSV gerado com sucesso!")


if __name__ == "__main__":
    main()