# API de Livros - FIAP Machine Learning Tech Challenge 1

Projeto de extração e API pública para consulta de livros, integrando web scraping e FastAPI.

| ![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688?logo=fastapi) ![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg) |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|

-----------------------------------

## Sumário

- [Descrição](#descrição)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura](#arquitetura)
- [Como Utilizar](#como-utilizar)
- [Endpoints](#endpoints)
- [Licença, Autores e Agradecimentos](#licença-autores)

-----------------------------------

## Descrição

O objetivo deste projeto é expor uma **API RESTful** para facilitar o acesso aos dados de diversos livros. Esses dados originalmente são extraídos via **web scraping** do site [Books to Scrape](https://books.toscrape.com/) 

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
│       ├── models/              # Modelos SQLAlchemy
│       ├── schemas/             # Schemas Pydantic (request/response)
│       └── services/            # Lógica de negócio e componente de scraping
├── requirements.txt             # Dependências gerais do projeto
├── runtime.txt                  # Versão do runtime (deploy)
└── vercel.json                  # Configurações de deploy
```

### Descrição das camadas:

**controllers**: Define os pontos de entrada da API (endpoints) e realiza roteamento.

**services**: Implementa a lógica de negócio, orquestrando operações de scraping e acesso a dados via models.

**models**: Representa o domínio de dados, definindo entidades e mapeamentos com SQLAlchemy.

**schemas**: Contém os Pydantic models para validação e serialização de requisições e respostas.

**core**: Agrupa configurações centrais, como autenticação JWT, inicialização de sessão de banco de dados e configurações gerais.

Essa separação melhora a modularidade, favorece testes unitários e permite evoluir cada camada independentemente.

-----------------------------------

## Como Utilizar

Você pode usar a API de duas formas: **localmente** no seu ambiente de desenvolvimento ou 
consumindo a **versão já deployada**.

Para sua conveniência, o repositório já inclui um banco de dados (`.sqlite`) e um arquivo (`.csv`) 
com os dados atualizados obtidos via Web Scraping previamente, além de um usuário de testes já criado. 
Isso permite que você teste a API imediatamente com uma base de dados de cerca de mil livros, sem precisar executar o Web Scraping.

**Autenticação (válido para ambos os modos)**

Cadastre um usuário (ou utilize o de teste)

Usuário de teste:

    username: test_user  
    password: test12345

Não se esqueça de gerar e usar o token JWT antes de acessar os dados.

### ☁️ Via Deploy (produção)

Acesse a versão pública em: https://fiap-machine-learning-tech-challeng-taupe.vercel.app/api/docs 

Lá você terá o Swagger UI e poderá testar todos os endpoints diretamente no navegador.

### 🏠 Execução Local

### Pré-requisitos

- Git
- Python 3.11+

### Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/cris-scheib/fiap-machine-learning-tech-challenge-1.git
   cd fiap-machine-learning-tech-challenge-1
   ```
2. **Crie e ative um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. **Instale dependências gerais**
   ```bash
   pip install -r requirements.txt
   ```
4. **Inicie a API**
   ```bash
   cd api
   uvicorn main:app --reload
   ```
5. **Execute o Scraping (Opcional)**

    > **Atenção:** O processo de Web Scraping é demorado, levando mais de 30 minutos. 
    > **Ele não é necessário para iniciar a API**, a menos que você queira gerar os dados do zero,e **antes de sua
    execução certifique-se de criar ou ter um usuário criado**.

   ```bash
   cd api
   python -m app.services.scrapper.scrapper_service
   ```

A API estará disponível em `http://127.0.0.1:8000`. 

A documentação interativa é acessível em `http://127.0.0.1:8000/docs` (Swagger UI) 
e `http://127.0.0.1:8000/redoc` (ReDoc).

## Endpoints

### Autenticação (opcional)

#### `POST /api/v1/auth/login`
- **Descrição:** Gera um token JWT para acesso a rotas protegidas.
- **Body Request:**
  ```json
  { "username": "seu_usuario", "password": "sua_senha" }
  ```
- **Resposta (200):**
  ```json
  { "access_token": "<seu_token>", "token_type": "bearer" }
  ```

Inclua no header das requisições protegidas:
```
Authorization: Bearer <seu_token>
```

---

### `GET /api/v1/health`
- **Descrição:** Verifica se a API está no ar.
- **Resposta (200):**
  ```json
  { "status": "ok" }
  ```

---

### `GET /api/v1/books`
- **Descrição:** Lista todos os livros carregados.
- **Resposta (200):**
  ```json
  [
    { "id": 1, "title": "A Light in the Attic", "price": 51.77, "category": "Travel", "availability": "In stock", "rating": 3 },
    ...
  ]
  ```

---

### `GET /api/v1/books/{id}`
- **Descrição:** Obtém detalhes completos de um livro pelo seu ID.
- **Path Param:**
  - `id` (int)
- **Resposta (200):**
  ```json
  { "id": 1, "title": "A Light in the Attic", "price": 51.77, "category": "Travel", "availability": "In stock", "rating": 3, "description": "Descrição detalhada..." }
  ```
- **Resposta (404):**
  ```json
  { "detail": "Book not found" }
  ```

---

### `GET /api/v1/books/search`
- **Descrição:** Busca livros por título parcial e/ou categoria.
- **Query Params:**
  - `title` (string, opcional)
  - `category` (string, opcional)
- **Resposta (200):** Lista de livros que atendem aos filtros.

---

### `GET /api/v1/categories`
- **Descrição:** Retorna todas as categorias existentes.
- **Resposta (200):**
  ```json
  ["Travel", "Mystery", "Historical Fiction", ...]
  ```

## Licença, Autores

### 🧑‍💻 Desenvolvido por

- `Beatriz Rosa Carneiro Gomes - RM365967`
- `Cristine Scheibler - RM365433`
- `Guilherme Fernandes Dellatin - RM365508`
- `Iana Alexandre Neri - RM360484`
- `João Lucas Oliveira Hilario - RM366185`

Este projeto é apenas para fins educacionais e segue a licença MIT.


---------------- Lembrete para remover abaixo ----------------
### Features

- **Complete Data Extraction**: Title, price, rating, availability, category, image URL
- **Robust Error Handling**: Retry logic and comprehensive logging
- **Respectful Scraping**: Configurable delays and rate limiting
- **Pagination Support**: Automatically handles multi-page categories
- **Data Quality**: Text cleaning and normalization

### Output

The scraper creates a CSV file in the `data/` directory with the following columns:
- `title`: Book title
- `price`: Numeric price value
- `rating`: Star rating (One, Two, Three, Four, Five)
- `availability`: Availability status
- `category`: Book category
- `image_url`: Full URL to the book cover image
- `book_url`: URL to the book detail page

### Configuration

You can modify the following in `scripts/scrapper.py`:
- `DELAY_BETWEEN_REQUESTS`: Delay between requests (default: 1.0 seconds)
- `MAX_RETRIES`: Maximum retry attempts (default: 3)

## API <a name="api"></a>

### Quick Start

1. Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
# Option 1: Using pip directly
pip install -r requirements.txt

# Option 2: Using the installation script
python install_dependencies.py
```

> **Note**: If you encounter import errors, make sure to run the installation script to properly install all dependencies.

3. Run the script to start the server:
```bash
# Option 1: Standard startup
python start_server.py

# Option 2: Startup with dependency checks (recommended if you have import errors)
python start_server_with_checks.py
```

4. Or navigate to the API directory and run:
```bash
cd api
uvicorn main:app --reload
```

### Available Endpoints

- `GET /api/v1/books`: List all books
- `GET /api/v1/books/search?title=&category=`: Search books by title and category
- `GET /api/v1/books/{id}`: Get a book by ID

### Endpoint GET /api/v1/books/{id}

This endpoint returns the details of a specific book by its ID.

**Example Response (Book found):**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "availability": "In stock",
  "rating": "Three",
  "category": "Poetry"
}
```

**Example Response (Book not found):**
```json
{
  "detail": "Error Book not found."
}
```

### Compatibility Issues

If you encounter compatibility issues when running the API, try:

1. Using Python 3.9 or 3.10 instead of newer versions
2. Running the `simulate_endpoint.py` script to test functionality without starting the server
3. Checking if the dependency versions in `requirements.txt` are compatible with your Python version

## Project Structure <a name="structure"></a>

```
fiap-machine-learning-tech-challenge-1/
├── api/                    # REST API application
│   ├── app/
│   │   ├── controllers/    # API controllers
│   │   ├── core/          # Core functionality (auth, database)
│   │   ├── models/        # Data models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   ├── main.py            # FastAPI application entry point
│   └── requirements.txt   # API dependencies
├── scripts/               # Web scraping tools
│   ├── scrapper.py        # Main scraper script
│   ├── demo_scrapper.py   # Demo version for testing
│   ├── test_scrapper.py   # Test script
│   ├── utils.py           # Utility functions
│   ├── requirements.txt   # Scraper dependencies
│   ├── run_scrapper.bat   # Windows batch file
│   └── README.md          # Scraper documentation
├── data/                  # Output directory for scraped data
└── README.md              # This file
```

![image]()

## Troubleshooting

### Import Errors

If you encounter import errors like `Unable to import 'fastapi'` or `Unable to import 'sqlalchemy'`, follow these steps:

1. Make sure you have activated your virtual environment
2. Run the environment check script to diagnose and fix issues:
   ```bash
   python check_environment.py
   ```
   This script will check your Python version, installed dependencies, and project structure, and offer to install any missing dependencies.

3. Alternatively, run the installation script to install all dependencies:
   ```bash
   python install_dependencies.py
   ```

4. If the issue persists, try installing the dependencies manually:
   ```bash
   pip install fastapi==0.95.2 uvicorn==0.22.0 pydantic==1.10.8 sqlalchemy==1.4.48 beautifulsoup4==4.12.2 requests==2.31.0
   ```

## Compatibility Issues

This project was developed and tested with Python 3.8+. Some compatibility issues may occur with older versions.

## Licensing, Authors and Acknowledgments<a name="licensing"></a>
