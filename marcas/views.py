# marca/views.py (MODIFICADO)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse # IMPORTAÇÃO ADICIONADA
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
    
    # Se a requisição for POST (vindo do modal de confirmação)
    if request.method == 'POST':
        try:
            marca.delete()
            messages.success(request, 'Marca excluída com sucesso!')
            
            # Resposta para o JavaScript (Fetch)
            return JsonResponse({'success': True}) 
        except Exception as e:
            # Em caso de erro (ex: chave estrangeira, itens relacionados)
            # Retornamos uma resposta JSON de falha
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    # Se a requisição não for POST, retorne erro 405 (o template deletar_marca.html não é mais usado)
    return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)