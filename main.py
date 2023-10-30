import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

servico = Service(ChromeDriverManager().install())

options = Options()
options.add_argument('window-size=1920,1080')

browser = webdriver.Chrome(service=servico, options=options)


browser.get(
    'https://www.xpi.com.br/investimentos/fundos-de-investimento/lista/#/'
)

wait = WebDriverWait(browser, 10)

button = wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            '//div[@class="position-detail-table-footer sly-container"]//div[@class="sly-row"]/div',j
        )
    )
)
browser.execute_script(
    'arguments[0].scrollIntoView(true); arguments[0].click()', button
)

time.sleep(10)

nomes = [
    nome.text for nome in browser.find_elements(By.CLASS_NAME, 'fund-name')
]
print(len(nomes))

aplicacoes_minimas = [
    aplicacao.text
    for aplicacao in browser.find_elements(
        By.CLASS_NAME, 'minimal-initial-investment'
    )
]
print(len(aplicacoes_minimas))

taxa_adms = [
    taxa.text
    for taxa in browser.find_elements(By.CLASS_NAME, 'administration-rate')
]
print(len(taxa_adms))

cotizacoes_resgate = [
    cotizacao.text
    for cotizacao in browser.find_elements(
        By.CLASS_NAME, 'redemption-quotation'
    )
]
print(len(cotizacoes_resgate))

liquidacoes_resgate = [
    liquidacao.text
    for liquidacao in browser.find_elements(
        By.CLASS_NAME, 'redemption-settlement'
    )
]
print(len(liquidacoes_resgate))

riscos = [risco.text for risco in browser.find_elements(By.CLASS_NAME, 'risk')]
print(len(riscos))

rentabilidades = [
    rentabilidade.text
    for rentabilidade in browser.find_elements(By.CLASS_NAME, 'profitability')
]
print(len(rentabilidades))

# dados = {
#     'nome': nomes,
#     'aplicacao_mininma': aplicacoes_minimas,
#     'taxa_administração': taxa_adms,
#     'cotizacao_resgate': cotizacoes_resgate,
#     'liquidacao_resgate': liquidacoes_resgate,
#     'risco': riscos,
#     'rentabilidade': rentabilidades,
# }

# df = pd.DataFrame(dados)
# df.to_excel('teste.xlsx', index=False)
# # classificacao_xp = browser.find_element(By.CLASS_NAME, '')
# classificacao_cvm = browser.find_element(By.CLASS_NAME, '')
# cnpj_fundo = browser.find_element(By.CLASS_NAME, '')

time.sleep(5000)
