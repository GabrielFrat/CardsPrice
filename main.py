import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from openpyxl import load_workbook


# Considerações:
# - Eu usei o Python 3.8 pra fazer o código, as novas versões tem diversos bugs, principalmente com o pandas
# - As bibliotecas é só dar o pip install selenium no terminal, por exemplo, isso se o VSCode n instalar direto
# - Eu testei no VSCode alêm de testar no pycharm, os dois rodaram tranquilo, eu n cronometrei mas leva uns 7 minutos pra rodar
# - o chromedriver serve pra executar o selenium

dictCard = {}
cardsTot = 0


# Função que busca o preço de cada carta
def getPreco(urlFinal):
    # tratamento de erro caso n encontre a carta no site
    try:
        crg_opt = webdriver.ChromeOptions()
        crg_opt.add_argument('--headless')
        crg_opt.add_argument('disable-notifications')
        crg_opt.add_argument('disable-geolocations')
        ser = Service("chromedriver.exe")
        op = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ser, options=op)
        driver.get(urlFinal)
        preco = driver.execute_script("return g_avgprice")
        # print(type(preco))
        return preco
    except:
        preco = 'NaN'
        return preco
    # print(preco)


# inserir o menor valor, nome e link de cada carta em lista
def criarDict(carta, precos, url):
    precosDict = json.loads(precos)
    jsonPrecos = {}
    jsonPrecos[carta] = precosDict
    valorCartaUm = 0
    valorCartaDois = 0
    for key, value in jsonPrecos.items():
        for i, j in value.items():
            for k, l in j.items():
                if k == "precoMenor":
                    if valorCartaUm == 0:
                        valorCartaUm = l
                        global cardsTot
                        cardsTot = cardsTot + 1
                        # print(cardsTot)
                    elif valorCartaDois == 0:
                        valorCartaDois = l

    dictCard[cardsTot] = {'nome': carta, 'menorPrecoUm': valorCartaUm,
                          'menorPrecoDois': valorCartaDois, 'url': url}

    return dictCard


# gerar um data frame com as listas e exportar para o excel
def exportaExcel(dictCartas):
    # print(dictCartas)
    df = pd.DataFrame(dictCartas).transpose()
    df.rename(columns={'nome': 'Nome', 'menorPrecoUm': 'Primeiro Menor Preço',
                       'menorPrecoDois': 'Segundo Menor Preço'}, inplace=True)

    df.to_excel(r'CardsMenorPreco.xlsx', sheet_name="Menor Preço")


# importar excel e consumir os links para uma lista
file_name = "Marco Busca Preços.xlsm"
df = pd.read_excel(file_name)
url = "https://www.ligamagic.com.br/?view=cards/card&card="
links = []
links = df['Carta'].tolist()
qtdeLinks = len(links)
cardName = df['Nome Da Carta'].tolist()

# rodar um for buscando cada carta
for i in range(qtdeLinks):
    urlConcat = url + links[i] # Concatena o link base com o nome carta
    # print(urlConcat)
    preco = getPreco(urlConcat)

    # faço uma validação pra n deixar entrar um valor incorreto na função e dps só exporto quando o for percorreu todos os links
    if preco != 'NaN':
        nameCard = cardName[i]
        dictFinal = criarDict(nameCard, preco, urlConcat)
    if i == qtdeLinks - 1:
        exportaExcel(dictFinal)

