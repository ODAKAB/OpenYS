import json
import os

import requests
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome


class Account:
    data: str = ''
    istoken: bool = False

    def __init__(self):
        print("    [1] Kayıtlı Hesaba Gir")
        print("    [2] Token ile Gir")
        sel: int = 0
        while not sel:
            try:
                sel = int(input("  Seçiminiz: "))
                if sel == 1:
                    self.istoken = False
                elif sel == 2:
                    self.istoken = True
                else:
                    sel = 0
            except ValueError:
                sel = 0
        if self.istoken:
            self.data = str(input("  Token: "))
        else:
            self.data = str(input("  Hesap: "))


def initialprint():
    os.system('cls||clear')
    print("""
  /$$$$$$                              /$$     /$$ /$$$$$$ 
 /$$__  $$                            |  $$   /$$//$$__  $$
| $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$\  $$ /$$/| $$  \__/
| $$  | $$ /$$__  $$ /$$__  $$| $$__  $$\  $$$$/ |  $$$$$$ 
| $$  | $$| $$  \ $$| $$$$$$$$| $$  \ $$ \  $$/   \____  $$
| $$  | $$| $$  | $$| $$_____/| $$  | $$  | $$    /$$  \ $$
|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$  | $$  | $$   |  $$$$$$/
 \______/ | $$____/  \_______/|__/  |__/  |__/    \______/ 
          | $$    Hatay Zurna'sız kalan bir milletin         
          | $$       yemek borusu kopmuş demektir.           
          |__/          https://github.com/ODAKAB/OpenYS    
    """)


def getresponse(token: str) -> str:
    res = requests.post('https://tgs.name.tr/getCookie.php?all=1&token=' + token)
    return str(res.text)


def writeresponse(accname: str, response: str):
    try:
        os.mkdir('openys_cookies')
    except FileExistsError:
        pass
    file = open('openys_cookies/' + accname, 'w+')
    file.write(response)
    print(accname + ' kaydedildi.')


def readresponse(accname: str) -> str:
    try:
        os.mkdir('openys_cookies')
    except FileExistsError:
        pass
    try:
        file = open('openys_cookies/' + accname, 'r+')
        return str(file.read())
    except FileNotFoundError:
        print(accname + ' bulunamadı.')
        return ''


def validresponse(response: str) -> bool:
    try:
        jresp = json.loads(response)
        if jresp['status'] == 'true':
            for x in jresp['data']:
                pass
        return True
    except:
        return False


if __name__ == '__main__':
    initialprint()
    acc: Account = Account()
    response: str = ''
    if acc.istoken:
        response = getresponse(acc.data)
    else:
        response = readresponse(acc.data)
    if validresponse(response):
        cookies = json.loads(response)['data']
        options = Options()
        options.add_argument('--start-maximized')
        driver = Chrome(options=options)
        driver.get("https://yemeksepeti.com")
        for x in cookies:
            driver.add_cookie(x)
        driver.get("https://yemeksepeti.com")
        if acc.istoken:
            print('    Hesabı kaydetmek için hesaba isim verin (aynı isimde başka hesap varsa üstüne yazılır!)')
            accname = input('  Kayıt: ')
            if accname:
                writeresponse(accname, response)
            else:
                print('    Hesaba isim vermediğiniz için kaydedilmedi.')
    input('    Afiyet olsun.')
