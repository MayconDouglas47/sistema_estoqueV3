# produto/views.py (MODIFICADO)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse # IMPORTAÇÃO ADICIONADA
from .models import Produto
from .forms import ProdutoForm


@login_required
def index(request):
    produtos = Produto.objects.select_related(
        'categoria', 'marca', 'fornecedor').all().order_by('nome')
    return render(request, 'produtos/index.html', {'produtos': produtos})


@login_required
def criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('produtos:index')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/criar_produto.html', {'form': form})


@login_required
def editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produtos:index')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar_produto.html', {'form': form, 'produto': produto})


@login_required
def deletar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    # 1. Se a requisição for POST (vindo do modal de confirmação)
    if request.method == 'POST':
        try:
            produto.delete()
            messages.success(request, 'Produto excluído com sucesso!')
            
            # Resposta para o JavaScript (Fetch)
            return JsonResponse({'success': True}) 
        except Exception as e:
            # Em caso de erro (ex: chave estrangeira, etc.)
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    # 2. Se a requisição não for POST, retorne erro 405 (Método não permitido) 
    #    ou trate como preferir (a view deletar.html não será mais usada).
    return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)

# O TEMPLATE 'produtos/deletar_produto.html' NÃO É MAIS USADO POR ESTA VIEW.