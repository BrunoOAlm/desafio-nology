# Desafio Nology — App de Cashback

App que calcula o cashback de uma compra, registra cada consulta pelo IP de quem
acessou e mostra o histórico apenas daquele IP. O backend é uma API em Python
(FastAPI) e o frontend é estático (HTML + JavaScript puro), servido pela própria API.

## Estrutura

```
cashback.py     # regra de negócio do cashback (cálculo puro, sem framework)
database.py     # acesso ao PostgreSQL com psycopg2 (criar tabela, salvar, consultar)
main.py         # API FastAPI: /api/cashback, /api/history e o frontend estático
static/         # frontend: index.html, app.js, style.css
requirements.txt
render.yaml     # configuração de deploy no Render (API + banco Postgres)
```

## Regras do cashback

As regras vieram dos três documentos do desafio:

1. Cashback base de 5% sobre o valor final (depois dos descontos).
2. Cliente VIP ganha +10% sobre o cashback base.
3. Compras com valor final acima de R$ 500 têm o cashback dobrado (vale para todos).

A ordem do cálculo é: desconto → cashback base → bônus VIP → promoção (dobro).

## Como rodar localmente

O app usa PostgreSQL. Localmente, aponte a variável `DATABASE_URL` para um banco
Postgres acessível (pode ser o próprio banco criado no Render).

PowerShell:

```powershell
pip install -r requirements.txt
$env:DATABASE_URL = "postgresql://usuario:senha@host:5432/nome_do_banco"
uvicorn main:app --reload
```

Depois abra http://localhost:8000 no navegador.

## Endpoints

- `GET /api/health` — confirma que a API está no ar.
- `GET /api/cashback?client_type=vip&purchase_amount=600` — calcula o cashback,
  registra a consulta com o IP e devolve o resultado.
- `GET /api/history` — devolve o histórico de consultas do IP que está acessando.

## Deploy (Render)

O arquivo `render.yaml` cria, de uma vez só, a API web e um banco PostgreSQL, já
ligando os dois pela variável `DATABASE_URL`. Basta subir o código para o GitHub e
criar um "Blueprint" no Render apontando para o repositório.
