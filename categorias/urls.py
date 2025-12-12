from django.urls import path
from . import views

app_name = "categorias"

urlpatterns = [
    path("", views.index, name="index"),
    path("criar/", views.criar, name="criar"),
    path("<int:pk>/editar/", views.editar, name="editar"),
    path("<int:pk>/deletar/", views.deletar, name="deletar"),
]
