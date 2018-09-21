from django import forms
from .models import College


class CollegeForm(forms.ModelForm):
	class Meta:
		model = College
		fields = ['name', 'average_cost', 'location', 'website']
		help_texts = {'average_cost': 'Enter the cost in lakhs'}