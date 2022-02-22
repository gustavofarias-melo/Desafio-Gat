# API Intelligence
API Intelligence busca informações, busca informações de acordo com os parâmetros. Desde e-mails, até endereços de carteiras de criptomoedas.

Nesta versão, está sendo utilizado. Está sendo importada a biblioteca, e sendo salva em um .txt.

Sendo por enquanto, uma realização de um GET. E também, está sendo realizado um breve CRUD (GET, POST, PUT, DELETE).

## Instalação
```bash
Python 3.6+
MongoDB para utilizar o pymongo
pip install -r requeriments.txt
```

## Como utilizar
````bash
MongoDB está configurado para funcionar em rede local (localhost)
# --reload utilizado para quando salvar após modificações (opcional)
# Execute para iniciar em 127.0.0.1:8000
uvicorn main:app --reload
# Acesse 127.0.0.1:8000/docs 
# Para utilizar as requesições, com o FastAPI, junto a UI Swagger
````

## Logs e Requisições
````commandline
Todas requisições estão sicronizadas com o banco de dados
* Logs estão sendo registrados no banco de dados e em logs.txt 
````