from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'codigo_barras', 'categoria', 'marca', 'fornecedor',
                  'unidade_medida', 'preco_custo', 'preco_venda', 'estoque_minimo', 'estoque_atual']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 3}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de barras'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-control'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço de custo'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço de venda'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estoque mínimo'}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estoque atual'}),
        }
