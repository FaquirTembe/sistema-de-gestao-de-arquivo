from django import forms
from .models import Expediente
 
 
class ExpedienteForm(forms.ModelForm):
    class Meta:
        model = Expediente
        # 'situacao', 'criado_por' e as datas NAO entram aqui -- sao geridos
        # automaticamente pelo sistema, nunca escritos directamente pelo utilizador.
        fields = ['numero', 'assunto', 'requerente', 'tipo', 'prioridade']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'assunto': forms.TextInput(attrs={'class': 'form-control'}),
            'requerente': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'prioridade': forms.Select(
                choices=[('NORMAL', 'Normal'), ('URGENTE', 'Urgente')],
                attrs={'class': 'form-select'},
            ),
        }
