from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password


class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'login', 'senha', 'nivel_acesso', 'is_active']
        labels = {
            'nome': 'Nome',
            'login': 'Login',
            'senha': 'Senha',
            'nivel_acesso': 'Nível de acesso',
            'is_active': 'Ativo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se é um usuário admin, desabilitar o campo is_active e mantê-lo sempre True
        if self.instance and self.instance.pk and self.instance.nivel_acesso == Usuario.NIVEL_ADMIN:
            self.fields['is_active'].disabled = True
            self.fields['is_active'].initial = True
            self.fields['is_active'].help_text = 'Usuários administradores não podem ser desativados.'

    def clean(self):
        cleaned_data = super().clean()
        # Garantir que admin sempre permaneça ativo
        if self.instance and self.instance.pk and self.instance.nivel_acesso == Usuario.NIVEL_ADMIN:
            cleaned_data['is_active'] = True
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)

        # Se foi informada uma senha nova, criptografa
        if self.cleaned_data.get("senha"):
            usuario.password = make_password(self.cleaned_data["senha"])

        # Garantir que admin sempre permaneça ativo
        if usuario.nivel_acesso == Usuario.NIVEL_ADMIN:
            usuario.is_active = True

        if commit:
            usuario.save()

        return usuario
