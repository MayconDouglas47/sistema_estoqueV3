from django.db import models

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nome
