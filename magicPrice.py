import json
import re

from bs4 import BeautifulSoup as sp
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pyautogui as pt

# WEB crawler - FATEC São Caetano do Sul
# Melhorias:
# - Criar uma lista com vários sites de clima e rodar um for com a qtde de sites passando cada item para requests.get

# Pega o conteudo da pagina
# resp = requests.get('https://www.ligamagic.com.br/?view=cards/card&card=Stoneforge+Mystic&aux=Mistico+Litoforjador&show=1')
# content = resp.content
#
# site = sp(content, 'html.parser')  # Transforma o conteudo do content em html
# print(type(site))  # retorna <class 'bs4.BeautifulSoup'>
# print(site.prettify())  # imprime o site organizadamente
#
#
# # Retorna o conteudo de uma div ou tag especifica (temp. Max e Min)
# post = site.find('span', attrs={'class': 'bigger'})
# print(post)
from selenium.webdriver.support.wait import WebDriverWait


def codigoFonte(url):
    crg_opt = webdriver.ChromeOptions()
    crg_opt.add_argument('--headless')
    crg_opt.add_argument('disable-notifications')
    crg_opt.add_argument('disable-geolocations')
    ser = Service("chromedriver.exe")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get(url)
    driver.maximize_window()
    preco = driver.execute_script("return g_avgprice")
    print(preco)
    data = json.loads(preco)
    print(data)
    print(type(data))
    # sleep(5)
    # pt.moveTo(1185, 681)
    # pt.click(1185, 681)
    # sleep(5)
    # pt.click(393, 54)
    # pt.hotkey('ctrl', 'c')
    # sleep(5)
    # pt.click(1146, 149)
    # sleep(2)
    # pt.click(1016, 253)
    # pt.typewrite("Only1Billy", interval=0.12)
    # pt.click(1032, 299)
    # pt.typewrite("293234619Gab!", interval=0.12)
    # pt.click(1062, 378)
    # sleep(5)
    # # < button onclick = "cookieAccept();" > Permitir Todos os Cookies < / button >
    # pt.click(1117, 168)
    # sleep(2)
    # pt.click(393, 54)
    # pt.hotkey('ctrl', 'v')
    # sleep(5)
    # pt.press('enter')
    # sleep(5)
    # driver.find_element(by=By.CLASS_NAME, value='mp-btn-comprar-btn-alerta ').click()
    # sleep(10)
    return driver.page_source


# popupAlertaPreco preco-menor-value AlertaPreco.showPopup(1131);
def procCodigoFonte(cf):
    soup = sp(cf, 'html.parser')
    # soupStr = str(soup)
    # teste = re.search(r'g_avgprice=(.*),"precoMaior":', soupStr)
    # print(teste)
    getValueFromSpan = soup.find('span', attrs={'id': 'preco-menor-value'})
    # print(getValueFromSpan)
    return getValueFromSpan.text


# m=re.search(r'<(.*)>','abevbv envvrhwkv <eiwbv> ebvi <wieunv> ajhbsvhj')
url = 'https://www.ligamagic.com.br/?view=cards/card&card=Stoneforge+Mystic&aux=Mistico+Litoforjador&show=1'
cdFonte = codigoFonte(url)
# print(cdFonte)
print(procCodigoFonte(cdFonte))


