from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UsuarioCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirme a senha", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ("login", "nome")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não coincidem")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ("login", "nome", "password",
                  "is_active", "is_staff", "nivel_acesso")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se é um usuário admin, desabilitar o campo is_active
        if self.instance and self.instance.pk and self.instance.nivel_acesso == Usuario.NIVEL_ADMIN:
            self.fields['is_active'].disabled = True
            self.fields['is_active'].help_text = 'Administradores não podem ser desativados.'

    def clean(self):
        cleaned_data = super().clean()
        # Garantir que admin sempre permaneça ativo
        if self.instance and self.instance.pk and self.instance.nivel_acesso == Usuario.NIVEL_ADMIN:
            cleaned_data['is_active'] = True
        return cleaned_data


class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    list_display = ("id", "login", "nome", "nivel_acesso",
                    "is_staff", "is_active")
    list_filter = ("nivel_acesso", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("login", "password")}),
        ("Informações pessoais", {"fields": ("nome",)}),
        ("Permissões", {"fields": ("is_active", "is_staff",
         "is_superuser", "nivel_acesso", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("login", "nome", "password1", "password2", "is_staff", "is_active", "nivel_acesso")
        }),
    )
    search_fields = ("login", "nome")
    ordering = ("id",)
    filter_horizontal = ("groups", "user_permissions")

    def has_delete_permission(self, request, obj=None):
        # Impedir exclusão de usuários admin
        if obj and obj.nivel_acesso == Usuario.NIVEL_ADMIN:
            return False
        return super().has_delete_permission(request, obj)


admin.site.register(Usuario, UsuarioAdmin)
