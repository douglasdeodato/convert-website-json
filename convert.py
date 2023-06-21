import requests
import json
from bs4 import BeautifulSoup

# Carrega a URL do arquivo JSON
with open('config.json', 'r') as arquivo:
    dados_json = json.load(arquivo)

# Obtém a URL do JSON carregado
url = dados_json['site_url']

# Faz uma solicitação HTTP para obter o conteúdo HTML do site
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analisa o conteúdo HTML usando BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Cria um dicionário vazio para armazenar os dados
    dados = {}

    # Extrai o título do site
    dados['titulo'] = soup.title.string

    # Extrai os parágrafos do site
    dados['paragrafos'] = [p.get_text() for p in soup.find_all('p')]

    # Salva os dados em um arquivo JSON
    with open('dados.json', 'w') as arquivo_saida:
        json.dump(dados, arquivo_saida)

    print("Dados salvos em dados.json com sucesso!")
else:
    print("Ocorreu um erro ao fazer a solicitação HTTP. Código de status:", response.status_code)
