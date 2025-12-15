# Inclui 'redirect' novamente
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Fornecedor
from .forms import FornecedorForm
from produtos.models import Produto


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def index(request):
    fornecedores_list = Fornecedor.objects.all().order_by('id')
    paginator = Paginator(fornecedores_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fornecedores/index.html', {
        'fornecedores': fornecedores_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


@login_required
@user_passes_test(is_admin)
def criar(request):
    # Detecta se a requisição veio via AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor criado com sucesso!')

            if is_ajax:
                # 1. Resposta AJAX: Sucesso.
                return JsonResponse({'success': True, 'message': 'Fornecedor criado com sucesso!'})
            else:
                # 2. Resposta Padrão (PRG): Redireciona para evitar reenvio (Correção!)
                return redirect('fornecedores:index')
        else:
            if is_ajax:
                # 3. Erro AJAX: Retorna erros do formulário e status 400.
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = FornecedorForm()

    return render(request, 'fornecedores/criar_fornecedor.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def editar(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    # Detecta se a requisição veio via AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso!')

            if is_ajax:
                # 1. Resposta AJAX: Sucesso.
                return JsonResponse({'success': True, 'message': 'Fornecedor atualizado com sucesso!'})
            else:
                # 2. Resposta Padrão (PRG): Redireciona para evitar reenvio (Correção!)
                return redirect('fornecedores:index')
        else:
            if is_ajax:
                # 3. Erro AJAX: Retorna erros do formulário e status 400.
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = FornecedorForm(instance=fornecedor)

    return render(request, 'fornecedores/editar_fornecedor.html', {
        'form': form,
        'fornecedor': fornecedor
    })


@login_required
@user_passes_test(is_admin)
def deletar(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    possui_produtos = Produto.objects.filter(fornecedor=fornecedor).exists()

    # Verificação prévia (antes do modal)
    if request.headers.get('X-Check-Only') == 'true':
        return JsonResponse({'can_delete': not possui_produtos})

    # Exclusão definitiva
    if possui_produtos:
        messages.error(
            request, 'Não é possível excluir este fornecedor pois existem produtos associados a ele.')
        return JsonResponse({
            'success': False,
            'message': 'Fornecedor possui produtos associados. Não pode ser excluído.'
        }, status=400)

    nome_fornecedor = fornecedor.nome
    fornecedor.delete()
    messages.success(request, 'Fornecedor excluído com sucesso!')
    return JsonResponse({'success': True, 'message': 'Fornecedor excluído com sucesso!'})
