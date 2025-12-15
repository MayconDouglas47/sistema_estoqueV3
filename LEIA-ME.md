📦 Sistema de Estooque

🚧 Em desenvolvimento e correções de erros

Aplicação Django para gerenciamento de estoque, permitindo o controle de produtos, fornecedores, marcas e movimentações de entrada e saída.

🚀 Funcionalidades
🔐 Autenticação de Usuários

Sistema de login com 3 níveis de acesso:

Admin

Estoquista

Caixa

⚙️ Como rodar o projeto (Windows)

1️⃣ Criar e ativar o ambiente virtual

python -m venv venv

.\venv\Scripts\activate

2️⃣ Instalar as dependências

pip install -r requirements.txt

3️⃣ Aplicar as migrações

python manage.py migrate

4️⃣ Criar o primeiro usuário (Administrador)

python manage.py createsuperuser

O sistema solicitará:
- **Username**: Nome de usuário para login
- **Email**: E-mail (opcional, pode deixar em branco)
- **Senha**: Senha de acesso (não aparece ao digitar)

Este usuário terá:
- ✅ Nível de acesso: **ADMINISTRADOR**
- ✅ Acesso ao Django Admin: `http://127.0.0.1:8000/admin/`
- ✅ Acesso total ao sistema (gerenciar usuários, fornecedores, produtos, movimentações)

5️⃣ Rodar o servidor

python manage.py runserver

6️⃣ Acessar o sistema

Abra o navegador em: `http://127.0.0.1:8000/`

