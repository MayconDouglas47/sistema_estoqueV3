from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "marca", "fornecedor", "unidade_medida", "preco_venda", "estoque_atual")
    search_fields = ("nome", "codigo_barras")
    list_filter = ("categoria", "marca", "fornecedor", "unidade_medida")
