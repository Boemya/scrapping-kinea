import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

servico = Service(ChromeDriverManager().install())

options = Options()
options.add_argument('window-size=400,800')

browser = webdriver.Chrome(service=servico, options=options)


browser.get('https://www.xpi.com.br/investimentos/fundos-de-investimento/lista/#/')

time.sleep(5)

nome_tipo_fundo = browser.find_element(By.CLASS_NAME, 'onclick-fund') # tem o nome do fundo
print(nome_tipo_fundo)

aplicacao_minima = browser.find_element(By.CLASS_NAME, 'minimal-investment-column')
print(aplicacao_minima)

taxa_adiminstracao = browser.find_element(By.CLASS_NAME, 'max-administration-rate-column')
print(taxa_adiminstracao)

cotizacao_resgate = browser.find_element(By.CLASS_NAME, 'redemption-quotation')
print(cotizacao_resgate)

liquidacao_resgate = browser.find_element(By.CLASS_NAME, 'redemption-settlement')
print(liquidacao_resgate)

risco = browser.find_element(By.CLASS_NAME, 'xp-responsive-risk-column')
print(risco)

rentabilidade = browser.find_element(By.CLASS_NAME, 'profitability-column')
print(rentabilidade)

# classificacao_xp = browser.find_element(By.CLASS_NAME, '')
# classificacao_cvm = browser.find_element(By.CLASS_NAME, '')
# cnpj_fundo = browser.find_element(By.CLASS_NAME, '')

time.sleep(5000)

