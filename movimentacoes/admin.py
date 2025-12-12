from django.contrib import admin
from .models import EntradaEstoque, SaidaEstoque, EntradaItem, SaidaItem

class EntradaItemInline(admin.TabularInline):
    model = EntradaItem
    extra = 1

class SaidaItemInline(admin.TabularInline):
    model = SaidaItem
    extra = 1

@admin.register(EntradaEstoque)
class EntradaEstoqueAdmin(admin.ModelAdmin):
    list_display = ("id", "fornecedor", "data_entrada", "usuario_responsavel")
    inlines = [EntradaItemInline]

@admin.register(SaidaEstoque)
class SaidaEstoqueAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_saida", "data_saida", "usuario_responsavel")
    inlines = [SaidaItemInline]
