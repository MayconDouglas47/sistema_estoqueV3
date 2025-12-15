from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Categoria
from .forms import CategoriaForm


@login_required
def index(request):
    categorias_list = Categoria.objects.all().order_by('id')
    paginator = Paginator(categorias_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categorias/index.html', {
        'categorias': categorias_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


@login_required
def criar(request):
    # Detecta se a requisição veio via AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')

            if is_ajax:
                return JsonResponse({'success': True, 'message': 'Categoria criada com sucesso!'})
            else:
                return redirect('categorias:index')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # Se não for POST, redireciona para index
    return redirect('categorias:index')


@login_required
def editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categorias:index')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/editar_categoria.html', {'form': form, 'categoria': categoria})


@login_required
def deletar(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    categoria = get_object_or_404(Categoria, pk=pk)
    nome_categoria = categoria.nome
    categoria.delete()
    messages.success(request, 'Categoria excluída com sucesso!')
    return JsonResponse({'success': True, 'message': 'Categoria excluída com sucesso!'})
