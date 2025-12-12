from django.contrib import admin
from .models import Marca

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)
