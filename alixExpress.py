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

entrada = input("INSIRA A PÁGINA QUE VOCÊ GOSTARIA DE BUSCAR PELO PRODUTO:" +"\n" +
      "SENDO " + "\n" + "1 - ALIEXPRESS" +"\n" + "2 - MERCADO LIVRE" + "\n" +
      "3 - FECHAR" + "\n")

escolha = int(entrada)

print("Numero escolhido foi:" + str(escolha))

print("--------------------------------------------------------------------------")
if escolha ==1:
    item_buscado = input("Digite o nome do produto que você está buscando: ")
    print("--------------------------------------------------------------------------")
    print("Irei retornar todos os resultados da busca apresentadas pelas páginas sinalizadas," + "na opção:" + str(
        escolha) + " baseados no que você inseriu!")
    print("--------------------------------------------------------------------------")
elif escolha ==2:
    item_buscado = input("Digite o nome do produto que você está buscando: ")
    print("--------------------------------------------------------------------------")
    print("Irei retornar todos os resultados da busca apresentadas pelas páginas sinalizadas," + "na opção:" + str(
        escolha) + " baseados no que você inseriu!")
    print("--------------------------------------------------------------------------")
elif escolha ==3:
    item_buscado = input("Digite o nome do produto que você está buscando: ")
    print("--------------------------------------------------------------------------")
    print("Irei retornar todos os resultados da busca apresentadas pelas páginas sinalizadas," + "na opção:" + str(
        escolha) + " baseados no que você inseriu!")
    print("--------------------------------------------------------------------------")
else:
    entrada = input("Você precisa selecionar as opções a seguir:" + "\n" +
                    "SENDO " + "\n" + "1 - ALIEXPRESS" + "\n" + "2 - MERCADO LIVRE" + "\n" +
                    "3 - FECHAR" + "\n")
escolha = int(entrada)

print("--------------------------------------------------------------------------")



url_ali = "https://pt.aliexpress.com/"
url_mli = "https://www.mercadolivre.com.br/"


if escolha ==1:
    print("----------------------------------------------------------------------------------")
    print("VOCÊ SINALIZOU ACESSO AO ALIEXPRESS")
    option = Options()
    option.headless = False

    driver = webdriver.Firefox(options=option)
    driver.get(url_ali)

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
    print("RESULTADOS PARA SUA BUSCA NO ALIEXPRESS SÃO: ")
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

elif escolha == 2:
    print("----------------------------------------------------------------------------------")
    print("VOCÊ SINALIZOU ACESSO AO MERCADO LIVRE")
    option = Options()
    option.headless = False

    driver = webdriver.Firefox(options=option)
    driver.get(url_mli)

    janela = driver.find_element(By.XPATH, '//*[@id="cb1-edit"]')
    acesso_janela = janela.send_keys(item_buscado)

    botao_de_busca = driver.find_element(By.XPATH, '/html/body/header/div/form/button')
    clica_botao = botao_de_busca.click()

    print("--------------------------------------------------------------------------")
    print("AGUARDE ENQUANTO TE MOSTRO OS RESULTADOS")
    print("--------------------------------------------------------------------------")

    time.sleep(10)

    xpath_mae = driver.find_element(By.XPATH, '/html/body/main/div/div/section/ol')
    html_content = xpath_mae.get_attribute('outerHTML')

    b_soup = soup(html_content, 'html.parser')


    lista_produtos = b_soup.find_all('div', class_='andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default')

    print("--------------------------------------------------------------------------")
    print("RESULTADOS PARA SUA BUSCA NO MERCADO LIVRE SÃO: ")
    print("--------------------------------------------------------------------------")

    for i in lista_produtos:
        print("--------------------------------------------------------------------------")
        produtos = i.select('h2', class_='ui-search-item__title')
        print(produtos[0].get_text())
        produtos = i.select('span', class_='price-tag-fraction')
        print(produtos[1].get_text())
        produtos = i.select('p', class_='ui-search-item__shipping ui-search-item__shipping--free')
        print(produtos[0].get_text())
        print("--------------------------------------------------------------------------")

    input("Digite sair para fechar: ")
elif escolha == 3:
    print("--------------------------------------------------------------------------")
    print("Você escolheu sair do programa!")
    print("--------------------------------------------------------------------------")
    print("NORONHA TECHNOLOGIES")
    print("BYE!")
    quit()

else:
    print("INSIRA A PÁGINA QUE VOCÊ GOSTARIA DE BUSCAR PELO PRODUTO:" + "\n" +
    "SENDO " + "\n" + "1 - ALIEXPRESS" + "\n" + "2 - MERCADO LIVRE" + "\n" +
    "3 - FECHAR" + "\n")












# VIDEO REFERENCIA https://www.youtube.com/watch?v=H-XpwSz4x8Y
