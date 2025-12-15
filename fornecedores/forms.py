from django import forms
from .models import Fornecedor


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'email', 'telefone', 'rua',
                  'numero', 'bairro', 'cidade', 'estado', 'cep']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do fornecedor'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0001-00',
                'autocomplete': 'off'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (opcional)'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 90000-0000',
                'autocomplete': 'off'
            }),
            'rua': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua (opcional)'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número (opcional)',
                'maxlength': '20'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro (opcional)'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade (opcional)'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CEP (opcional)',
                'maxlength': '9'
            }),
        }
