# -*- coding: utf-8 -*-

# from django.forms import inlineformset_factory, modelformset_factory, BaseModelFormSet
# from django.forms.util import ErrorList , ErrorDict
# from django.forms.models import ModelMultipleChoiceField
# from django.forms import ModelForm, BaseInlineFormSet
# from django.forms import ModelForm, CharField
# from django.forms.widgets import HiddenInput, TextInput
#
# from solr_front.models import FnSearch
#
#
# class FnSearchForm(ModelForm):
#     class Meta:
#         model = FnSearch
#         exclude = []


from django.forms import ModelForm
from solr_front.models import *
from django import forms

class PesquisaForm(ModelForm):
    class Meta:
        model = Pesquisa
        fields = "__all__"

class ExportaCsvForm(forms.Form):

    name= forms.CharField(label='Seu nome', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email_from = forms.EmailField(label='Seu email',widget=forms.TextInput(attrs={'class':'form-control'}))
    email_to = forms.CharField(label='Para (Email)', help_text="Exemplo: nome@exemplo.com. Caso queira incluir mais de uma pessoa, separe os endereços de e-mail por vírgulas.", max_length=2000,widget=forms.TextInput(attrs={'class':'form-control'}))
    comentario = forms.CharField(required=False, label='Comentário', max_length=15000, widget=forms.Textarea(attrs={'rows':4, 'class':'form-control' ,'placeholder': 'Digite algum mensagem no email email enviado'}))

class ExportForm(forms.Form):

    FORMAT_CHOICES = (
    ('csv', 'CSV'),
    ('json', 'JSON'),
    ('excel', 'MS Excel')
    )
    name= forms.CharField(label='Seu nome', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email_from = forms.EmailField(label='Seu email',widget=forms.TextInput(attrs={'class':'form-control'}))
    email_to = forms.CharField(label='Para (Email)', help_text="Exemplo: nome@exemplo.com. Caso queira incluir mais de uma pessoa, separe os endereços de e-mail por vírgulas.", max_length=2000,widget=forms.TextInput(attrs={'class':'form-control'}))
    comentario = forms.CharField(required=False, label='Comentário', max_length=15000, widget=forms.Textarea(attrs={'rows':4, 'class':'form-control' ,'placeholder': 'Digite algum mensagem no email email enviado'}))
    formato = forms.ChoiceField(
        required=True,
        choices=FORMAT_CHOICES,
    )
