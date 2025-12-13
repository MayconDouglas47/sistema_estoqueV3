from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria
from .forms import CategoriaForm


@login_required
def index(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'categorias/index.html', {'categorias': categorias})


@login_required
def criar(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('categorias:index')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/criar_categoria.html', {'form': form})


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
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria deletada com sucesso!')
        return redirect('categorias:index')
    return render(request, 'categorias/deletar_categoria.html', {'categoria': categoria})
