# produto/views.py (MODIFICADO)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse  # IMPORTAÇÃO ADICIONADA
from django.core.paginator import Paginator
from .models import Produto
from .forms import ProdutoForm
from movimentacoes.models import EntradaItem, SaidaItem


@login_required
def index(request):
    produtos_list = Produto.objects.select_related(
        'categoria', 'marca', 'fornecedor').all().order_by('id')
    paginator = Paginator(produtos_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'produtos/index.html', {
        'produtos': produtos_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


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
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    produto = get_object_or_404(Produto, pk=pk)
    possui_movimentacoes = (
        EntradaItem.objects.filter(produto=produto).exists() or
        SaidaItem.objects.filter(produto=produto).exists()
    )

    # Verificação prévia (antes do modal)
    if request.headers.get('X-Check-Only') == 'true':
        return JsonResponse({'can_delete': not possui_movimentacoes})

    # Exclusão definitiva
    if possui_movimentacoes:
        messages.error(
            request, 'Não é possível excluir este produto pois existem movimentações associadas a ele.')
        return JsonResponse({
            'success': False,
            'message': 'Produto possui movimentações associadas. Não pode ser excluído.'
        }, status=400)

    nome_produto = produto.nome
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso!')
    return JsonResponse({'success': True, 'message': 'Produto excluído com sucesso!'})
