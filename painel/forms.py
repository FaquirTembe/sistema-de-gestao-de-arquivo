from django import forms
from django.contrib.auth import get_user_model
 
Usuario = get_user_model()
 
 
class UsuarioAdminForm(forms.ModelForm):
    """Formulário usado pelo Super Admin para criar ou editar uma conta.
    A password é tratada à parte (ver views.py) porque nunca deve ser
    gravada em texto simples nem exigida ao editar (deixar em branco =
    'não mudar a password')."""
 
    nova_senha = forms.CharField(
        label='Nova password (deixe em branco para não alterar)',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
    )
 
    class Meta:
        model = Usuario
        fields = ['nome', 'email_login', 'nivel', 'setor', 'is_active']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email_login': forms.EmailInput(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
