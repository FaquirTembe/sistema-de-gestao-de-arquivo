from django.test import TestCase
from .models import Usuario
 
 
class UsuarioModelTestCase(TestCase):
    def test_password_nunca_fica_em_texto_simples(self):
        usuario = Usuario.objects.create_user(
            'teste@teste.com', 'Nome Teste', 'senhaSegura123'
        )
        # O campo 'password' guardado na BD NUNCA deve ser igual
                # ao texto original -- deve estar 'transformado' em hash.
        self.assertNotEqual(usuario.password, 'senhaSegura123')
        # Mas check_password() deve continuar a reconhecer a password certa:
        self.assertTrue(usuario.check_password('senhaSegura123'))
        self.assertFalse(usuario.check_password('senhaErrada'))
 
    def test_niveis_de_acesso(self):
        super_admin = Usuario.objects.create_user('sa@t.com', 'SA', 'x123456789', nivel=1)
        operador = Usuario.objects.create_user('op@t.com', 'Op', 'x123456789', nivel=3)
        self.assertTrue(super_admin.eh_super_admin)
        self.assertFalse(operador.eh_super_admin)
