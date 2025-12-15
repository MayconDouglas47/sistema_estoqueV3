from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Sum, Count, F, DecimalField
from django.contrib import messages
from django.http import JsonResponse
from produtos.models import Produto
from movimentacoes.models import EntradaEstoque, SaidaEstoque
from .models import Usuario
from .forms import UsuarioForm


class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('usuarios:dashboard')


@login_required(login_url='login')
def dashboard(request):
    # Alertas de estoque mínimo
    estoque_baixo = Produto.objects.filter(
        estoque_atual__lte=F('estoque_minimo')
    ).select_related('categoria').order_by('estoque_atual')[:10]

    # Stats de produtos
    total_produtos = Produto.objects.count()
    produtos_zerados = Produto.objects.filter(estoque_atual=0).count()
    valor_total_estoque = Produto.objects.aggregate(
        total=Sum(F('estoque_atual') * F('preco_custo'),
                  output_field=DecimalField())
    )['total'] or 0

    # Stats de movimentacoes
    total_entradas = EntradaEstoque.objects.count()
    total_saidas = SaidaEstoque.objects.count()

    # Categorias com mais produtos
    categorias_top = Produto.objects.values('categoria__nome').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    context = {
        'estoque_baixo': estoque_baixo,
        'total_produtos': total_produtos,
        'produtos_zerados': produtos_zerados,
        'valor_total_estoque': valor_total_estoque,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'categorias_top': categorias_top,
    }
    return render(request, 'usuarios/dashboard.html', context)


@login_required(login_url='login')
def profile(request):
    usuario = request.user
    return render(request, 'usuarios/perfil.html', {'usuario': usuario})


@login_required(login_url='login')
def index(request):
    from django.core.paginator import Paginator
    from django.db.models import Case, When, Value, IntegerField

    # Ordenar: Admin > Estoquista > Caixa
    usuarios_list = Usuario.objects.all().annotate(
        role_order=Case(
            When(nivel_acesso='admin', then=Value(0)),
            When(nivel_acesso='estoquista', then=Value(1)),
            When(nivel_acesso='caixa', then=Value(2)),
            output_field=IntegerField()
        )
    ).order_by('role_order', 'nome')

    paginator = Paginator(usuarios_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'usuarios/index.html', {
        'usuarios': usuarios_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


@login_required(login_url='login')
def detalhe(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/detalhe.html', {'usuario': usuario})


@login_required(login_url='login')
def criar_usuario(request):
    # Detecta se a requisição veio via AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')

            if is_ajax:
                return JsonResponse({'success': True, 'message': 'Usuário criado com sucesso!'})
            else:
                return redirect('usuarios:index')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # Se não for POST, retorna erro ou redireciona
    return redirect('usuarios:index')


@login_required(login_url='login')
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    # Detecta se a requisição veio via AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            # Proteção extra: garantir que admin sempre permaneça ativo
            user_obj = form.save(commit=False)
            if user_obj.nivel_acesso == Usuario.NIVEL_ADMIN:
                user_obj.is_active = True
            user_obj.save()
            messages.success(request, 'Usuário atualizado com sucesso!')

            if is_ajax:
                return JsonResponse({'success': True, 'message': 'Usuário atualizado com sucesso!'})
            else:
                return redirect('usuarios:index')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # Se não for POST, redireciona para index
    return redirect('usuarios:index')


@login_required(login_url='login')
def deletar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    # Impedir exclusão de usuários admin
    if usuario.nivel_acesso == Usuario.NIVEL_ADMIN:
        messages.error(
            request, 'Usuários administradores não podem ser excluídos!')
        return redirect('usuarios:index')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('usuarios:index')
    return render(request, 'usuarios/deletar.html', {'usuario': usuario})


@login_required(login_url='login')
def atualizar_avatar(request, pk):
    """Atualiza o avatar do usuário via AJAX"""
    usuario = get_object_or_404(Usuario, pk=pk)

    # Apenas o próprio usuário ou admin pode atualizar o avatar
    if request.user != usuario and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Sem permissão'}, status=403)

    if request.method == 'POST':
        avatar = request.POST.get('avatar')
        if avatar in ['homem', 'mulher']:
            usuario.avatar = avatar
            usuario.save()
            return JsonResponse({'success': True, 'avatar': avatar})

    return JsonResponse({'success': False, 'error': 'Requisição inválida'}, status=400)
