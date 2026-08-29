from django.contrib import admin
from .models import LogAuditoria
 
 
@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('criado_em', 'utilizador', 'accao', 'modelo', 'objecto_id')
    list_filter = ('accao', 'modelo')
    search_fields = ('descricao',)
    # Ninguem pode EDITAR nem APAGAR um registo de auditoria -- so ler.
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
