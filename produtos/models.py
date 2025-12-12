from django.db import models
from django.utils import timezone
from categorias.models import Categoria
from marcas.models import Marca
from fornecedores.models import Fornecedor

class Produto(models.Model):
    UN = "UN"
    G = "G"
    KG = "KG"
    L = "L"
    CX = "CX"
    PAC = "PAC"
    MT = "MT"

    UNIDADE_CHOICES = [
        (UN, "Unidade"),
        (G, "Grama"),
        (KG, "Quilo"),
        (L, "Litro"),
        (CX, "Caixa"),
        (PAC, "Pacote"),
        (MT, "Metro"),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    codigo_barras = models.CharField(max_length=20, unique=True, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="produtos")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name="produtos", blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name="produtos", blank=True, null=True)
    unidade_medida = models.CharField(max_length=10, choices=UNIDADE_CHOICES, default=UN)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_minimo = models.IntegerField(default=0)
    estoque_atual = models.IntegerField(default=0)
    data_registro = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome
