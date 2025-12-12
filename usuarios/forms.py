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

    def save(self, commit=True):
        usuario = super().save(commit=False)

        # Se foi informada uma senha nova, criptografa
        if self.cleaned_data.get("senha"):
            usuario.password = make_password(self.cleaned_data["senha"])

        if commit:
            usuario.save()

        return usuario
