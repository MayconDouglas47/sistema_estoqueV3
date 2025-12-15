from django.contrib import admin
from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "cnpj", "telefone",
                    "email", "cidade", "data_cadastro")
    search_fields = ("nome", "cnpj", "email", "cidade")

    fieldsets = (
        ("Informações Básicas", {
            "fields": ("nome", "email")
        }),
        ("Documentação", {
            "fields": ("cnpj", "telefone"),
            "description": "CNPJ e telefone são validados e sanitizados automaticamente."
        }),
        ("Endereço", {
            "fields": ("rua", "numero", "bairro", "cidade", "estado", "cep"),
            "description": "Os campos de endereço são normalizados. O campo 'Endereço (legado)' é preenchido automaticamente."
        }),
        ("Endereço Legado", {
            "fields": ("endereco",),
            "description": "Este campo é preenchido automaticamente com base nos campos normalizados."
        }),
        ("Metadados", {
            "fields": ("data_cadastro",),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = ("endereco", "data_cadastro")
