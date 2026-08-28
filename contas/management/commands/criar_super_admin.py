from getpass import getpass
from django.core.management.base import BaseCommand
from contas.models import Usuario

class Command(BaseCommand):
    help = 'Cria o primeiro utilizador Super Admin do sistema.'
 
    def handle(self, *args, **options):
        nome = input('Nome completo: ')
        email_login = input('E-mail de acesso: ')
        senha = getpass('Palavra-passe: ')          # nao aparece no ecra
        confirmar = getpass('Confirmar palavra-passe: ')
 
        if senha != confirmar:
            self.stderr.write('As palavras-passe nao coincidem. Tenta outra vez.')
            return
 
        if Usuario.objects.filter(email_login=email_login).exists():
            self.stderr.write('Ja existe um utilizador com este e-mail.')
            return
 
        Usuario.objects.create_superuser(email_login, nome, senha)
        self.stdout.write(self.style.SUCCESS(
            f'Super Admin "{nome}" criado com sucesso!'
        ))
