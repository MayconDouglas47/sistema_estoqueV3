from django.urls import path
from . import views

app_name = "movimentacoes"

urlpatterns = [
    path("", views.index, name="index"),
    path("entradas/", views.entradas, name="entradas"),
    path("saidas/", views.saidas, name="saidas"),
    path("relatorios/estoque/", views.stock_report, name="stock_report"),
    path("relatorios/historico/", views.history, name="history"),
    path("entradas/criar/", views.criar_entrada, name="criar_entrada"),
    path("entradas/<int:pk>/deletar/",views.deletar_entrada, name="deletar_entrada"),
    path("saidas/criar/", views.criar_saida, name="criar_saida"),
    path("saidas/<int:pk>/deletar/", views.deletar_saida, name="deletar_saida"),
    path("entradas/<int:entrada_pk>/itens/adicionar/", views.adicionar_item_entrada, name="adicionar_item_entrada"),
    path("saidas/<int:saida_pk>/itens/adicionar/", views.adicionar_item_saida, name="adicionar_item_saida"),
    path("entradas/<int:pk>/", views.detalhe_entrada, name="detalhe_entrada"),
    path("saidas/<int:pk>/", views.detalhe_saida, name="detalhe_saida"),
    path("itens/entrada/<int:item_pk>/editar/", views.editar_item_entrada, name="editar_item_entrada"),
    path("itens/entrada/<int:item_pk>/deletar/", views.deletar_item_entrada, name="deletar_item_entrada"),
    path("itens/saida/<int:item_pk>/editar/", views.editar_item_saida, name="editar_item_saida"),
    path("itens/saida/<int:item_pk>/deletar/", views.deletar_item_saida, name="deletar_item_saida"),
]
