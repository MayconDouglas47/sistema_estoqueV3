# Sistema de Estoque

Aplicação Django para gerenciamento de estoque
(produtos, fornecedores, marcas e movimentações de entrada/saída).

## Funcionalidades

- Autenticação de usuários com 3 níveis de acesso:
  - Admin
  - Estoquista
  - Caixa
- CRUD de:
  - Categorias
  - Marcas
  - Fornecedores
  - Produtos
- Movimentações:
  - Entrada e Saída de produtos
  - Atualização automática do estoque
- Dashboard com KPIs e alertas de estoque baixo
- Relatórios:
  - Relatório de estoque atual
  - Histórico de movimentações

## Como rodar o projeto (Windows)

### 1. Criar e ativar o ambiente virtual

python -m venv venv

.\venv\Scripts\activate

### 2. Instalar dependências

pip install -r requirements.txt

### 3. aplicar migrações 

python manage.py migrate

### 4. Rodar o servidor 

python manage.py runserver

### Acesse:

http://127.0.0.1:8000/
