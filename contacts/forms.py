from django import forms

from .models import Contact

class ContactForm(forms.ModelForm):
	
	class Meta:
		model = Contact
		fields = ('name',)

class ContactSearchForm(forms.Form):

	name = forms.CharField(required=False, max_length=200)
