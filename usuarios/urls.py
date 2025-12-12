from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("criar/", views.criar_usuario, name="criar"),
    path("editar/<int:id>/", views.editar_usuario, name="editar"),
    path("deletar/<int:id>/", views.deletar_usuario, name="deletar"),
    path("ver/<int:id>/", views.ver_usuario, name="ver"),
]
