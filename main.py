import time
import investpy
import numpy as np
import pandas as pd
from datetime import datetime
from currency_converter import CurrencyConverter
from datetime import date
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from keys import *
import pywhatkit
import os


# KEYS PARA ACESSO NA API
client = Client(api_key, api_secret)
# client.API_URL = 'https://testnet.binance.vision/api' CANAL DE TESTES, TEM QUE ATIVAR CAMPO DE CHAVES 1

info_one = client.get_account()
run = True

while True:

    # DATA ATUAL - SERÁ REGISTRADA A CONSULTA

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    dia = date.today()
    print("**************************************************")
    print(dia)
    print("**************************************************")
    print("HORA DE INÍCIO =", current_time)
    print("**************************************************")

    # --------------------------------------VERIFICAÇÃO-DOS-HISTORICOS- HISTORICO E CARTEIRA----------------------------------------------------
    try:
        print("VERIFICANDO EXISTENCIA DE ARQUIVO COM HISTÓRICO DE COTAÇÕES: ")
        df1 = pd.read_excel(r'dados.xlsx', engine='openpyxl')
        print('Arquivo com histórico carregado com sucesso!')
        print("**************************************************")

        acoes = investpy.get_cryptos_overview(as_json=False, n_results=500)
        dados = pd.DataFrame(acoes)

        resultados = pd.concat([dados, df1], sort=False)
        resultados.loc[resultados['DATA COTAÇÃO'].isnull(), 'DATA COTAÇÃO'] = now
        resultados.to_excel(r'dados.xlsx', index=False)

    except:
        print("O arquivo de armazenamento não existe, criando um novo arquivo de nome - dados.xlsx")
        print("**************************************************")
        acoes = investpy.get_cryptos_overview(as_json=False, n_results=500)
        dados = pd.DataFrame(acoes)
        dados['DATA COTAÇÃO'] = now
        cotacoes = dados.to_excel(r'dados.xlsx', index=False)
        print("**************************************************")
        print("ARQUIVO GERADO COM SUCESSO!")

        new_df = pd.read_excel(r'dados.xlsx', engine='openpyxl')
        cripto_chart = new_df[['name', 'price', 'DATA COTAÇÃO']]

    try:
        print("VERIFICANDO EXISTENCIA DE ARQUIVO COM A SUA CARTEIRA: ")
        carteira = pd.read_excel(r'carteira.xlsx', engine='openpyxl')
        print('Carteira carregada com sucesso!')
        print("**************************************************")
        carteira_df = pd.DataFrame(carteira)

    except:
        print("O arquivo de carteira não existe, criando um novo arquivo de nome - carteira.xlsx")
        print("**************************************************")
        client = Client(api_key, api_secret)
        info_one = client.get_account()
        info_one_list = list(info_one.items())
        extract = info_one_list[9]
        extract_one = extract[1]
        rmv_brl = filter(lambda asset: asset['asset'] != 'BRL', extract_one)

        cripto_df = pd.DataFrame(rmv_brl)
        cripto_df['free'] = pd.to_numeric(cripto_df['free'], downcast="float")
        cripto_df['locked'] = pd.to_numeric(cripto_df['locked'], downcast="float")
        keep_action = cripto_df[(cripto_df['locked'] > 0)]
        keep_action_two = cripto_df[(cripto_df['free'] > 0)]
        keep_count = keep_action_two['asset'].value_counts()
        excel_cript = keep_action_two.to_excel('carteira.xlsx', index=False)
        carteira_xls = pd.read_excel(r'carteira.xlsx')
        new_df = pd.DataFrame(carteira_xls)
        new_df['PREÇO DE COMPRA'] = ""
        new_df['DATA DE COMPRA'] = ""
        new_df['maxima'] = ""
        new_df['minima'] = ""
        new_df['DATA DE VENDA'] = ""
        new_df['VALOR DE VENDA'] = ""
        new_df['VALOR EM U$ - CARTEIRA'] = ""
        new_df['maxima'] = new_df['maxima'].fillna(0)
        new_df['minima'] = new_df['minima'].fillna(0)
        new_df['DATA DE VENDA'] = new_df['DATA DE VENDA'].fillna(0)
        new_df['VALOR DE VENDA'] = new_df['VALOR DE VENDA'].fillna(0)
        new_df['PREÇO DE COMPRA'] = new_df['PREÇO DE COMPRA'].fillna(0)
        new_df['DATA DE COMPRA'] = new_df['DATA DE COMPRA'].fillna(0)
        new_df['VALOR EM U$ - CARTEIRA'] = new_df['VALOR EM U$ - CARTEIRA'].fillna(0)

        # CONFIGURAÇÃO DE PARAMETROS DE CADA CRIPTO EM CARTEIRA:
        contador = 0
        for index_label, row_series in new_df.iterrows():
            print("ADICIONE AS INFORMAÇÕES DE PREÇO E DATA DE COMPRA PARA CADA CRIPTO EM SUA CARTEIRA!")
            print("************************************************************************************")
            print("A LISTA DO QUE FOI ENCONTRADO EM SUA CARTEIRA IRÁ APARECER ABAIXO!")
            print(new_df.head())
            print("************************************************************************************")
            new_df.at[index_label, 'PREÇO DE COMPRA'] = input(
                "INSIRA O VALOR PAGO NO FORMATO (000.00) PARA A CRIPTO NA POSIÇÃO " + str(contador) + ": ")
            print("************************************************************************************")
            new_df.at[index_label, 'DATA DE COMPRA'] = input(
                "INSIRA A DATA DA COMPRA NO FORMATO DD-MM-AAAA DA CRIPTO  NA POSIÇÃO " + str(contador) + ": ")
            print("************************************************************************************")
            print("CONFIRA OS DADOS INSERIDOS!")
            print("************************************************************************************")
            new_df.at[index_label, 'maxima'] = input(
                "INSIRA A CONDIÇÃO DE % PARA ATIVAR VENDA - SUPERSELL (0 a 100),PARA MOEDA NA POSIÇÃO: " + str(
                    contador) + ": ")
            print("************************************************************************************")
            print("CONFIRA OS DADOS INSERIDOS!")
            new_df.at[index_label, 'minima'] = input(
                "INSIRA A CONDIÇÃO DE % PARA ATIVAR VENDA - SELL (-1 a -100),PARA MOEDA NA POSIÇÃO: " + str(
                    contador) + ": ")
            print("************************************************************************************")
            print("CONFIRA OS DADOS INSERIDOS!")
            print(new_df.head())

            print("************************************************************************************")
            print("DADOS DE CARTEIRA SALVOS!VOCÊ PODE CONFERIR O QUE FOI INSERIDO NO ARQUIVO: carteiraCompleta.xlsx")
            contador = contador + 1
            new_df.to_excel('carteiraCompleta.xlsx', index=False)

    asset_excel = pd.read_excel('carteiraCompleta.xlsx')
    asset_df = pd.DataFrame(asset_excel)
    asset_df['VALOR EM U$ - CARTEIRA'] = asset_df['PREÇO DE COMPRA'] * asset_df['free'] + asset_df['locked']

    # RESUMO DOS DADOS ENCONTRADOS E INPUTADOS PELO USUARIO

    contador_dois = 0
    for asset in asset_df['asset']:
        y_wallet = asset
        balance = client.get_asset_balance(asset=y_wallet)  # the asset must be linked to a variable
        cripto_one = list(balance.items())

        # DICT TO LIST (cripto name)
        cripto_one_name = cripto_one[0]
        cripto_one_qt = cripto_one[1]
        cripto_one_r = cripto_one[2]

        # LIST TO TUPLE (cripto name)
        cripto_one_value = cripto_one_name[1]
        cripto_one_q = cripto_one_qt[1]
        cripto_one_rt = cripto_one_r[1]

        cripto_wallet = float(cripto_one_q) + float(cripto_one_rt)
        print("----------------------------------------------------------------")
        print("Estes são os fundos encontrados parâmetros definidos para sua carteira digital: ")
        print("Criptomoeda em carteira: " + cripto_one_value)
        print("Quantidade em carteira: " + cripto_one_q)
        print("Quantidade em reserva: " + cripto_one_rt)
        print("Total de " + cripto_one_value + ": " + str(cripto_wallet))
        print("U$ em carteira: " + str(asset_df['VALOR EM U$ - CARTEIRA'][contador_dois]))
        print("SUPERSELL: " + str(asset_df['maxima'][contador_dois]))
        print("SELL: " + str(asset_df['minima'][contador_dois]))
        contador_dois = contador_dois + 1

    asset_df.to_excel('carteiraCompleta.xlsx', index=False)

    # ALTERA O NOME DA COLUNA ASSET PARA SYMBOL, PARA PODER EXECUTAR A MESCLA DE DOIS DF E ADICIONA O TERMO CONDIÇÕES
    # PALAVRAS GATILHOS: SELL, SUPERSELL, KEEP

    dados_ex = pd.read_excel('dados.xlsx', engine='openpyxl')
    dados_df = pd.DataFrame(dados_ex)
    dados_df.rename({'symbol': 'asset'}, axis='columns', inplace=True)
    asset_ex = pd.read_excel('carteiraCompleta.xlsx', engine='openpyxl')
    asset_df = pd.DataFrame(asset_ex)
    df_new = pd.merge(dados_df, asset_df, on=['asset'], how='left')
    df_new['Condições'] = (df_new['price'] / df_new['PREÇO DE COMPRA'] - 1) * 100

    # APLICACAO DAS STRINGS DE AÇÃO NA COLUNA CONDIÇÕES:

    df_new['AÇÃO'] = ""
    df_new.loc[df_new['Condições'] < df_new['maxima'], 'AÇÃO'] = 'KEEP'
    df_new.loc[df_new['Condições'] > df_new['minima'], 'AÇÃO'] = 'KEEP'
    df_new.loc[df_new['Condições'] > df_new['maxima'], 'AÇÃO'] = 'SUPERSELL'
    df_new.loc[df_new['Condições'] < df_new['minima'], 'AÇÃO'] = 'SELL'
    df_new = df_new.fillna(0)

    # CONCATENACAO DE DF PARA CRIAR HISTÓRICO E AGRUPAMENTO DAS AÇÕES:

    tendencias_data = []
    tend_df = pd.DataFrame(tendencias_data)

    for asset in asset_df['asset']:
        y_wallet = asset
        keep_action = df_new[(df_new['asset'] == y_wallet) & (df_new["AÇÃO"] == 'KEEP')]
        keep_count = keep_action['AÇÃO'].value_counts()
        tend_df = pd.concat([tend_df, keep_action])

    for asset in asset_df['asset']:
        y_wallet = asset
        keep_action = df_new[(df_new['asset'] == y_wallet) & (df_new["AÇÃO"] == 'SELL')]
        keep_count = keep_action['AÇÃO'].value_counts()

        tend_df = pd.concat([tend_df, keep_action])

    for asset in asset_df['asset']:
        y_wallet = asset
        keep_action = df_new[(df_new['asset'] == y_wallet) & (df_new["AÇÃO"] == 'SUPERSELL')]
        keep_count = keep_action['AÇÃO'].value_counts()
        tend_df = pd.concat([tend_df, keep_action])

    # REMOÇÃO DE COLUNAS NÃO UTILIZADAS PARA O NOVO DF

    del tend_df['status']
    del tend_df['market_cap']
    del tend_df['volume24h']
    del tend_df['change24h']
    del tend_df['change7d']

    # ORGANIZAÇÃO DOS STATUS POR DATA DE OCORRÊNCIA DECRESCENTE DAS CRIPTOS POSSUIDAS

    tend_df.sort_values(by='DATA COTAÇÃO', ascending=False, inplace=True)

    # CRIACAO DO DF CALCULADOR, PAGINA FOCADA EM DAR UM RESUMO SIMPLIFICADO AO USUARIO
    len_wallet = len(asset_ex['asset'])

    calculador = pd.DataFrame(
        columns=['name', 'sell', 'keep', 's.sell', 'amostras', 'ação', 'preço compra', 'valor atual', 'ganho atual',
                 'carteira', 'maxima', 'minima'], index=[int(len_wallet)])

    # AQUI SÃO CRIADOS OS GATILHOS DO DATAFRAME DE AÇÕES

    contador = 0
    for asset in asset_df['asset']:
        sell_force = tend_df[(tend_df['asset'] == asset) & (tend_df["AÇÃO"] == 'SELL')]
        sell_numb = (sell_force['AÇÃO'].values == 'SELL').sum()

        keep_force = tend_df[(tend_df['asset'] == asset) & (tend_df["AÇÃO"] == 'KEEP')]
        keep_numb = (keep_force['AÇÃO'].values == 'KEEP').sum()

        ssell_force = tend_df[(tend_df['asset'] == asset) & (tend_df["AÇÃO"] == 'SUPERSELL')]
        ssell_numb = (ssell_force['AÇÃO'].values == 'SUPERSELL').sum()

        valor_acao_f = asset_df[(asset_df['asset'] == asset)]

        valor_acao = (valor_acao_f['PREÇO DE COMPRA'])
        valor_acao_l = list(valor_acao)
        valor_acao_v = valor_acao_l[0]
        valor_acao_str = str(valor_acao_v).replace('[', '').replace(']', '')
        valor_acao_fl = float(valor_acao_str)

        dados_ex = pd.read_excel('dados.xlsx', engine='openpyxl'
                                 )
        dados_df = pd.DataFrame(dados_ex)
        dados_df.sort_values(by='DATA COTAÇÃO', ascending=False, inplace=True)
        data_acao = dados_df[(dados_df['symbol'] == asset)]
        valor_df = data_acao.iloc[:1]
        price_tag = valor_df['price']
        price_tag_l = list(price_tag)
        price_tag_v = price_tag_l[0]
        price_tag_str = str(price_tag_v).replace('[', '').replace(']', '')
        price_tag_fl = float(price_tag_str)

        qt_acao = asset_df[(asset_df['asset'] == asset)]
        free_qt = (qt_acao['free'])
        free_qt_l = list(free_qt)
        free_qt_v = free_qt_l[0]
        free_qt_str = str(free_qt_v).replace('[', '').replace(']', '')
        free_qt_fl = float(free_qt_str)

        qt_acao_dois = asset_df[(asset_df['asset'] == asset)]
        locked_qt = (qt_acao_dois['locked'])
        locked_qt_l = list(locked_qt)
        locked_qt_v = locked_qt_l[0]
        locked_qt_str = str(locked_qt_v).replace('[', '').replace(']', '')
        locked_qt_fl = float(locked_qt_str)

        status = tend_df[(tend_df['asset'] == asset)]
        status_qt = (status['AÇÃO'])
        status_qt_l = list(status_qt)
        status_qt_v = status_qt_l[0]

        # preenchimento do df contador com os dados pegos no for loop

        calculador.loc[contador] = {'name': asset, 'sell': sell_numb, 'keep': keep_numb, 's.sell': ssell_numb,
                                    'amostras': sell_numb + keep_numb + ssell_numb, 'ação': status_qt_v,
                                    'preço compra': valor_acao_fl, 'valor atual': price_tag_fl,
                                    'ganho atual': ((price_tag_fl / valor_acao_fl) - 1) * 100,
                                    'carteira': (free_qt_fl + locked_qt_fl) * price_tag_fl,
                                    'maxima': asset_ex['maxima'][contador], 'minima': asset_ex['minima'][contador]}

        contador = contador + 1

    # SALDO DA CARTEIRA BRL
    client = Client(api_key, api_secret)
    info_one = client.get_account()
    info_one_list = list(info_one.items())
    extract = info_one_list[9]
    extract_one = extract[1]
    rmv_brl = filter(lambda asset: asset['asset'] == 'BRL', extract_one)
    brl_df = pd.DataFrame(rmv_brl)


    # DENTRO DESTE FOR LOOP SERÃO ATIVADOS OS AVISOS VIA WHATS E AQUI TAMBÉM PODEM SER COLOCADOS
    # GATILHOS DE VENDA!

    # UM CALCULADOR TO EXCEL PODE SER CRIADO AQUI CASO NECESSÁRIO


    calculador.dropna(subset=['name'], inplace=True)
    resultados_xlsx = calculador.to_excel('resultados.xlsx',index=0)

    try:
        vendas_xlsx = pd.read_excel('vendas.xlsx',engine='openpyxl')
        print("CARTEIRA COM ATIVOS PARA VENDAS GERADOS COM SUCESSO!")
    except:
        print("Carteira de vendas não encontrada!" + "\n" +
              "Deseja adicionar com base nas moedas existentes em sua carteira?"
              + "\n" + "1- SIM ou 2- NÃO")

        while True:
            rep = input("INSIRA SUA RESPOSTA: ")
            if rep == "1":
                print("GERANDO UM ARQUIVO COM BASE NAS MOEDAS ATIVAS")
                venda_pd = pd.DataFrame(resultados_xlsx)
                venda_pd.to_excel("vendas.xlsx",index=0)

                print("ARQUIVO GERADO COM SUCESSO!!!")
                break

            elif rep == "2":
                print("A GERAÇÃO DO ARQUIVO SERÁ IGNORADA")
                break
            else:
                print("OS VALORES INSERIDOS NÃO CONFEREM! TENTE NOVAMENTE POR FAVOR.")



    contador_tres = 0
    for nome in calculador['name']:
        now = datetime.now()
        sell_force = calculador[(calculador['name'] == nome) & (calculador["ação"] == 'SELL')]
        valor_down = sell_force['ganho atual']
        valor_down_l = list(valor_down)
        valor_down_str = str(valor_down_l).replace('[', '').replace(']', '')
        if valor_down_str == "":
            valor_down_str = str(0)

        c_max = calculador['maxima'][contador_tres]
        c_max_str = str(c_max)
        c_max_f = float(c_max)
        c_min = calculador['minima'][contador_tres]
        c_min_str = str(c_min)
        c_min_f = float(c_min)
        contador_tres = contador_tres + 1

        texto_sell = "Cripto: " + str(nome) + "\n" \
                     + "Tol. Maxima: " + str(c_max_str) + "\n" + "Tol. Minima: " + str(
            c_min_str) + "\n" + "Apresenta queda de: " + str(valor_down_str) + "\n" + "RECOMENDACAO: SELL"

        current_time_one = now.strftime("%H")
        current_time_two = now.strftime("%M")
        current_time_three = now.strftime("%S")
        time_one = int(current_time_one)
        time_two = int(current_time_two) + 2
        time_three = int(current_time_three)

        if time_two >= 58:
            now = datetime.now()
            current_time_one = now.strftime("%H")
            current_time_two = now.strftime("%M")
            time_one = time_one + 1
            time_two = 0
            if float(valor_down_str) < float(c_min_f):
                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_sell, time_one, time_two, 15,
                                               tab_close=True,
                                               close_time=5)

        else:
            now = datetime.now()
            current_time_one = now.strftime("%H")
            current_time_two = now.strftime("%M")
            time_one = int(current_time_one)
            time_two = int(current_time_two) + 2
            if float(valor_down_str) < float(c_min_f):
                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_sell, time_one, time_two, 15,

                                               tab_close=True, close_time=5)
    contador_tres = 0
    for nome in calculador['name']:
        now = datetime.now()
        ssell_force = calculador[(calculador['name'] == nome) & (calculador["ação"] == 'SUPERSELL')]
        valor_down = ssell_force['ganho atual']
        valor_down_l = list(valor_down)
        valor_down_str = str(valor_down_l).replace('[', '').replace(']', '')
        if valor_down_str == "":
            valor_down_str = str(0)

        c_max = calculador['maxima'][contador_tres]
        c_max_str = str(c_max)
        c_max_f = float(c_max)
        c_min = calculador['minima'][contador_tres]
        c_min_str = str(c_min)
        c_min_f = float(c_min)

        price_now = calculador['valor atual'][contador_tres]
        price_now_f = float(price_now)
        price_now_str = str(price_now)

        wallet = calculador['carteira'][contador_tres]
        wallet_f = float(wallet)
        wallet_str = str(wallet)
        contador_tres = contador_tres + 1

        texto_ssell = "Cripto: " + str(nome) + "\n" \
                      + "Tol. Maxima: " + str(c_max_str) + "\n" + "Tol. Minima: " + str(
            c_min_str) + "\n" + "Apresenta lucro de: " + str(valor_down_str) + "\n" + "RECOMENDACAO: SUPERSELL"

        texto_ssell_action = "Executando a ordem de venda da cripto: " + str(nome) + "\n" + "Quantidade: " + str(
            wallet) + "\n" + "Pelo valor de: " + str(price_now_str)

        texto_ssell_notice = "A ordem de venda de: " + str(nome) + "\n" + "Quantidade: " + str(
            wallet) + "\n" + "Pelo valor de: " + str(price_now_str) + "\n" + "FOI CONCLUIDA COM SUCESSO!"

        current_time_one = now.strftime("%H")
        current_time_two = now.strftime("%M")
        current_time_three = now.strftime("%S")
        time_one = int(current_time_one)
        time_two = int(current_time_two) + 2
        time_three = int(current_time_three)

        if time_two >= 58:
            now = datetime.now()
            current_time_one = now.strftime("%H")
            current_time_two = now.strftime("%M")
            time_one = time_one + 1
            time_two = 0
            if float(valor_down_str) > float(c_max_f):
                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_ssell, time_one, time_two, 15,
                                               tab_close=True,
                                               close_time=5)
                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_ssell_action, time_one, time_two, 15,
                                               tab_close=True,
                                               close_time=5)

                ssell_order = client.create_test_order(symbol=nome,
                                                       side='SELL',
                                                       type='LIMIT',
                                                       timeInForce='GTC',
                                                       quantity=wallet_f,
                                                       price=price_now_f)

                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_ssell_notice, time_one, time_two, 15,
                                               tab_close=True,
                                               close_time=5)




        else:
            now = datetime.now()
            current_time_one = now.strftime("%H")
            current_time_two = now.strftime("%M")
            time_one = int(current_time_one)
            time_two = int(current_time_two) + 2
            if float(valor_down_str) > c_max_f:
                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_ssell, time_one, time_two, 15,
                                               tab_close=True,
                                               close_time=5)
    contador_tres = 0
    for nome in calculador['name']:
        now = datetime.now()
        keep_force = calculador[(calculador['name'] == nome) & (calculador["ação"] == 'KEEP')]
        valor_down = keep_force['ganho atual']
        valor_down_l = list(valor_down)
        valor_down_str = str(valor_down_l).replace('[', '').replace(']', '')
        if valor_down_str == "":
            valor_down_str = str(0)
        c_max = calculador['maxima'][contador_tres]
        c_max_str = str(c_max)
        c_max_f = float(c_max)
        c_min = calculador['minima'][contador_tres]
        c_min_str = str(c_min)
        c_min_f = float(c_min)
        contador_tres = contador_tres + 1

        texto_keep = "Cripto: " + str(nome) + "\n" \
                     + "Tol. Maxima: " + str(c_max_str) + "\n" + "Tol. Minima: " + str(
            c_min_str) + "\n" + "Esta apresentando valor: " + str(valor_down_str) + "\n" + "RECOMENDACAO: KEEP"

        current_time_one = now.strftime("%H")
        current_time_two = now.strftime("%M")
        current_time_three = now.strftime("%S")
        time_one = int(current_time_one)
        time_two = int(current_time_two) + 2
        time_three = int(current_time_three)

        if time_two >= 58:
            now = datetime.now()
            current_time_one = now.strftime("%H")
            current_time_two = now.strftime("%M")
            time_one = time_one + 1
            time_two = 0
            if float(valor_down_str) > float(c_min_f) and float(valor_down_str) < float(c_max_f) and float(
                    valor_down_str) != 0:
                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_keep, time_one, time_two, 15,
                                               tab_close=True,
                                               close_time=5)
        else:
            now = datetime.now()
            current_time_one = now.strftime("%H")
            current_time_two = now.strftime("%M")
            time_one = int(current_time_one)
            time_two = int(current_time_two) + 2
            if float(valor_down_str) > float(c_min_f) and float(valor_down_str) < float(c_max_f) and float(
                    valor_down_str) != 0:
                pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", texto_keep, time_one, time_two, 15,
                                               tab_close=True,
                                               close_time=5)

# CARTEIRA EM REAIS
    now = datetime.now()
    current_time_one = now.strftime("%H")
    current_time_two = now.strftime("%M")
    time_one = int(current_time_one)
    time_two = int(current_time_two) + 2
    saldo_brl = brl_df['free'][0]
    saldo_em_brl = (str(saldo_brl))
    carteira_brl = "SEU SALDO EM BRL É: " + str(saldo_em_brl)
    pywhatkit.sendwhatmsg_to_group("GgEuZUnvgwYInFLuYqtV4X", carteira_brl, time_one, time_two, 15,
                                   tab_close=True,
                                   close_time=5)


   






