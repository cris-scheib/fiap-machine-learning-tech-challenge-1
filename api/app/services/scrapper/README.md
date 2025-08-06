# Books to Scrape Web Scraper

-----------------------------------

## Componente de Scraping

O coração da coleta de dados do projeto reside no componente de scraping, projetado para ser robusto e eficiente na extração de informações do site `books.toscrape.com`. Ele é dividido em duas partes principais: um serviço orquestrador (**`scrapper_service.py`**) e um módulo de utilitários (**`scrapper_utils.py`**), que trabalham em conjunto.

### Fluxo de Execução do Scraper

O processo de scraping é orquestrado pelo `scrapper_service.py` e segue os seguintes passos:

1.  **Busca de Categorias**: O scraper primeiro acessa a página inicial do site para mapear e extrair as URLs de todas as categorias de livros disponíveis.
2.  **Navegação por Categoria**: Para cada categoria encontrada, ele navega pela sua página inicial.
3.  **Coleta de Livros e Paginação**: O scraper extrai a URL de cada livro listado na página e, de forma inteligente, procura por um botão "next" para avançar para as próximas páginas da mesma categoria, garantindo que todos os livros sejam coletados.
4.  **Extração de Dados**: Para cada URL de livro, uma requisição é feita para extrair os dados brutos da página (título, preço, avaliação, etc.).
5.  **Limpeza e Processamento**: Os dados brutos extraídos são processados e limpos pelas funções do módulo `scrapper_utils.py`.
6.  **Armazenamento**: Ao final do processo, os dados limpos e estruturados são salvos em dois locais:
    * No banco de dados **SQLite**, para serem consumidos pela API.
    * Em um arquivo **CSV**, servindo para análises futuras.

-----------------------------------

### A Classe `BooksToScrapeScraper`

Esta classe encapsula toda a lógica e o estado do scraper. Seus métodos são organizados para dividir o processo complexo de scraping em etapas menores e gerenciáveis.

- **__init__(self, ...)**: O construtor da classe. Inicializa o scraper com a URL base do site e o `delay` (atraso) a ser respeitado entre as requisições. Ele também valida a URL para garantir que o processo não inicie com um endereço inválido.


- **get_all_category_urls(self)**: Responsável por acessar a página inicial do site, encontrar o menu lateral de categorias e extrair o nome e a URL de cada uma delas, preparando a lista de "tarefas" para o scraper.


- **get_all_book_urls_from_category(category_url)**: Método estático que recebe a URL de uma categoria e navega por todas as suas páginas (utilizando a lógica de paginação "next") para coletar as URLs de todos os livros contidos nela.


- **extract_book_data(book_url)**: Recebe a URL de um único livro e extrai todas as informações detalhadas de sua página: título, preço, avaliação, disponibilidade, categoria e link da imagem. Utiliza intensivamente as funções do `scrapper_utils.py` para limpar e formatar os dados.


- **scrape_all_books(self)**: É o método orquestrador principal. Ele executa o fluxo completo: chama `get_all_category_urls`, itera sobre os resultados, chama `get_all_book_urls_from_category` para cada categoria, e por fim, `extract_book_data` para cada livro, respeitando o `delay` definido entre as requisições.


- **save_to_csv(books_data, ...)**: Um método estático que recebe a lista final de dados dos livros e utiliza a biblioteca `pandas` para salvá-los de forma organizada em um arquivo CSV com nome único (gerado com timestamp).


- **save_to_db(books_data, db)**: Também estático, este método é responsável por persistir os dados no banco de dados. Ele converte cada dicionário de livro em uma entidade SQLAlchemy (`Book`) e realiza uma operação de inserção em massa (`add_all`) para maior eficiência.

### Utilitários de Scraping (`scrapper_utils.py`)

Este módulo contém um conjunto de funções auxiliares de baixo nível, responsáveis pelo trabalho pesado de realizar requisições, processar e extrair dados brutos.

- **safe_request(url, ...)**: Realiza requisições HTTP de forma segura e resiliente. Inclui um `User-Agent` para simular um navegador, múltiplas tentativas (retries) com delay em caso de falha e timeouts para evitar que o script fique travado.


- **clean_text(text)**: Limpa strings removendo espaços em branco extras, tabulações e quebras de linha, padronizando o texto para armazenamento.


- **extract_price(price_text)**: Utiliza expressões regulares (regex) para localizar e extrair um valor numérico (`float`) a partir de uma string de preço (ex: "£51.77"), ignorando símbolos de moeda.


- **extract_rating(rating_class)**: Extrai a avaliação em texto (ex: 'Five', 'Three') a partir do atributo `class` do elemento HTML da classificação por estrelas.


- **check_availability(availability_text)**: Verifica e padroniza o status de disponibilidade do livro para "In Stock" ou "Out of Stock", garantindo consistência dos dados.


- **validate_url(url)**: Uma função simples para verificar se uma string de URL possui um formato válido antes de tentar fazer uma requisição.


- **create_filename(base_name, ...)**: Gera um nome de arquivo único adicionando um timestamp (data e hora), ideal para salvar os arquivos CSV sem sobrescrever os dados de coletas anteriores.

## Example Output

```
INFO:__main__:Initializing the database and creating tables if necessary...
INFO:__main__:Database ready.
INFO:__main__:Starting Books to Scrape scraper...
INFO:__main__:Starting to scrape all books...
INFO:__main__:Fetching category URLs...
....
INFO:__main__:Successfully extracted data for: 1,000 Places to See Before You Die
...
INFO:__main__:Scraping completed. Total books extracted: 11
INFO:__main__:Inserted 11 records into the database.
INFO:__main__:Total records: 11
INFO:__main__:Data Summary:
INFO:__main__:- Total books: 11
INFO:__main__:- Categories: 1
INFO:__main__:- Price range: £23.21 - £56.88
INFO:__main__:- Average price: £39.79
INFO:__main__:- Rating distribution: {'Two': 3, 'Three': 3, 'Four': 2, 'One': 2, 'Five': 1}
INFO:__main__:Scraping completed successfully!
INFO:__main__:Data saved to db: 11
INFO:__main__:Scraping completed successfully!
INFO:__main__:Data saved to: ../api/app/core/data\books_data_20250806_115921.csv
```


## Licença e Autores

### 🧑‍💻 Desenvolvido por

- `Beatriz Rosa Carneiro Gomes - RM365967`
- `Cristine Scheibler - RM365433`
- `Guilherme Fernandes Dellatin - RM365508`
- `Iana Alexandre Neri - RM360484`
- `João Lucas Oliveira Hilario - RM366185`

Este projeto é apenas para fins educacionais e segue a licença MIT.