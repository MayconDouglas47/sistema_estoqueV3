from django.db import models
from django.utils import timezone
from fornecedores.models import Fornecedor
from usuarios.models import Usuario
from produtos.models import Produto

class EntradaEstoque(models.Model):
    id = models.AutoField(primary_key=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, null=True, blank=True, related_name="entradas")
    data_entrada = models.DateTimeField(default=timezone.now)
    usuario_responsavel = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="entradas")
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Entrada de Estoque"
        verbose_name_plural = "Entradas de Estoque"

    def __str__(self):
        return f"Entrada #{self.id} - {self.data_entrada.date()}"

class SaidaEstoque(models.Model):
    TIPO_VENDA = "venda"
    TIPO_PERDA = "perda"
    TIPO_DEVOLUCAO = "devolucao"
    TIPO_AJUSTE = "ajuste"

    TIPO_CHOICES = [
        (TIPO_VENDA, "Venda"),
        (TIPO_PERDA, "Perda"),
        (TIPO_DEVOLUCAO, "Devolução"),
        (TIPO_AJUSTE, "Ajuste"),
    ]

    id = models.AutoField(primary_key=True)
    tipo_saida = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_saida = models.DateTimeField(default=timezone.now)
    usuario_responsavel = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="saidas")
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Saída de Estoque"
        verbose_name_plural = "Saídas de Estoque"

    def __str__(self):
        return f"Saída #{self.id} - {self.tipo_saida} - {self.data_saida.date()}"

class EntradaItem(models.Model):
    id = models.AutoField(primary_key=True)
    entrada = models.ForeignKey(EntradaEstoque, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="entrada_itens")
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    class Meta:
        verbose_name = "Item da Entrada"
        verbose_name_plural = "Itens da Entrada"

    def save(self, *args, **kwargs):
        # calcula subtotal e atualiza estoque do produto
        self.subtotal = (self.quantidade or 0) * (self.preco_unitario or 0)
        super().save(*args, **kwargs)
        # Atualiza estoque_atual do produto
        produto = self.produto
        produto.estoque_atual = (produto.estoque_atual or 0) + (self.quantidade or 0)
        produto.save(update_fields=["estoque_atual"])

    def __str__(self):
        return f"{self.produto.nome} — {self.quantidade} {self.produto.unidade_medida}"

class SaidaItem(models.Model):
    id = models.AutoField(primary_key=True)
    saida = models.ForeignKey(SaidaEstoque, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="saida_itens")
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    class Meta:
        verbose_name = "Item da Saída"
        verbose_name_plural = "Itens da Saída"

    def save(self, *args, **kwargs):
        # calcula subtotal e atualiza estoque do produto (subtraindo)
        self.subtotal = (self.quantidade or 0) * (self.preco_unitario or 0)
        super().save(*args, **kwargs)
        produto = self.produto
        produto.estoque_atual = (produto.estoque_atual or 0) - (self.quantidade or 0)
        if produto.estoque_atual < 0:
            produto.estoque_atual = 0
        produto.save(update_fields=["estoque_atual"])

    def __str__(self):
        return f"{self.produto.nome} — {self.quantidade} {self.produto.unidade_medida}"
