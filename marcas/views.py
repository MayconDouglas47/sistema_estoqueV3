from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Marca
from .forms import MarcaForm
from produtos.models import Produto


@login_required
def index(request):
    marcas_list = Marca.objects.all().order_by('id')
    paginator = Paginator(marcas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'marcas/index.html', {
        'marcas': marcas_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


@login_required
def criar(request):
    # Detecta se a requisição veio via AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca criada com sucesso!')

            if is_ajax:
                return JsonResponse({'success': True, 'message': 'Marca criada com sucesso!'})
            else:
                return redirect('marcas:index')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # Se não for POST, redireciona para index
    return redirect('marcas:index')


@login_required
def editar(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca atualizada com sucesso!')
            return redirect('marcas:index')
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'marcas/editar_marca.html', {'form': form, 'marca': marca})


@login_required
def deletar(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    marca = get_object_or_404(Marca, pk=pk)
    possui_produtos = Produto.objects.filter(marca=marca).exists()

    # Verificação prévia (antes do modal)
    if request.headers.get('X-Check-Only') == 'true':
        return JsonResponse({'can_delete': not possui_produtos})

    # Exclusão definitiva
    if possui_produtos:
        messages.error(
            request, 'Não é possível excluir esta marca pois existem produtos associados a ela.')
        return JsonResponse({
            'success': False,
            'message': 'Marca possui produtos associados. Não pode ser excluída.'
        }, status=400)

    nome_marca = marca.nome
    marca.delete()
    messages.success(request, 'Marca excluída com sucesso!')
    return JsonResponse({'success': True, 'message': 'Marca excluída com sucesso!'})
