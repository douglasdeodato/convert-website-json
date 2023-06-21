import requests
import json
from bs4 import BeautifulSoup

# 1. Faça uma solicitação HTTP para obter o conteúdo HTML do site
response = requests.get('http://exemplo.com')

# 2. Analise o conteúdo HTML usando BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# 3. Extraia as informações relevantes e armazene em uma estrutura de dados
dados = {}
dados['titulo'] = soup.title.string
dados['paragrafos'] = [p.get_text() for p in soup.find_all('p')]

# 4. Salve a estrutura de dados em um arquivo JSON
with open('dados.json', 'w') as arquivo:
    json.dump(dados, arquivo)
