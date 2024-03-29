import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Connfiguração do serviço do ChromeDriver
servico = Service(ChromeDriverManager().install())

#Configurando opções personalizados
options = Options()
options.add_argument('window-size=1920,1080')

#Inicia o navegador
browser = webdriver.Chrome(service=servico, options=options)

#Faz a requisição no site da XP
browser.get(
    'https://www.xpi.com.br/investimentos/fundos-de-investimento/lista/#/'
)

# Cria um tempo de atraso de 10s para o site poder carregar o html
wait = WebDriverWait(browser, 10)

# Rola a página até encontrar o botão de ver mais para carregar a página e mostrar todos os fundos
button = wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            '//div[@class="position-detail-table-footer sly-container"]//div[@class="sly-row"]/div',
        )
    )
)
browser.execute_script(
    'arguments[0].scrollIntoView(true); arguments[0].click()', button
)

time.sleep(5)

# Acha o botão que abre as informações do fundo, fazendo uma iteração em cada um
details_buttons = browser.find_elements(By.CLASS_NAME, 'funds-table-row')

cnpjs = []
classificacoes_xp = []
classificacoes_cvm = []

for button in details_buttons:
    browser.execute_script('arguments[0].scrollIntoView(true);', button)
    browser.execute_script('arguments[0].click();', button)
    time.sleep(4.5)

    cnpj_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[text()="CNPJ"]/following-sibling::div')
        )
    )
    classificacao_xp_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//div[text()="Classificação XP"]/following-sibling::div',
            )
        )
    )
    classificacao_cvm_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//div[text()="Classificação CVM"]/following-sibling::div',
            )
        )
    )

    cnpjs.append(cnpj_element.text)
    print(len(cnpjs))
    classificacoes_xp.append(classificacao_xp_element.text)
    print(len(classificacoes_xp))
    classificacoes_cvm.append(classificacao_cvm_element.text)
    print(len(classificacoes_cvm))

# Aqui é basicamente a mesma repetição para cada varíavel, procurando todos os elementos dela
# Isso se repete para todas as variáveis de interesse abaixo.
nomes = [
    nome.text for nome in browser.find_elements(By.CLASS_NAME, 'fund-name')
][1:]
print(len(nomes))

aplicacoes_minimas = [
    aplicacao.text
    for aplicacao in browser.find_elements(
        By.CLASS_NAME, 'minimal-initial-investment'
    )
][1:]
#print(len(aplicacoes_minimas))

taxa_adms = [
    taxa.text
    for taxa in browser.find_elements(By.CLASS_NAME, 'administration-rate')
][1:]
#print(len(taxa_adms))

cotizacoes_resgate = [
    cotizacao.text
    for cotizacao in browser.find_elements(
        By.CLASS_NAME, 'redemption-quotation'
    )
][1:]
#print(len(cotizacoes_resgate))

liquidacoes_resgate = [
    liquidacao.text
    for liquidacao in browser.find_elements(
        By.CLASS_NAME, 'redemption-settlement'
    )
][1:]
#print(len(liquidacoes_resgate))

riscos = [risco.text for risco in browser.find_elements(By.CLASS_NAME, 'risk')][1:]
#print(len(riscos))

rentabilidades_mensal = []
rentabilidades_anual = []
rentabilidades_12m = []
rentabilidades_24m = []
rentabilidades_36m = []

elements = browser.find_elements(By.CLASS_NAME, 'profitability')[1:]

for element in elements:
    rentabilidades = element.text.split('\n')

    rentabilidades_mensal.append(rentabilidades[0])
    rentabilidades_anual.append(rentabilidades[1])
    rentabilidades_12m.append(rentabilidades[2])
    rentabilidades_24m.append(rentabilidades[3])
    rentabilidades_36m.append(rentabilidades[4])
# aqui está o dicionário de dados para receber todas essas informações

dados = {
    'nome': nomes,
    'aplicacao_mininma': aplicacoes_minimas,
    'taxa_administração': taxa_adms,
    'cotizacao_resgate': cotizacoes_resgate,
    'liquidacao_resgate': liquidacoes_resgate,
    'risco': riscos,
    'rentabilidade_mensal': rentabilidades_mensal,
    'rentabilidade_anual': rentabilidades_anual,
    'rentabilidade_12m': rentabilidades_12m,
    'rentabilidade_24m': rentabilidades_24m,
    'rentabilidade_36m': rentabilidades_36m,
    'cnpj': cnpjs,
    'classificacao_xp': classificacoes_xp,
    'classificacao_cvm': classificacoes_cvm
}

# E aqui, transformei o dicionário em um DataFrame do pandas e passei para o formato de Excel
df = pd.DataFrame(dados)
df.to_excel('resultado.xlsx', sheet_name='scrapping_result', index=False)

#Só deixei isso aqui pra poder manter o browser aberto e ir verificando se o código estava funcionando
#Disclaimer: confesso que é um pouco gambiarra, mas, o browser sem isso estava abrindo e fechando em segundos
time.sleep(5000)
