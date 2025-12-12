from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UsuarioManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    NIVEL_ADMIN = "admin"
    NIVEL_ESTOQUISTA = "estoquista"
    NIVEL_CAIXA = "caixa"

    NIVEL_CHOICES = [
        (NIVEL_ADMIN, "Admin"),
        (NIVEL_ESTOQUISTA, "Estoquista"),
        (NIVEL_CAIXA, "Caixa"),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField("Nome", max_length=150)
    login = models.CharField("Login", max_length=50, unique=True)
    nivel_acesso = models.CharField(
        "Nível de acesso", max_length=30, choices=NIVEL_CHOICES, default=NIVEL_ESTOQUISTA)
    is_staff = models.BooleanField("Staff", default=False)
    is_active = models.BooleanField("Ativo", default=True)
    data_criacao = models.DateTimeField(
        "Data de criação", default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["nome"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.nome} ({self.login})"
