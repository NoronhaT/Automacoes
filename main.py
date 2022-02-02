import investpy
import pandas as pd
from datetime import datetime
import numpy as np
from currency_converter import CurrencyConverter
from datetime import date

c = CurrencyConverter(decimal=True)

# DATA ATUAL - SERÁ REGISTRADA A CONSULTADO:

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
dia = date.today()
print(dia)
print("HORA DE INÍCIO =", current_time)

# DADOS DO USUÁRIO

cr_nome_um = 'Bitcoin'
cr_nome_dois = 'Ethereum'
qt_nome_um = 0.00023971
qt_nome_dois = 0.00845140
st_nome_um = 'COINBASE'
st_nome_dois = 'COINBASE'
pr_nome_um = 203108.69
pr_nome_dois = 14523.42
dat_nome_um = (2022 / 1 / 28)
dat_nome_dois = (2022 / 1 / 28)

pr_nome_um_conv = c.convert(pr_nome_um, 'BRL', 'USD', date=date(year=2022, month=1, day=13))
pr_nome_um_float = float(pr_nome_um_conv)

pr_nome_dois_conv = c.convert(pr_nome_dois, 'BRL', 'USD')
pr_nome_dois_float = float(pr_nome_dois_conv)

my_wallet = {'name': [cr_nome_um, cr_nome_dois],
             'QUANT': [qt_nome_um, qt_nome_dois],
             'SITE': [st_nome_um, st_nome_dois],
             'PREÇO': [pr_nome_um_conv, pr_nome_dois]}

print(my_wallet)

try:
    df1 = pd.read_excel(r'dados.xlsx', engine='openpyxl')
    print('Arquivo com histórico carregado com sucesso!')

    acoes = investpy.get_cryptos_overview(as_json=False, n_results=500)
    dados = pd.DataFrame(acoes)

    resultados = pd.concat([dados, df1], sort=False)
    resultados.loc[resultados['DATA COTAÇÃO'].isnull(), 'DATA COTAÇÃO'] = now
    resultados.to_excel(r'dados.xlsx', index=False)

except:
    print("O arquivo de armazenamento não existe, criando um novo arquivo de nome - dados.xlsx")
    acoes = investpy.get_cryptos_overview(as_json=False, n_results=500)
    dados = pd.DataFrame(acoes)
    dados['DATA COTAÇÃO'] = now
    cotacoes = dados.to_excel(r'dados.xlsx', index=False)
    print("--------------------------------------------------------------------------")
    print("ARQUIVO GERADO COM SUCESSO!")
    print("--------------------------------------------------------------------------")

new_df = pd.read_excel(r'dados.xlsx', engine='openpyxl')
cripto_chart = new_df[['name', 'price', 'DATA COTAÇÃO']]

# ENTRADA CRYPTO_UM

filtro = cripto_chart['name'] == 'Bitcoin'
filter_cripto = cripto_chart[filtro]
crypto_um_shape = filter_cripto.shape
crypto_um = filter_cripto.head
crypto_um_average = np.mean(filter_cripto['price'])
av_um = (((pr_nome_um_float / crypto_um_average) - 1) * -1) * 100
av_um_format = round(av_um, 2)
str_av_um = str(av_um_format)

print('O valor atual da crypto em: ' + '\n' + str(dia) + '\n' + current_time)
print('U$ ' + str(round(float(crypto_um_average), 2)))
print('Seu valor na data da sua compra era: ' + 'U$ ' + str(round(pr_nome_um_float, 2)))
print('Seu resultado em: ' + cr_nome_um + ' é: ' + str_av_um + ' %')

valor = qt_nome_um * pr_nome_um_float
print('A quantidade que você possui desta cripto é: ' + str(qt_nome_um))
print('Total: U$ ' + str(round(valor,2)))
valor_brl = c.convert(valor,'USD','BRL')
print('Equivalente a R$: ' + str(round(valor_brl,2)))