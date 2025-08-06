# API de Livros - FIAP Machine Learning Tech Challenge 1

Projeto de extração e API pública para consulta de livros, integrando web scraping e FastAPI.

| ![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688?logo=fastapi) ![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg) |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|

-----------------------------------

## Sumário

- [Descrição](#descrição)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura](#arquitetura)
- [Banco de Dados](#banco-de-dados)
- [Como Utilizar](#como-utilizar)
- [Endpoints](#endpoints)
- [Testes Unitários e Integração](#testes-unitários-e-integração)
- [Licença e Autores](#licença-e-autores)

-----------------------------------

## Descrição

O objetivo deste projeto é expor uma **API RESTful** para facilitar o acesso aos dados de diversos livros. Esses dados originalmente são extraídos via **web scraping** do site [Books to Scrape](https://books.toscrape.com/) 

A API fornece endpoints para:

- Cadastro e autenticação de usuários via JWT (Bearer Token).
- Consulta de informações de livros: listagem, busca por ID, busca por título/categoria, mais avaliados e por média de preços.
- Estatísticas gerais e por categoria.
- Trigger de scraping via endpoint para atualização dos dados.
- Health check da API.

Os dados disponíveis envolvem informações sobre:

- `Id`: Identificador do livro
- `Título`: Título do livro
- `Preço`: Preço do livro
- `Disponibilidade`: Status da disponibilidade do livro
- `Avaliação`: Avaliação do livro em estrelas
- `Categoria`: Categoria do livro
- `Imagem`: Link da imagem do livro


-----------------------------------

## Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI**
- **Uvicorn**
- **BeautifulSoup4**
- **SQLite**

-----------------------------------

## Arquitetura

O projeto segue uma arquitetura em camadas, inspirada no Clean Architecture,
separando responsabilidades em diferentes módulos e 
facilitando manutenção e testes.

### 📂 Estrutura do Repositório

```
fiap-machine-learning-tech-challenge-1/
├── api/                         # Aplicação FastAPI
│   ├── main.py                  # Entrypoint (uvicorn app.main:app)
│   ├── requirements.txt         # Dependências da API
│   └── app/                     # Código-fonte da API
│       ├── controllers/         # Implementação dos endpoints (routes)
│       ├── core/                # Configurações de autenticação e sessão de BD
│       ├── entities/            # Contém as entidades do banco (Modelos SQLAlchemy)
│       ├── schemas/             # Schemas Pydantic (request/response)
│       └── services/            # Lógica de negócio e componente de scraping
├──tests/
│   ├── conftest.py              # Configurações e fixtures compartilhadas
│   ├── test_auth.py             # Testes de autenticação (unitários)
│   ├── test_book_controller.py  # Testes dos endpoints da API (integração)
│   └── test_books_service.py    # Testes dos serviços de livros (misto)
├── pytest.ini                   # Configurações globais para rodar o Pytest
├── requirements.txt             # Dependências gerais do projeto
├── runtime.txt                  # Versão do runtime (deploy)
└── vercel.json                  # Configurações de deploy
```

### Descrição das camadas:

**Controllers**: Define os pontos de entrada da API (endpoints) e realiza roteamento.

**Services**: Implementa a lógica de negócio, orquestrando operações de scraping e acesso a dados via models.

**Entities**: Representa o domínio de dados, definindo entidades e mapeamentos com SQLAlchemy.

**Schemas**: Contém os Pydantic models para validação e serialização de requisições e respostas.

**Core**: Agrupa configurações centrais, como autenticação JWT, inicialização de sessão de banco de dados e configurações gerais.

Essa separação melhora a modularidade, e permite evoluir cada camada independentemente.

-----------------------------------

## Banco de Dados
A aplicação utiliza um banco de dados SQLite para armazenar os dados extraídos (também são armazenados em um csv). 
O banco é inicializado automaticamente ao iniciar a aplicação ou realizar o scrapping, criando as tabelas necessárias.

-----------------------------------

## Como Utilizar

Você pode usar a API de duas formas: **localmente** no seu ambiente de desenvolvimento ou 
utilizando a **versão já deployada**.

Para sua conveniência, o repositório já inclui um banco de dados SQlite (`data.db`) com cerca de mil livros e 
um usuário de testes, além de um arquivo (`books_data_20250729_232318.csv`). Permitindo que você explore a API imediatamente.


**Autenticação (válido para ambos os modos)**

Cadastre um usuário (ou utilize o de teste)

Usuário de teste:

    username: test_user  
    password: test12345

Não se esqueça de gerar e usar o token JWT antes de acessar os endpoints que requerem autenticação.

### 🏠 Execução Local

### Pré-requisitos

- Git
- Python 3.11+

### Passos

### 1. Clone o repositório
```bash
   git clone https://github.com/cris-scheib/fiap-machine-learning-tech-challenge-1.git
   cd fiap-machine-learning-tech-challenge-1
```
### 2. Crie e ative um ambiente virtual
```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
```
### 3. Instale dependências gerais
```bash
   pip install -r requirements.txt
```
### 4. Configurar variáveis de ambiente
 
Crie um arquivo **.env** na raiz do projeto com as seguintes variáveis:
```dotenv
SECRET_KEY=minha_super_chave_secreta_123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=1
```
   
###  5. Inicie a API
```bash
   cd api
   uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`. 

A documentação interativa é acessível em `http://127.0.0.1:8000/docs` (Swagger UI) 
e `http://127.0.0.1:8000/redoc` (ReDoc).

> **Atenção:** No Swagger selecione o servidor **Local**: http://127.0.0.1:8000 - Execução local.

### Opcional: Executar o Web Scraping

Utilize este processo apenas se desejar substituir os dados existentes por uma nova coleta, ou se você limpou o banco.

> **Atenção:** O processo é demorado (entre 30 minutos a 1 hora) para extrair todos os livros.
> Caso queira executar de forma mais rápida, apenas para ver o funcionamento, limite a quantidade de dados extraídos:
> - Entre na classe scrapper_service.py
> - Na linha 61, no retorno category_links[1:] 
> - Modifique o intervalo ex: category_links[1:2]

### Fluxo de trabalho para o scraping:

### 1. Certifique-se de que a API NÃO esteja em execução (pressione `Ctrl+C` no terminal onde a API está ativa).
### 2. Execute o script de scraping. No diretório raiz do projeto, execute:
```bash
   cd api
   # Certifique-se de estar no diretório 'api'
   python -m app.services.scrapper.scrapper_service
```
### 3. Pronto! Após a conclusão, inicie a API normalmente (passo 4 da execução local) para usar os novos dados.

### ☁️ Via Deploy (produção)

A nossa API está hospedada na Vercel que é uma plataforma de nuvem projetada 
para facilitar o desenvolvimento e a implantação de aplicações web

Acesse a versão em: https://fiap-machine-learning-tech-challeng.vercel.app/api/docs 

Lá você terá o Swagger UI e poderá testar todos os endpoints diretamente no navegador.

> **Atenção:** No Swagger selecione o servidor **Produção**: https://fiap-machine-learning-tech-challeng.vercel.app - Vercel server.

-----------------------------------

## Endpoints

### `POST /users/`
- **Descrição:** Registra um novo usuário no sistema.
- **Corpo da Requisição (application/json)**
  ```json
  {
    "username": "bob",
    "password": "strongpassword"
  }
  ```
- **Exemplo de Resposta (200 Created):**
  ```json
  {
    "username": "bob",
    "password": "strongpassword"
  }
  ```
  
### `GET /users/me`
- **Descrição:** Obtém os detalhes do usuário atualmente autenticado. **Requer autenticação.**
- **Exemplo de Resposta (200 Ok):**
  ```json
  {
    "id": "1",
    "username": "test_user"
  }
  ```

-----------------------------------

### `POST /auth/login`
- **Descrição:** Realiza login e gera um token de acesso JWT para um usuário, com base em suas credenciais.
- **Corpo da Requisição:**
- `username`(string, obrigatório)
- `password`(string, obrigatório)
- **Exemplo de Resposta (200 Ok):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTQzNDM1OTV9.ajROUaSSezlfxecLmcGdks7WsLSLj2bGOBFf3pM5xtk",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTQ0MjYzOTV9.XVcXe6bMY9dGuvpPzEhf-35dQIL53AYf-li-A8Eu8tw",
    "token_type": "bearer"
  }
  ```
### `POST /auth/refresh`
- **Descrição:** Usa refresh token para gerar novo access token.
- **Corpo da Requisição:**
- `refresh_token`: (string, obrigatório)
- **Exemplo de Resposta (200 Ok):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

---

### `GET /api/v1/health`
- **Descrição:** Verifica se a API está no ar.
- **Resposta (200):**
  ```json
  { "status": "ok" }
  ```

-----------------------------------

### `GET /api/v1/books`
- **Descrição:** Lista todos os livros carregados. **Requer autenticação.**
- **Resposta (200):**
  ```json
  [
    { 
      "id": 824,
      "title": "A Light in the Attic",
      "price": 51.77,
      "availability": "In Stock",
      "rating": "Three",
      "category": "Poetry",
      "image_url": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg" 
    }
  ]
  ```

### `GET /api/v1/books/{id}`
- **Descrição:** Retorna os detalhes de um livro específico pelo seu id. **Requer autenticação.**
- **Path Param:**
  - `id` (int, obrigatório)
- **Resposta (200):** Detalhes de um livro
  ```json
  {
    "id": 824,
    "title": "A Light in the Attic",
    "price": 51.77,
    "availability": "In Stock",
    "rating": "Three",
    "category": "Poetry",
    "image_url": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
  }
  ```
- **Resposta (404):**
  ```json
  { "detail": "Book not found" }
  ```

### `GET /api/v1/books/search`
- **Descrição:** Busca livros por título e/ou categoria. Se nenhum parâmetro for fornecido, 
retorna todos os livros. **Requer autenticação.**
- **Query Params:**
  - `title` (string, opcional)
  - `category` (string, opcional)
- **Resposta (200):** Lista de livros que atendem aos filtros.
  ```json
  [
    {
      "id": 824,
      "title": "A Light in the Attic",
      "price": 51.77,
      "availability": "In Stock",
      "rating": "Three",
      "category": "Poetry",
      "image_url": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
    }
  ]
  ```
### `/api/v1/books/top-rated`
- **Descrição:** Retorna uma lista dos livros com as melhores avaliações em ordem. **Requer autenticação.**
- **Query Params:**
  - `limit` (int, opcional, valor padrão = 10)
- **Resposta (200):** Lista de livros com as melhores avaliações.
  ```json
  [
    {
      "id": 11,
      "title": "1,000 Places to See Before You Die",
      "price": 26.08,
      "availability": "In Stock",
      "rating": "Five",
      "category": "Travel",
      "image_url": "https://books.toscrape.com/media/cache/9e/10/9e106f81f65b293e488718a4f54a6a3f.jpg"
    }
  ]
  ```  

### `/api/v1/books/price-range`
- **Descrição:** Filtra livros dentro de uma faixa de preço específica (inclusivo). **Requer autenticação.**
- **Query Params:**
  - `min` (float, obrigatório)
  - `max` (float, obrigatório)
- **Resposta (200):** Lista de livros com os valores de uma faixa específica.
  ```json
  [
    {
      "id": 11,
      "title": "1,000 Places to See Before You Die",
      "price": 26.08,
      "availability": "In Stock",
      "rating": "Five",
      "category": "Travel",
      "image_url": "https://books.toscrape.com/media/cache/9e/10/9e106f81f65b293e488718a4f54a6a3f.jpg"
    }
  ]
  ``` 
  
---

### `GET /api/v1/categories`
- **Descrição:** Retorna todas as categorias existentes. **Requer autenticação.**
- **Resposta (200):** Lista de todas as categorias
  ```json
  ["Travel", "Mystery", "Historical Fiction"]
  ```

-----------------------------------

### `GET /api/v1/stats/overview`
- **Descrição:** Retorna estatísticas gerais, como número total de livros, preço médio 
e distribuição de classificação. **Requer autenticação.**
- **Resposta (200):** Estatísticas
  ```json
  {
    "total_books": 1011,
    "average_price": 35.12,
    "rating_distribution": {
      "Five": 197,
      "Four": 181,
      "One": 228,
      "Three": 206,
      "Two": 199
      }
  }
  ```

### `GET /api/v1/stats/categories`
- **Descrição:** Retorna estatísticas detalhadas para cada categoria, 
incluindo contagem de livros e preço médio. **Requer autenticação.**
- **Resposta (200):** Lista de Estatísticas detalhadas por categoria
  ```json
  [
    {
      "category": "Poetry",
      "total_books": 19,
      "average_price": 47.66
    }
  ]
  ```
  
-----------------------------------

### `POST /api/v1/scraping/trigger`
- **Descrição:** Inicia o processo de web scraping em segundo plano para atualizar a 
base de dados de livros. **Requer autenticação.**
- **Resposta (202):** A API retornará um status 202 com uma mensagem para indicar que a tarefa foi iniciada com sucesso. 
Não há corpo na resposta.
  
-----------------------------------

## Testes Unitários e Integração

O projeto inclui uma suíte abrangente de testes utilizando pytest que combina **testes unitários** e **testes de integração** para garantir a qualidade e confiabilidade do código.

### 📊 Cobertura Atual
- **40 testes** implementados
- **54% de cobertura** de código

### 🧪 Tipos de Teste

**Testes Unitários:**
- Funções de autenticação e JWT
- Lógica de negócio isolada
- Utilitários e helpers

**Testes de Integração:**
- Endpoints da API completos
- Interação com banco de dados
- Fluxos de autenticação
- Serialização de dados

### 🚀 Executando os Testes

**Comandos disponíveis:**

```bash
# Executar todos os testes
python -m pytest tests/

# Executar com relatório de cobertura
python -m pytest tests/ --cov=api/app --cov-report=term-missing --cov-report=html:htmlcov

# Executar testes específicos
python -m pytest tests/test_auth.py
python -m pytest tests/test_book_controller.py
python -m pytest tests/test_books_service.py

# Executar com saída detalhada
python -m pytest tests/ -v
```

**Relatório HTML de Cobertura:**
Após executar os testes com `--cov-report=html:htmlcov`, abra o arquivo `htmlcov/index.html` no navegador para visualizar o relatório detalhado de cobertura.

### 🔧 Fixtures Disponíveis
- `db_session`: Sessão de banco de dados para testes
- `client`: Cliente de teste da API FastAPI
- `sample_user`: Usuário de exemplo para testes
- `multiple_books`: Conjunto de livros para testes

-----------------------------------

## Licença e Autores

### 🧑‍💻 Desenvolvido por

- `Beatriz Rosa Carneiro Gomes - RM365967`
- `Cristine Scheibler - RM365433`
- `Guilherme Fernandes Dellatin - RM365508`
- `Iana Alexandre Neri - RM360484`
- `João Lucas Oliveira Hilario - RM366185`

Este projeto é apenas para fins educacionais e segue a licença MIT.
