from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from usuarios.views import UsuarioLoginView


def home(request):
    return redirect("usuarios:dashboard")


class CustomLogoutView(auth_views.LogoutView):
    http_method_names = ['get', 'post']


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),

    # 🔥 ROTA GLOBAL /login/ CORRETA!
    path("login/", UsuarioLoginView.as_view(), name="login"),

    # 🔥 Logout funcionando corretamente
    path("logout/", CustomLogoutView.as_view(next_page='login'), name="logout"),

    # Rotas de usuários (sem incluir login aqui!)
    path("usuarios/", include(("usuarios.urls", "usuarios"), namespace="usuarios")),

    path("categorias/", include(("categorias.urls", "categorias"), namespace="categorias")),
    path("marcas/", include(("marcas.urls", "marcas"), namespace="marcas")),
    path("fornecedores/", include(("fornecedores.urls", "fornecedores"), namespace="fornecedores")),
    path("produtos/", include(("produtos.urls", "produtos"), namespace="produtos")),
    path("movimentacoes/", include(("movimentacoes.urls", "movimentacoes"), namespace="movimentacoes")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
