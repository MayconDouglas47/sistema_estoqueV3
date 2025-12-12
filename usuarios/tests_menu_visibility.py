from django.test import TestCase, Client
from .models import Usuario


class MenuVisibilityTests(TestCase):
    def setUp(self):
        # criar usuários de teste
        Usuario.objects.create_superuser(
            'admin_test_ci', 'Pass@123', nome='Admin CI', nivel_acesso=Usuario.NIVEL_ADMIN)
        Usuario.objects.create_user(
            'estoq_test_ci', 'Pass@123', nome='Estoquista CI', nivel_acesso=Usuario.NIVEL_ESTOQUISTA)
        Usuario.objects.create_user(
            'caixa_test_ci', 'Pass@123', nome='Caixa CI', nivel_acesso=Usuario.NIVEL_CAIXA)
        self.client = Client()

    def test_admin_sees_all_sections(self):
        logged = self.client.login(login='admin_test_ci', password='Pass@123')
        self.assertTrue(logged)
        resp = self.client.get('/usuarios/dashboard/')
        content = resp.content.decode('utf-8')
        # Deve ver links essenciais (ver produtos / novos produtos / relatórios)
        self.assertIn('Usuários', content)
        self.assertIn('Ver Produtos', content)
        self.assertIn('Novo Produto', content)
        self.assertIn('Nova Entrada', content)
        self.assertIn('Relatório de estoque', content)

    def test_estoquista_sees_products_and_movements_but_not_users(self):
        logged = self.client.login(login='estoq_test_ci', password='Pass@123')
        self.assertTrue(logged)
        resp = self.client.get('/usuarios/dashboard/')
        content = resp.content.decode('utf-8')
        self.assertNotIn('Usuários', content)
        self.assertIn('Ver Produtos', content)
        self.assertIn('Nova Entrada', content)
        self.assertIn('Relatório de estoque', content)

    def test_caixa_sees_minimal(self):
        logged = self.client.login(login='caixa_test_ci', password='Pass@123')
        self.assertTrue(logged)
        resp = self.client.get('/usuarios/dashboard/')
        content = resp.content.decode('utf-8')
        # Caixa não deve ver usuários, atalhos de produtos ou relatórios
        self.assertNotIn('Usuários', content)
        self.assertNotIn('Ver Produtos', content)
        self.assertNotIn('Novo Produto', content)
        self.assertNotIn('Relatório de estoque', content)
        # Dashboard título sempre disponível
        self.assertIn('Dashboard', content)
