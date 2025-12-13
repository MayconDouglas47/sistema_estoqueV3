# Sistema de Estoque

Aplicação Django para gerenciamento de estoque (produtos, fornecedores, marcas, movimentações de entrada/saída).

Principais features:
- Autenticação com usuários com 3 níveis de acesso: `Admin`, `Estoquista`, `Caixa`.
- CRUD para Categorias, Marcas, Fornecedores, Produtos.
- Movimentações: Entradas e Saídas com itens e atualização automática de estoque.
- Dashboard com KPIs e alertas de estoque baixo.
- Relatórios: Relatório de Estoque e Histórico de Movimentações.

Usuário de teste criado:
- login: `admin_test`
- senha: `Test@1234`

Como rodar (Windows):

1. Criar e ativar virtualenv

python -m venv venv
.\venv\Scripts\Activate

2. Instalar dependências

pip install -r requirements.txt

3. Aplicar migrations

python manage.py migrate

4. Rodar servidor

python manage.py runserver

5. Acessar http://127.0.0.1:8001/ e logar com o usuário de teste.

Observações:
- Para criar novos usuários use o Django admin ou o shell com o `UsuarioManager`.
- Para ajustar permissões no front-end, edite `templates/includes/sidebar.html` (usa o template tag `has_access`).

