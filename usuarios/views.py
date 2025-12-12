from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Sum, Count, F, DecimalField
from django.contrib import messages
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
def index(request):
    # Lista de usuários — apenas exibir usuários do sistema
    usuarios = Usuario.objects.all().order_by('nome')
    return render(request, 'usuarios/index.html', {'usuarios': usuarios})


@login_required(login_url='login')
def profile(request):
    # Mostrar perfil do usuário autenticado
    return render(request, 'usuarios/perfil.html', {'user': request.user})


@login_required(login_url='login')
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('usuarios:index')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/criar.html', {'form': form})


@login_required(login_url='login')
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuarios:index')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar.html', {'form': form, 'usuario': usuario})


@login_required(login_url='login')
def deletar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário deletado com sucesso!')
        return redirect('usuarios:index')
    return render(request, 'usuarios/deletar.html', {'usuario': usuario})


@login_required(login_url='login')
def ver_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    return render(request, 'usuarios/ver.html', {'usuario': usuario})
