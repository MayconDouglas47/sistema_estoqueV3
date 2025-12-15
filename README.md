📦 Sistema de Estooque

🚧 Em desenvolvimento e correções de erros

Aplicação Django para gerenciamento de estoque, permitindo o controle de produtos, fornecedores, marcas e movimentações de entrada e saída.

🚀 Funcionalidades
🔐 Autenticação de Usuários

Sistema de login com 3 níveis de acesso:

Admin

Estoquista

Caixa

🗂️ Cadastro (CRUD)

Categorias

Marcas

Fornecedores

Produtos

🔄 Movimentações de Estoque

Entrada de produtos

Saída de produtos

Atualização automática do saldo em estoque

📊 Dashboard

KPIs de estoque

Alertas de estoque baixo

📄 Relatórios

Relatório de estoque atual

Histórico de movimentações

⚙️ Como rodar o projeto (Windows)

1️⃣ Criar e ativar o ambiente virtual

python -m venv venv

.\venv\Scripts\activate

2️⃣ Instalar as dependências

pip install -r requirements.txt

3️⃣ Aplicar as migrações

python manage.py migrate

4️⃣ Rodar o servidor

python manage.py runserver

🌐 Acesso ao sistema

http://127.0.0.1:8000/
