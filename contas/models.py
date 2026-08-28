from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.
class UsuarioManager(BaseUserManager):
    """
    Um 'Manager' e a classe responsavel por CRIAR objectos.
    Sem isto, o Django nao saberia como criar um Usuario 'a nossa maneira'
    (por exemplo, como aplicar o hash da password automaticamente).
    """
 
    def create_user(self, email_login, nome, senha=None, nivel=3):
        # 1) Validar que o email/login foi mesmo fornecido
        if not email_login:
            raise ValueError('O utilizador precisa de um identificador de acesso.')
 
        # 2) Criar o objecto Usuario em memoria (ainda nao gravado na BD)
        usuario = self.model(
            email_login=self.normalize_email(email_login),
            nome=nome,
            nivel=nivel,
        )
 
        # 3) set_password() e um metodo magico herdado do Django:
        #    ele NUNCA grava a password tal como foi escrita -- aplica
        #    um algoritmo de 'hash' (uma funcao matematica que so anda
        #    num sentido: e facil confirmar 'e esta a password certa?',
        #    mas impossivel descobrir a password original a partir do hash).
        usuario.set_password(senha)
 
        # 4) So agora gravamos mesmo na base de dados
        usuario.save(using=self._db)
        return usuario
 
    def create_superuser(self, email_login, nome, senha=None):
        """Usado pelo comando 'criar_super_admin' que escrevemos no Passo 5."""
        usuario = self.create_user(email_login, nome, senha, nivel=1)
        usuario.is_staff = True       # permite entrar no /admin/ do Django
        usuario.is_superuser = True   # ignora verificacoes de permissao especificas
        usuario.save(using=self._db)
        return usuario
 
 
class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    O nosso utilizador. Herda de duas classes do Django:
    - AbstractBaseUser: da-nos a gestao segura de password e de login;
    - PermissionsMixin: da-nos o sistema de permissoes usado no /admin/.
    """
 
    # Os 3 'craches' do nosso predio (ver analogia acima).
    # Reparar que sao NUMEROS: quanto MENOR o numero, MAIOR o poder.
    NIVEL_SUPER_ADMIN = 1
    NIVEL_ADMIN = 2
    NIVEL_OPERADOR = 3
 
    NIVEL_CHOICES = [
        (NIVEL_SUPER_ADMIN, 'Super Admin (Acesso Total)'),
        (NIVEL_ADMIN, 'Administrador (Gestao de Expedientes)'),
        (NIVEL_OPERADOR, 'Operador (Apenas os Proprios Expedientes)'),
    ]
 
    nome = models.CharField(max_length=150)
    email_login = models.EmailField(max_length=190, unique=True)
    nivel = models.PositiveSmallIntegerField(
        choices=NIVEL_CHOICES, default=NIVEL_OPERADOR
    )
    setor = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)   # False = conta desactivada
    is_staff = models.BooleanField(default=False)    # True = pode entrar no /admin/
    criado_em = models.DateTimeField(auto_now_add=True)
 
    objects = UsuarioManager()   # liga o nosso Manager a este modelo
 
    USERNAME_FIELD = 'email_login'   # diz ao Django: 'o login e por AQUI'
    REQUIRED_FIELDS = ['nome']       # pedido extra ao criar superuser via terminal
 
    class Meta:
        verbose_name = 'Utilizador'
        verbose_name_plural = 'Utilizadores'
 
    def __str__(self):
        # Isto e o que aparece no /admin/ do Django, em vez de 'Usuario object (1)'
        return f'{self.nome} ({self.get_nivel_display()})'
 
    @property
    def eh_super_admin(self):
        return self.nivel == self.NIVEL_SUPER_ADMIN
 
    @property
    def eh_admin(self):
        # 'in' verifica se o nivel esta dentro da lista -- super admin
        # tambem conta como admin, porque tem mais poder, nao menos.
        return self.nivel in (self.NIVEL_SUPER_ADMIN, self.NIVEL_ADMIN)
