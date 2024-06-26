﻿# Projeto FastAPI com PostgreSQL/PostGIS

Este é um projeto de exemplo utilizando FastAPI, PostgreSQL com extensão PostGIS. O projeto inclui uma configuração completa para desenvolver, testar e executar uma aplicação FastAPI com um banco de dados PostgreSQL espacial.

Estrutura do Projeto
A estrutura de diretórios do projeto segue uma abordagem modular e organizada:

Projeto FastAPI com PostgreSQL/PostGIS
Este é um projeto de exemplo utilizando FastAPI, PostgreSQL com extensão PostGIS. O projeto inclui uma configuração completa para desenvolver, testar e executar uma aplicação FastAPI com um banco de dados PostgreSQL espacial.

Estrutura do Projeto
A estrutura de diretórios do projeto segue uma abordagem modular e organizada:
```
├── app/
│   ├── core/
│   │   ├── auth_bearer.py
│   │   ├── auth_handler.py
│   │   ├── config.py
│   ├── db/
│   │   ├── database.py
│   ├── models/
│   │   ├── graph.py
│   ├── routers/
│   │   ├── graph.py
│   ├── schemas/
│   │   ├── graph.py
│   ├── tests/
│   │   ├── test_graph.py
│   ├── main.py
│   └── init_db.sh
├── .env
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

```

Pré-requisitos
Python 3.11
PostgreSQL 15.0+
PostGIS 3.3+
Configuração
Clonar o Repositório
Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/marcosmadeira34/spotsatchallenge.git
cd app
```

Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

```bash
USER=postgres
PASSWORD=postgres
HOST=localhost
PORT=5432
```

Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

# Configuração do Banco de Dados
Instalar PostgreSQL e PostGIS
Siga as instruções de instalação no site oficial do PostgreSQL e site do PostGIS.

Criar Banco de Dados e Extensão PostGIS
Execute os seguintes comandos no PostgreSQL para criar o banco de dados e habilitar a extensão PostGIS:

```
CREATE DATABASE yourdatabase;
\c yourdatabase
CREATE EXTENSION postgis;
````

Configuração do Banco de Dados no Projeto
Certifique-se de que as configurações do banco de dados em app/db/database.py estão corretas:

```
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

```

# Rodando o Projeto
Para iniciar o servidor FastAPI, execute:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000

```
A aplicação estará disponível em http://localhost:8000.

Testes
Rodar Testes com Pytest
Para executar os testes, certifique-se de que você está no ambiente virtual e execute:

``` bash
pytest
```

Estrutura de Pastas
app/core: Contém a lógica de autenticação e configuração.
app/db: Contém a configuração do banco de dados.
app/models: Contém os modelos SQLAlchemy.
app/routers: Contém as rotas da aplicação.
app/schemas: Contém os schemas Pydantic.
app/tests: Contém os testes Pytest.
app/main.py: Ponto de entrada da aplicação.

# Conclusão

Este projeto demonstra a integração de FastAPI com PostgreSQL e PostGIS, configuração de autenticação JWT, testes unitários com Pytest e boas práticas de estruturação de código. Sinta-se à vontade para contribuir ou abrir issues no repositório!

Para mais informações e documentação, consulte:

FastAPI Documentation
PostgreSQL Documentation
PostGIS Documentation
Licença
Este projeto é licenciado sob os termos da licença MIT. Para mais informações, consulte o arquivo LICENSE.

# Observações

Este projeto pode ser rodado em um container Docker. Para isso, basta executar o comando docker-compose up na raiz do projeto. Nele existe um arquivo docker-compose.yml que contém a configuração básica para rodar o projeto em um container Docker, porém não foi testado por falta de recursos computacionais no momento..

