from django.contrib import admin
from .models import Usuario


# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Colunas mostradas na lista de utilizadores
    list_display = ('nome', 'email_login', 'nivel', 'setor', 'is_active')
    # Filtros na barra lateral direita
    list_filter = ('nivel', 'is_active')
    # Campo de pesquisa no topo
    search_fields = ('nome', 'email_login')
