from django.test import TestCase
from django.urls import reverse
from contas.models import Usuario
from .models import Expediente
 
 
class RBACExpedienteTestCase(TestCase):
    """
    TestCase e uma 'caixa de testes' do Django: cada metodo comecado
    por 'test_' e um teste independente, e a base de dados e limpa
    automaticamente entre cada um -- nunca 'suja' dados reais.
    """
 
    def setUp(self):
        # Corre ANTES de cada teste: prepara os dados de que vamos precisar.
        self.operador1 = Usuario.objects.create_user(
            'operador1@teste.com', 'Operador Um', 'senhaSegura123', nivel=3
        )
        self.operador2 = Usuario.objects.create_user(
            'operador2@teste.com', 'Operador Dois', 'senhaSegura123', nivel=3
        )
        self.expediente = Expediente.objects.create(
            numero='EXP-0001', assunto='Teste', requerente='Fulano',
            tipo='Geral', criado_por=self.operador1,
        )
 
    def test_operador_ve_o_proprio_expediente(self):
        self.client.force_login(self.operador1)
        resposta = self.client.get(reverse('expedientes:ver', args=[self.expediente.id]))
        self.assertEqual(resposta.status_code, 200)   # 200 = OK
 
    def test_operador_NAO_ve_expediente_alheio(self):
        # Este e O teste mais importante de todo o projecto: confirma
                # que o RBAC de facto impede o acesso indevido.
        self.client.force_login(self.operador2)
        resposta = self.client.get(reverse('expedientes:ver', args=[self.expediente.id]))
        self.assertEqual(resposta.status_code, 403)   # 403 = Acesso Negado
 
    def test_anonimo_e_redireccionado_para_login(self):
        # 'self.client' sem force_login simula um visitante sem sessao
        resposta = self.client.get(reverse('expedientes:ver', args=[self.expediente.id]))
        self.assertEqual(resposta.status_code, 302)   # 302 = redireccionamento
