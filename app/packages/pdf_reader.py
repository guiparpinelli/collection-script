import os
import re
from collections import namedtuple

import pandas as pd
import pdfplumber


def get_data(filedata):
    # return current working directory in which process is running
    path = os.getcwd()
    Client = namedtuple(
        'Client', 'cod uf duplicata rca cod_cobranca tipo_cobranca filial vl_titulo desconto vl_juros_prev vl_titulo_juros emissao venc atraso obs')
    # re for client line data
    new_client_re = re.compile(r"^Cliente : (\d{1,4}).*(\w{2})$")
    # re for data line
    data_re = re.compile(
        r"(^\d{4,6}\s\d{1}) (\d{1,2}) (\d{1,3}|D) (\w+ [DO| ]*\w+|\w+) (\d{1}) ([\d\.]+\,\d{2}) ([\d\.]+\,\d{2}) ([\d\.]+\,\d{2}) ([\d\.]+\,\d{2}) (\d{2}\/\d{2}\/\d{4}) (\d{2}\/\d{2}\/\d{4}) (\d{1,4})?(.*)")
    # trackers & data list
    total_clients = 0
    total_nfes = 0
    data = []

    with pdfplumber.open(filedata) as pdf:
        for page in pdf.pages:
            # extracting raw data
            p = page.extract_text()

            # for each page line
            for line in p.split('\n'):
                # looking for matches
                match_client = re.search(
                    new_client_re, line)
                match_data = re.search(data_re, line)
                if match_client:
                    cod = match_client.group(1)
                    uf = match_client.group(2)
                    total_clients += 1
                if match_data:
                    duplicata = match_data.group(1)
                    rca = match_data.group(2)
                    cod_cobranca = match_data.group(3)
                    tipo_cobranca = match_data.group(4)
                    filial = match_data.group(5)
                    vl_titulo = match_data.group(6)
                    desconto = match_data.group(7)
                    vl_juros_prev = match_data.group(8)
                    vl_titulo_juros = match_data.group(9)
                    emissao = match_data.group(10)
                    venc = match_data.group(11)
                    atraso = match_data.group(12)
                    obs = match_data.group(13)

                    # adding to data list
                    data.append(Client(cod, uf, duplicata, rca, cod_cobranca, tipo_cobranca, filial,
                                       vl_titulo, desconto, vl_juros_prev, vl_titulo_juros, emissao, venc, atraso, obs))
                    total_nfes += 1

    # formatting float numbers
    def format(x):
        return x.replace('.', '').replace(',', '.')

    df = pd.DataFrame(data)

    # formatting data
    df['emissao'] = pd.to_datetime(df['emissao'])
    df['venc'] = pd.to_datetime(df['venc'])
    df['vl_titulo'] = df['vl_titulo'].apply(format)
    df['desconto'] = df['desconto'].apply(format)
    df['vl_juros_prev'] = df['vl_juros_prev'].apply(format)
    df['vl_titulo_juros'] = df['vl_titulo_juros'].apply(format)

    # saving to csv file
    df.to_csv(path + '/output/data.csv', index=False)

    print('Success!')
    print(f'Data exported to {path}/output/data.csv')
