# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms import widgets
from django.forms import ModelForm, Select, Textarea

from django import forms


from .models import Alert

class AlertForm(forms.ModelForm):
	main_category = forms.CharField(label="Tipo de carro", required=False, widget=forms.Select(choices=[]))
	brand = forms.CharField(label="Marca", required=False, widget=forms.Select(choices=[]))
	model = forms.CharField(label="Linea", required=False, widget=forms.Select(choices=[]))
	location = forms.CharField(label="Departamento", required=False, widget=forms.Select(choices=[]))

	class Meta:
		model = Alert
		fields = ['main_category','brand','model','year_min','year_max','price_min','price_max','location']
		labels = {
			'main_category': _('Tipo de carro'),
			'brand': _('Marca'),
			'model': _('Linea'),
            'location': _('Departamento'),
            'year_min': _('Modelo'),
            'year_max': _(''),
            'price_min': _('Precio en $'),
            'price_max': _(''),
            #'mileage': _('Kilometraje'),
        }

	def clean_price_min(self):
		price_min=self.cleaned_data.get('price_min')
		return price_min

	def clean_price_max(self):
		price_min=self.cleaned_data.get('price_min')
		price_max=self.cleaned_data.get('price_max')
		if int(price_min)>=int(price_max):
			price_max=price_min
			raise forms.ValidationError("Este valor debe ser mayor o igual que el anterior")
		return price_max

	def clean_year_max(self):
		year_min=self.cleaned_data.get('year_min')
		year_max=self.cleaned_data.get('year_max')
		if int(year_min)>=int(year_max):
			year_max=year_min
			raise forms.ValidationError("Este valor debe ser mayor o igual que el anterior")
		return year_max


    
