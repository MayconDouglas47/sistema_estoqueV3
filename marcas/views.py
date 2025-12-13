from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Marca
from .forms import MarcaForm


@login_required
def index(request):
    marcas = Marca.objects.all().order_by('nome')
    return render(request, 'marcas/index.html', {'marcas': marcas})


@login_required
def criar(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca criada com sucesso!')
            return redirect('marcas:index')
    else:
        form = MarcaForm()
    return render(request, 'marcas/criar_marca.html', {'form': form})


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
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        messages.success(request, 'Marca deletada com sucesso!')
        return redirect('marcas:index')
    return render(request, 'marcas/deletar_marca.html', {'marca': marca})
