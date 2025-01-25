import pandas as pd
import requests
import time

def main():
    # Diretórios
    file_path_og = 'excel/CNPJ_ORIGINAL.xlsx' # Arquivo original
    file_path_copy = 'excel/CNPJ_COPIA.xlsx' # Cópia do arquivo original que será modificada (medida de segurança)
    csv_copy = 'cnpj_data_hist.csv' # Uma cópia das respostas para csv, podendo ser utilizado posteriormente
    api_url = 'https://publica.cnpj.ws/cnpj/'

    # Dict com o nome das colunas no arquivo excel que serão modificadas (à direita)
    col_names = {
        "Situação Cadastral" : "SITUAÇÃO",
        "Cidade_e_Estado" : "CIDADE",
        "Socios" : "SOCIOS",
        "Telefone" : "TELEFONE",
        "Email" : "EMAIL"
    }

    # Range de linhas de cnpj que serão inclusas no algoritmo
    row_range = [None, None] # Todas
    #row_range = [0,5] # Apenas da linha 1 até a 5
    

    # Coletando cnpj's 
    cnpj = get_excel_array(file_path_og, 'CNPJ') # A coluna de cnpj's precisa ter exatamente esse nome de header 'CNPJ'

    # Limpando dados
    cnpj = clean_cnpj(cnpj) # Cnpj's com caracteres especiais comumente utilizados serão removidos aqui

    # Coleta dos dados através da API, utilizando url e chave (cnpj)
    response = make_requests(cnpj[row_range[0]:row_range[1]], api_url, csv_copy, 1)

    print(response)
    
    # Linha de processamento final, sobrescrevendo sobre o arquivo excel
    wstatus_1 = write_excel_array(response['Situacao'], file_path_copy, col_names['Situação Cadastral'])
    wstatus_2 = write_excel_array(response['Cidade'], file_path_copy, col_names['Cidade_e_Estado'])
    wstatus_3 = write_excel_array(response['Socios'], file_path_copy, col_names['Socios'])
    wstatus_4 = write_excel_array(response['Telefone'], file_path_copy, col_names['Telefone'])
    wstatus_5 = write_excel_array(response['Email'], file_path_copy, col_names['Email'])

    wstatus = [wstatus_1, wstatus_2, wstatus_3, wstatus_4, wstatus_5]

    for index, sts in enumerate(wstatus):
        if sts:
            print(f"Status {index+1}: Escrita com sucesso")
        else:
            print(f"Status {index+1}: Escrita malsucedida")

# Coleta certa coluna de um arquivo excel e retorna todos em uma lista do pandas
def get_excel_array(file_path:str, col_name:str) -> pd.Series:
    df_col = pd.read_excel(file_path, usecols=[col_name])
    
    return df_col[col_name]

# limpa caracteres especiais dos cnpj's
def clean_cnpj(cnpj_series:pd.Series) -> pd.Series:
    return (
        cnpj_series
        .fillna('')                            
        .astype(str)                           
        .str.strip()                           
        .str.replace(r'[^\d]', '', regex=True)
    )

def make_requests(array_keys:pd.Series, url_key:str, copy_url:str, print_out:int) -> pd.DataFrame:
    
    # dataframe onde todos os dados coletados serão armazenados, cada um em sua categoria
    response_df = pd.DataFrame(columns=['Situacao','Cidade','Socios','Telefone','Email'])

    for i in range(0, len(array_keys), 3):

        # Selecionando os 3 primeiros cnpj's como key
        batch_keys = array_keys[i:i+3]

        # Lista de resposta de cada leva (batch)
        batch_response = []

        for num, key in enumerate(batch_keys):
            url = url_key + key # https://publica.cnpj.ws/cnpj/
            response = requests.get(url, headers={})
            
            # Coletando resposta da API
            data = response.json()

            # Coletando dados ESPECÍFICOS recebidos pela API
            situacao_cadastral = data.get("estabelecimento", {}).get("situacao_cadastral", "Não encontrado")

            cidade = data.get("estabelecimento", {}).get("cidade", {}).get("nome", "Não encontrado")
            estado = data.get("estabelecimento", {}).get("estado", {}).get("nome", "Não encontrado")

            email = data.get("estabelecimento", {}).get("email", {})

            telefone = str(data.get("estabelecimento", {}).get("telefone1", "Não encontrado"))
            ddd = data.get("estabelecimento", {}).get("ddd1", "Não encontrado")
            if ddd:
                telefone = str(ddd) + '-' + str(telefone)

            socios = [socio.get("nome") for socio in data.get("socios", {})]
            socios_string = "; ".join(socios)

            cidade_estado = f'{cidade}, {estado}'

            # "Buffer" com todos dados coletados
            batch_response.append([situacao_cadastral, cidade_estado, socios_string, telefone, email])

            # Mensagem de status para cada coleta
            status_text = f'{i+num},{key},{situacao_cadastral},{cidade + ' ' + estado},{socios_string},{telefone},{email}'
            print(status_text)

            copy_to_csv(copy_url, status_text)

            time.sleep(1)

        print()
        # Aloca os dados coletados dentro do dataframe "response", cada um em seu respectivo lugar
        for j, batch in enumerate(batch_response):
            response_df.loc[(i+j),'Situacao'] = batch[0]
            response_df.loc[(i+j),'Cidade'] = batch[1]
            response_df.loc[(i+j),'Socios'] = batch[2]
            response_df.loc[(i+j),'Telefone'] = batch[3]
            response_df.loc[(i+j),'Email'] = batch[4]

        if len(array_keys) > i+3:
            print(f'Waiting 1 minute... batch {i}\n')
            time.sleep(60)
        
    return response_df

# Adiciona ao fim de um txt uma linha de dados (string)
def copy_to_csv(file_name:str, text:str) -> int:
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

# Escreve certa array de dados sobre uma coluna de um arquivo excel
def write_excel_array(array:pd.Series, file_path: str, col_name: str) -> bool:
    df = pd.read_excel(file_path, engine='openpyxl')

    if col_name not in df.columns:
        df[col_name] = None
        return False
    
    df[col_name] = df[col_name].astype(str)

    for i, cnpj in enumerate(array):
        if i < len(df):
            df.at[i, col_name] = str(cnpj)

    df.to_excel(file_path, index=False, engine='openpyxl')
    return True

# Impossibilita a execução do algoritmo sem ser de forma direta
if __name__ == "__main__":
    main()