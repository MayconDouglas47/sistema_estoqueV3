#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo realistas.
Execute com: python manage.py shell < populate_data.py
"""

from django.utils import timezone
from usuarios.models import Usuario
from categorias.models import Categoria
from marcas.models import Marca
from fornecedores.models import Fornecedor
from produtos.models import Produto
from movimentacoes.models import EntradaEstoque, SaidaEstoque, EntradaItem, SaidaItem
from datetime import timedelta
import random

print("\n=== Iniciando população do banco de dados ===\n")

# 1. Criar usuários
usuarios_data = [
    {'login': 'joao_estoquista', 'nome': 'João Silva',
        'password': 'Estoque@123', 'nivel_acesso': Usuario.NIVEL_ESTOQUISTA},
    {'login': 'maria_estoquista', 'nome': 'Maria Santos',
        'password': 'Estoque@123', 'nivel_acesso': Usuario.NIVEL_ESTOQUISTA},
    {'login': 'pedro_caixa', 'nome': 'Pedro Costa',
        'password': 'Caixa@123', 'nivel_acesso': Usuario.NIVEL_CAIXA},
]

usuarios = {}
for udata in usuarios_data:
    login = udata.pop('login')
    password = udata.pop('password')

    if not Usuario.objects.filter(login=login).exists():
        u = Usuario.objects.create_user(login, password, **udata)
        usuarios[login] = u
        print(f"✓ Usuário criado: {u.nome}")
    else:
        usuarios[login] = Usuario.objects.get(login=login)
        print(f"→ Usuário já existe: {login}")

# 2. Criar categorias
categorias_list = ['Eletrônicos', 'Livros',
                   'Vestuário', 'Alimentos', 'Higiene']

categorias = {}
for nome in categorias_list:
    c, created = Categoria.objects.get_or_create(nome=nome)
    categorias[nome] = c
    status = "criada" if created else "já existia"
    print(f"✓ Categoria {status}: {nome}")

# 3. Criar marcas
marcas_list = ['Samsung', 'LG', 'Sony', 'Philips', 'Positivo']

marcas = {}
for nome in marcas_list:
    m, created = Marca.objects.get_or_create(nome=nome)
    marcas[nome] = m
    status = "criada" if created else "já existia"
    print(f"✓ Marca {status}: {nome}")

# 4. Criar fornecedores
fornecedores_data = [
    {'nome': 'Distribuição XYZ', 'cnpj': '12.345.678/0001-90', 'email': 'contato@xyz.com',
        'telefone': '1133334444', 'endereco': 'Rua A, 100, São Paulo, SP'},
    {'nome': 'Fornecedor ABC', 'cnpj': '98.765.432/0001-10', 'email': 'vendas@abc.com',
        'telefone': '1144445555', 'endereco': 'Av. B, 200, São Paulo, SP'},
    {'nome': 'Importadora DEF', 'cnpj': '55.666.777/0001-88', 'email': 'pedidos@def.com',
        'telefone': '1155556666', 'endereco': 'Rua C, 300, São Paulo, SP'},
]

fornecedores = {}
for fdata in fornecedores_data:
    f, created = Fornecedor.objects.get_or_create(
        cnpj=fdata['cnpj'], defaults={k: v for k, v in fdata.items() if k != 'cnpj'})
    fornecedores[f.nome] = f
    status = "criado" if created else "já existia"
    print(f"✓ Fornecedor {status}: {f.nome}")

# 5. Criar produtos
produtos_data = [
    {'nome': 'Smart TV 55"', 'codigo_barras': 'TV001', 'categoria': 'Eletrônicos', 'marca': 'Samsung',
        'preco_custo': 1500.00, 'preco_venda': 1999.99, 'estoque_minimo': 5, 'estoque_atual': 8},
    {'nome': 'Notebook i7', 'codigo_barras': 'NB001', 'categoria': 'Eletrônicos', 'marca': 'Positivo',
        'preco_custo': 2500.00, 'preco_venda': 3299.99, 'estoque_minimo': 3, 'estoque_atual': 6},
    {'nome': 'Mouse Gamer', 'codigo_barras': 'MG001', 'categoria': 'Eletrônicos', 'marca': 'Sony',
        'preco_custo': 80.00, 'preco_venda': 149.99, 'estoque_minimo': 20, 'estoque_atual': 45},
    {'nome': 'Teclado Mecânico', 'codigo_barras': 'KB001', 'categoria': 'Eletrônicos', 'marca': 'Philips',
        'preco_custo': 250.00, 'preco_venda': 399.99, 'estoque_minimo': 10, 'estoque_atual': 25},
    {'nome': 'Camisa Básica', 'codigo_barras': 'CB001', 'categoria': 'Vestuário', 'marca': 'Positivo',
        'preco_custo': 25.00, 'preco_venda': 79.99, 'estoque_minimo': 30, 'estoque_atual': 120},
    {'nome': 'Calça Jeans', 'codigo_barras': 'CJ001', 'categoria': 'Vestuário', 'marca': 'Samsung',
        'preco_custo': 40.00, 'preco_venda': 119.99, 'estoque_minimo': 20, 'estoque_atual': 80},
    {'nome': 'Livro Python Avançado', 'codigo_barras': 'LV001', 'categoria': 'Livros', 'marca': 'LG',
        'preco_custo': 60.00, 'preco_venda': 99.99, 'estoque_minimo': 5, 'estoque_atual': 15},
    {'nome': 'Shampoo 500ml', 'codigo_barras': 'SH001', 'categoria': 'Higiene', 'marca': 'Sony',
        'preco_custo': 15.00, 'preco_venda': 39.99, 'estoque_minimo': 50, 'estoque_atual': 150},
]

produtos = {}
for pdata in produtos_data:
    categoria_nome = pdata.pop('categoria')
    marca_nome = pdata.pop('marca')
    codigo = pdata.pop('codigo_barras')
    p, created = Produto.objects.get_or_create(
        codigo_barras=codigo,
        defaults={
            **pdata,
            'categoria': categorias[categoria_nome],
            'marca': marcas[marca_nome],
        }
    )
    produtos[codigo] = p
    status = "criado" if created else "já existia"
    print(f"✓ Produto {status}: {p.nome}")

# 6. Criar entradas de estoque
agora = timezone.now()
entrada_count = 0
for i in range(1, 4):
    entrada = EntradaEstoque.objects.create(
        usuario_responsavel=usuarios['joao_estoquista'],
        fornecedor=random.choice(list(fornecedores.values())),
        data_entrada=agora - timedelta(days=random.randint(1, 30)),
        observacao=f'Entrada #{i} de fornecedor'
    )
    entrada_count += 1

    for codigo, produto in list(produtos.items())[:random.randint(2, 4)]:
        quantidade = random.randint(5, 30)
        EntradaItem.objects.create(
            entrada=entrada,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=produto.preco_custo
        )
    print(f"✓ Entrada #{entrada.id} criada com {entrada.itens.count()} itens")

# 7. Criar saídas de estoque
saida_count = 0
for i in range(1, 3):
    saida = SaidaEstoque.objects.create(
        usuario_responsavel=usuarios['maria_estoquista'],
        tipo_saida='venda',
        data_saida=agora - timedelta(days=random.randint(1, 15)),
        observacao=f'Saída #{i} - venda'
    )
    saida_count += 1

    for codigo, produto in list(produtos.items())[:random.randint(1, 3)]:
        quantidade = random.randint(1, 10)
        if produto.estoque_atual >= quantidade:
            SaidaItem.objects.create(
                saida=saida,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco_venda
            )
    print(f"✓ Saída #{saida.id} criada com {saida.itens.count()} itens")

print(f"\n=== Banco de dados populado com sucesso! ===")
print(f"✓ {len(usuarios)} usuários")
print(f"✓ {len(categorias)} categorias")
print(f"✓ {len(marcas)} marcas")
print(f"✓ {len(fornecedores)} fornecedores")
print(f"✓ {len(produtos)} produtos")
print(f"✓ {entrada_count} entradas")
print(f"✓ {saida_count} saídas\n")
