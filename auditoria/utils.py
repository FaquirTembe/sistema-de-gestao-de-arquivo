import logging
from .models import LogAuditoria
 
# Um 'logger' do Python escreve tambem para um FICHEIRO em disco --
# uma segunda fonte de verdade, independente da base de dados.
# Se algum dia a base de dados for adulterada, o ficheiro de log
# continua a contar a verdade.
logger = logging.getLogger('auditoria')
 
 
def obter_ip(request):
    """O endereco IP normalmente vem em REMOTE_ADDR, mas se o site
    estiver atras de um proxy/load-balancer, vem em X-Forwarded-For."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
 
 
def registar(request, accao, modelo, objecto_id, descricao):
    """Chamada a partir de QUALQUER view do sistema que faca algo sensivel."""
    ip = obter_ip(request)
 
    LogAuditoria.objects.create(
        utilizador=request.user if getattr(request, 'user', None) and request.user.is_authenticated else None,        
        accao=accao, modelo=modelo, objecto_id=str(objecto_id),
        descricao=descricao, endereco_ip=ip,
    )
 
    logger.info(
        '%s | user=%s | %s | %s#%s | ip=%s',
         accao, getattr(getattr(request, 'user', None), 'email_login', 'anonimo'),
        descricao, modelo, objecto_id, ip,
    )
