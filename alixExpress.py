import time
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


print("--------------------------------------------------------------------------")
print("NORONHA TECHNOLOGIES")
print("--------------------------------------------------------------------------")
print("ALIXEXPRESS - WEBSCRAPPER rv.00")
print("--------------------------------------------------------------------------")
item_buscado = input("Digite o nome do produto que você está buscando: ")
print("Irei retornar todos os resultados da busca apresentadas pela página do ALIEXPRESS, baseados no que você inseriu!")

url = "https://pt.aliexpress.com/"

option = Options()
option.headless = False

driver = webdriver.Firefox(options=option)
driver.get(url)

janela = driver.find_element(By.XPATH,'//*[@id="search-key"]')
acesso_janela = janela.send_keys(item_buscado)

botao_de_busca = driver.find_element(By.XPATH,'//*[@id="form-searchbar"]/div[1]/input')
clica_botao = botao_de_busca.click()

print("--------------------------------------------------------------------------")
print("AGUARDE ENQUANTO TE MOSTRO OS RESULTADOS")
print("--------------------------------------------------------------------------")

time.sleep(10)

xpath_mae = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]')
html_content = xpath_mae.get_attribute('outerHTML')

b_soup = soup(html_content, 'html.parser')

# print(b_soup.prettify())

# class="JIIxO" PRECISA CHECAR ISSO
# VIDEO REFERENCIA https://www.youtube.com/watch?v=H-XpwSz4x8Y

lista_produtos = b_soup.find_all('div', class_='_3GR-w')

print("--------------------------------------------------------------------------")
print("RESULTADOS PARA SUA BUSCA SÃO: ")
print("--------------------------------------------------------------------------")

for i in lista_produtos:

    print("--------------------------------------------------------------------------")
    produtos = i.select('h1', class_='_18_85')
    print(produtos[0].get_text())
    produtos = i.select('div', class_='mGXnE _37W_B')
    print(produtos[1].get_text())
    produtos = i.select('span', class_='_2jcMA')
    print(produtos[6].get_text())
    print("--------------------------------------------------------------------------")

input("Digite sair para fechar: ")


# exemplo: pyinstaller -c -F -i cm_icon.ico console_monopoly.py
#impede que a janela executável feche