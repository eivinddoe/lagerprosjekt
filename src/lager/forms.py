from bootstrap_datepicker_plus import DatePickerInput
from django import forms
import datetime

class MvpForm(forms.Form):
	pris = forms.IntegerField(label='Pris')
	leveringstid = forms.IntegerField(label='Leveringstid (uker)')
	sist_byttet = forms.DateField(label='Sist byttet', input_formats=['%d/%m/%Y'],
		widget=DatePickerInput(format='%d/%m/%Y'))
	levetid = forms.IntegerField(label='Levetid (år)')

	KONSEKVENSER = (
		("Driftsavbrudd", "Driftsavbrudd"),
		("Strømproduksjon", "Strømproduksjon"),
		("Ingen avbrudd", "Ingen avbrudd"),
	)

	konsekvens = forms.ChoiceField(choices = KONSEKVENSER)