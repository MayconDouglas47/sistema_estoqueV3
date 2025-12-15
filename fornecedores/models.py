from django.db import models
from django.utils import timezone


class Fornecedor(models.Model):
    ESTADO_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField("Nome", max_length=150)
    cnpj = models.CharField("CNPJ", max_length=14, blank=True,
                            null=True, unique=True)
    telefone = models.CharField(
        "Telefone", max_length=11, blank=True, null=True)
    email = models.EmailField("Email", max_length=100, blank=True, null=True)

    # Campos de endereço normalizado
    rua = models.CharField("Rua", max_length=150, blank=True, null=True)
    numero = models.CharField("Número", max_length=20, blank=True, null=True)
    bairro = models.CharField("Bairro", max_length=100, blank=True, null=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True, null=True)
    estado = models.CharField("Estado", max_length=2,
                              choices=ESTADO_CHOICES, blank=True, null=True)
    cep = models.CharField("CEP", max_length=8, blank=True,
                           null=True)

    # Campo legado mantido para compatibilidade (será preenchido automaticamente)
    endereco = models.TextField("Endereço (legado)", blank=True,
                                null=True, help_text="Campo mantido apenas para compatibilidade")

    data_cadastro = models.DateTimeField(
        "Data de cadastro", default=timezone.now)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Atualizar campo legado de endereço com base nos campos normalizados
        self._atualizar_endereco_legado()

        super().save(*args, **kwargs)

    def _atualizar_endereco_legado(self):
        """Constrói o campo endereco a partir dos campos normalizados."""
        partes = []
        if self.rua:
            partes.append(self.rua)
        if self.numero:
            partes.append(f"nº {self.numero}")
        if self.bairro:
            partes.append(self.bairro)
        if self.cidade:
            partes.append(self.cidade)
        if self.estado:
            partes.append(self.get_estado_display())
        if self.cep:
            partes.append(f"CEP: {self.cep}")

        self.endereco = ", ".join(partes) if partes else ""

    def get_endereco_completo(self):
        """Retorna o endereço completo formatado."""
        return self._atualizar_endereco_legado() or self.endereco

    def get_cnpj_formatado(self):
        """Retorna o CNPJ formatado."""
        return self.cnpj if self.cnpj else ""

    def get_telefone_formatado(self):
        """Retorna o telefone formatado."""
        return self.telefone if self.telefone else ""

    def get_cep_formatado(self):
        """Retorna o CEP formatado."""
        return self.cep if self.cep else ""
