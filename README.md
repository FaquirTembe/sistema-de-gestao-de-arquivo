# sistema-de-gestao-de-arquivo
Um Sistema de Gestão de Expedientes dotado de um mecanismo robusto de Controlo de Acesso Baseado em Papéis (RBAC), capaz de automatizar o registo, a tramitação, o despacho e o arquivo de processos administrativos, assegurando a confidencialidade, a integridade e a rastreabilidade da informação.

# SGE-Mandlakazi
Sistema de Gestao de Expedientes com Controlo de Acesso Baseado em
Papeis (RBAC), desenvolvido em Django + PostgreSQL.
 
## Requisitos
- Python 3.11+
- PostgreSQL 14+
- Git
 
## Como instalar e correr localmente
 
1. Clonar o repositorio:
   git clone https://github.com/FaquirTembe/sistema-de-gestao-de-arquivo.git
   cd sistema-de-gestao-de-arquivo
 
2. Criar e activar o ambiente virtual:
   python -m venv .venv
   source .venv/bin/activate   (Windows: .venv\Scripts\activate)
 
3. Instalar as dependencias:
   pip install -r requirements.txt
 
4. Criar a base de dados PostgreSQL (ver Fase 1 do guiao de implementacao):
   CREATE DATABASE sge_mandlakazi;
 
5. Copiar .env.example para .env e preencher com as tuas credenciais:
   cp .env.example .env
 
6. Aplicar as migracoes:
   python manage.py migrate
 
7. Criar o primeiro Super Admin:
   python manage.py criar_super_admin
 
8. Iniciar o servidor:
   python manage.py runserver
   Aceder a http://127.0.0.1:8000/contas/entrar/
 
## Correr os testes
   python manage.py test
 
## Estrutura das apps
- contas: utilizadores e RBAC (3 niveis)
- expedientes: registo, tramitacao, despacho e arquivo
- documentos: upload/download seguro de anexos
- auditoria: trilha de auditoria e relatorios PDF/Excel
- comum: mixins de permissao partilhados entre apps

