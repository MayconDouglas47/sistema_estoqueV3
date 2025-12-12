from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Fornecedor
from .forms import FornecedorForm


@login_required
def index(request):
    fornecedores = Fornecedor.objects.all().order_by('nome')
    return render(request, 'fornecedores/index.html', {'fornecedores': fornecedores})


@login_required
def criar(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor criado com sucesso!')
            return redirect('fornecedores:index')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedores/criar.html', {'form': form})


@login_required
def editar(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso!')
            return redirect('fornecedores:index')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'fornecedores/editar.html', {'form': form, 'fornecedor': fornecedor})


@login_required
def deletar(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        messages.success(request, 'Fornecedor deletado com sucesso!')
        return redirect('fornecedores:index')
    return render(request, 'fornecedores/deletar.html', {'fornecedor': fornecedor})
