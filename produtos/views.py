from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    return render(request, 'produtos/criar.html', {'form': form})


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
    return render(request, 'produtos/editar.html', {'form': form, 'produto': produto})


@login_required
def deletar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto deletado com sucesso!')
        return redirect('produtos:index')
    return render(request, 'produtos/deletar.html', {'produto': produto})
