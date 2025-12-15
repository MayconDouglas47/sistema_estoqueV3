# categoria/views.py (MODIFICADO)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse # IMPORTAÇÃO ADICIONADA
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
    
    # Se a requisição for POST (vindo do modal de confirmação)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoria excluída com sucesso!')
            
            # Resposta para o JavaScript (Fetch)
            return JsonResponse({'success': True}) 
        except Exception as e:
            # Em caso de erro (ex: chave estrangeira, itens relacionados)
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    # Se a requisição não for POST, retorne erro 405 (o template deletar_categoria.html não é mais usado)
    return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)