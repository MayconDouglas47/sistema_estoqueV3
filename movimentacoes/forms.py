from django import forms
from .models import EntradaEstoque, SaidaEstoque, EntradaItem, SaidaItem
from produtos.models import Produto


class EntradaEstoqueForm(forms.ModelForm):
    class Meta:
        model = EntradaEstoque
        fields = ['fornecedor', 'data_entrada',
                  'usuario_responsavel', 'observacao']
        widgets = {
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'data_entrada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'usuario_responsavel': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SaidaEstoqueForm(forms.ModelForm):
    class Meta:
        model = SaidaEstoque
        fields = ['tipo_saida', 'data_saida',
                  'usuario_responsavel', 'observacao']
        widgets = {
            'tipo_saida': forms.Select(attrs={'class': 'form-control'}),
            'data_saida': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'usuario_responsavel': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EntradaItemForm(forms.ModelForm):
    class Meta:
        model = EntradaItem
        fields = ['produto', 'quantidade', 'preco_unitario']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class SaidaItemForm(forms.ModelForm):
    class Meta:
        model = SaidaItem
        fields = ['produto', 'quantidade', 'preco_unitario']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
