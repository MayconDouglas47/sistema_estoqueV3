from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import EntradaEstoque, SaidaEstoque, EntradaItem, SaidaItem
from .forms import EntradaEstoqueForm, SaidaEstoqueForm, EntradaItemForm, SaidaItemForm
from produtos.models import Produto
from django.db.models import Sum, F, DecimalField, Count


@login_required
def index(request):
    # Página combinada não é mais usada; redireciona para entradas
    return redirect('movimentacoes:entradas')


@login_required
def entradas(request):
    entradas_list = (
        EntradaEstoque.objects.select_related(
            'fornecedor', 'usuario_responsavel')
        .annotate(total_itens=Count('itens'))
        .all()
        .order_by('-data_entrada')
    )
    total_entradas = entradas_list.count()
    total_itens = EntradaItem.objects.count()
    ultima_entrada = entradas_list.first()
    paginator = Paginator(entradas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movimentacoes/entradas.html', {
        'entradas': entradas_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_entradas': total_entradas,
        'total_itens': total_itens,
        'ultima_entrada': ultima_entrada,
    })


@login_required
def saidas(request):
    saidas_list = (
        SaidaEstoque.objects.select_related('usuario_responsavel')
        .annotate(total_itens=Count('itens'))
        .all()
        .order_by('-data_saida')
    )
    total_saidas = saidas_list.count()
    total_itens = SaidaItem.objects.count()
    ultima_saida = saidas_list.first()
    paginator = Paginator(saidas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movimentacoes/saidas.html', {
        'saidas': saidas_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_saidas': total_saidas,
        'total_itens': total_itens,
        'ultima_saida': ultima_saida,
    })


@login_required
def criar_entrada(request):
    if request.method == 'POST':
        form = EntradaEstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrada criada com sucesso!')
            return redirect('movimentacoes:entradas')
    else:
        form = EntradaEstoqueForm()
    return render(request, 'movimentacoes/criar_entrada.html', {'form': form})


@login_required
def adicionar_item_entrada(request, entrada_pk):
    entrada = get_object_or_404(EntradaEstoque, pk=entrada_pk)
    if request.method == 'POST':
        form = EntradaItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.entrada = entrada
            item.save()
            messages.success(request, 'Item adicionado à entrada!')
            return redirect('movimentacoes:detalhe_entrada', pk=entrada_pk)
    else:
        form = EntradaItemForm()
    return render(request, 'movimentacoes/adicionar_item_entrada.html', {'form': form, 'entrada': entrada})


@login_required
def criar_saida(request):
    if request.method == 'POST':
        form = SaidaEstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saída criada com sucesso!')
            return redirect('movimentacoes:saidas')
    else:
        form = SaidaEstoqueForm()
    return render(request, 'movimentacoes/criar_saida.html', {'form': form})


@login_required
def adicionar_item_saida(request, saida_pk):
    saida = get_object_or_404(SaidaEstoque, pk=saida_pk)
    if request.method == 'POST':
        form = SaidaItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.saida = saida
            item.save()
            messages.success(request, 'Item adicionado à saída!')
            return redirect('movimentacoes:detalhe_saida', pk=saida_pk)
    else:
        form = SaidaItemForm()
    return render(request, 'movimentacoes/adicionar_item_saida.html', {'form': form, 'saida': saida})


@login_required
def deletar_entrada(request, pk):
    print(f"Método recebido: {request.method}")
    print(f"Headers: {request.headers}")
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    entrada = get_object_or_404(EntradaEstoque, pk=pk)
    entrada.delete()
    messages.success(request, 'Entrada excluída com sucesso!')
    return JsonResponse({'success': True, 'message': 'Entrada excluída com sucesso!'})


@login_required
def deletar_saida(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    saida = get_object_or_404(SaidaEstoque, pk=pk)
    saida.delete()
    messages.success(request, 'Saída excluída com sucesso!')
    return JsonResponse({'success': True, 'message': 'Saída excluída com sucesso!'})


@login_required
def detalhe_entrada(request, pk):
    entrada = get_object_or_404(EntradaEstoque, pk=pk)
    itens = entrada.itens.select_related('produto')
    return render(request, 'movimentacoes/detalhe_entrada.html', {'entrada': entrada, 'itens': itens})


@login_required
def detalhe_saida(request, pk):
    saida = get_object_or_404(SaidaEstoque, pk=pk)
    itens = saida.itens.select_related('produto')
    return render(request, 'movimentacoes/detalhe_saida.html', {'saida': saida, 'itens': itens})


@login_required
def editar_item_entrada(request, item_pk):
    item = get_object_or_404(EntradaItem, pk=item_pk)
    if request.method == 'POST':
        form = EntradaItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado!')
            return redirect('movimentacoes:detalhe_entrada', pk=item.entrada.id)
    else:
        form = EntradaItemForm(instance=item)
    return render(request, 'movimentacoes/editar_item_entrada.html', {'form': form, 'item': item})


@login_required
def editar_item_saida(request, item_pk):
    item = get_object_or_404(SaidaItem, pk=item_pk)
    if request.method == 'POST':
        form = SaidaItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado!')
            return redirect('movimentacoes:detalhe_saida', pk=item.saida.id)
    else:
        form = SaidaItemForm(instance=item)
    return render(request, 'movimentacoes/editar_item_saida.html', {'form': form, 'item': item})


@login_required
def deletar_item_entrada(request, item_pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    item = get_object_or_404(EntradaItem, pk=item_pk)
    entrada_id = item.entrada.id
    item.delete()
    messages.success(request, 'Item removido!')
    return JsonResponse({'success': True, 'entrada_id': entrada_id})


@login_required
def deletar_item_saida(request, item_pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    item = get_object_or_404(SaidaItem, pk=item_pk)
    saida_id = item.saida.id
    item.delete()
    messages.success(request, 'Item removido!')
    return JsonResponse({'success': True, 'saida_id': saida_id})


@login_required
def stock_report(request):
    # Relatório simples de estoque: lista produtos com quantidade e valor total por produto
    produtos = Produto.objects.select_related(
        'categoria', 'marca', 'fornecedor').all()
    produtos = produtos.annotate(valor_total=F(
        'estoque_atual') * F('preco_custo'))
    valor_geral = produtos.aggregate(
        total=Sum('valor_total', output_field=DecimalField()))['total'] or 0
    return render(request, 'movimentacoes/relatorio_estoque.html', {'produtos': produtos, 'valor_geral': valor_geral})


@login_required
def history(request):
    # Histórico combinado de entradas e saídas
    entradas = EntradaEstoque.objects.select_related(
        'fornecedor', 'usuario_responsavel').all().order_by('-data_entrada')
    saidas = SaidaEstoque.objects.select_related(
        'usuario_responsavel').all().order_by('-data_saida')
    return render(request, 'movimentacoes/historico.html', {'entradas': entradas, 'saidas': saidas})
