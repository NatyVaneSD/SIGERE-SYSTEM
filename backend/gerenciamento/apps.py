from django.apps import AppConfig


class GerenciamentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gerenciamento'

from django import forms


class ContactForm(forms.Form):
    error_css_class = "error"
    required_css_class = "required"