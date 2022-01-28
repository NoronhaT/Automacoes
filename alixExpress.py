from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from tkinter import *
import time

# JANELA
root = Tk()
root.geometry('500x500')
root.title('WebbyScrapper - NORONHA TECHNOLOGIES')
label_0 = Label(root, text="WEBBY", width=20, font=("bold", 20))
label_0.place(x=90, y=60)

var = IntVar()

label_1 = Label(root, text="ITEM A SER PROCURADO", width=20, font=("bold", 10))
label_1.place(x=50, y=200)
entry_1 = Entry(root)
entry_1.place(x=240, y=200)
entry_1.get()

Radiobutton(root, text="BUSCA NO ALIEXPRESS", padx=20, variable=var, value=1).place(x=220, y=250)
Radiobutton(root, text="BUSCA NO MERCADO LIVRE", padx=20, variable=var, value=2).place(x=220, y=290)
Radiobutton(root, text="SAIR DO PROGRAMA", padx=20, variable=var, value=3).place(x=220, y=330)

print("--------------------------------------------------------------------------")
print("NORONHA TECHNOLOGIES")
print("--------------------------------------------------------------------------")
print("ML E AE - WEBSCRAPPER rv.05")
print("--------------------------------------------------------------------------")

url_ali = "https://pt.aliexpress.com/"
url_mli = "https://www.mercadolivre.com.br/"


def checaVar():
    if var.get() == 1 and len(entry_1.get()) != 0:
        print("----------------------------------------------------------------------------------")
        print("VOCÊ SINALIZOU ACESSO AO ALIEXPRESS")
        option = Options()
        option.headless = False

        driver = webdriver.Firefox(options=option)
        driver.get(url_ali)

        janela = driver.find_element(By.XPATH, '//*[@id="search-key"]')
        janela.send_keys(entry_1.get())

        botao_de_busca = driver.find_element(By.XPATH, '//*[@id="form-searchbar"]/div[1]/input')
        botao_de_busca.click()

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
        quit()

    elif var.get() == 2:
        print("----------------------------------------------------------------------------------")
        print("VOCÊ SINALIZOU ACESSO AO MERCADO LIVRE")
        option = Options()
        option.headless = False

        driver = webdriver.Firefox(options=option)
        driver.get(url_mli)

        time.sleep(5)
        janela = driver.find_element(By.XPATH, '//*[@id="cb1-edit"]')
        janela.send_keys(entry_1.get())

        botao_de_busca = driver.find_element(By.XPATH, '/html/body/header/div/form/button')
        botao_de_busca.click()

        print("--------------------------------------------------------------------------")
        print("AGUARDE ENQUANTO TE MOSTRO OS RESULTADOS")
        print("--------------------------------------------------------------------------")

        time.sleep(10)

        xpath_mae = driver.find_element(By.XPATH, '/html/body/main/div/div/section/ol')
        html_content = xpath_mae.get_attribute('outerHTML')

        b_soup = soup(html_content, 'html.parser')

        lista_produtos = b_soup.find_all('div',
                                         class_='andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default')

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
            print("----------------------------------------------------------------------------------")
            print("VOCÊ SINALIZOU ACESSO AO MERCADO LIVRE")

        print(" FAZENDO PESQUISA ADICIONAL NO MERCADO LIVRE, AGUARDE...")

        print("--------------------------------------------------------------------------")
        print("AGUARDE ENQUANTO TE MOSTRO OS RESULTADOS ADICIONAIS")
        print("--------------------------------------------------------------------------")

        time.sleep(10)

        xpath_mae = driver.find_element(By.XPATH, '/html/body/main/div/div/section')
        html_content = xpath_mae.get_attribute('outerHTML')

        b_soup = soup(html_content, 'html.parser')

        lista_produtos = b_soup.find_all('ol',
                                         class_='ui-search-layout ui-search-layout--grid')

        print("--------------------------------------------------------------------------")
        print("RESULTADOS PARA SUA BUSCA ADICIONAL NO MERCADO LIVRE SÃO: ")
        print("--------------------------------------------------------------------------")

        for i in lista_produtos:
            print("--------------------------------------------------------------------------")
            produtos = i.select('h2', class_='ui-search-item__title ui-search-item__group__element')
            print(produtos[1].get_text())
            produtos = i.select('span', class_='price-tag-text-sr-only')
            print(produtos[1].get_text())
            produtos = i.select('p', class_='ui-search-item__shipping ui-search-item__shipping--free')
            print(produtos[1].get_text())

        input("Digite sair para fechar: ")
        quit()

    elif var.get() == 3:
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

botao_iniciar = Button(root, text='Iniciar', width=20, bg="black", fg='white', command=checaVar).place(x=180, y=380)
root.mainloop()


# VIDEO REFERENCIA https://www.youtube.com/watch?v=H-XpwSz4x8Y

