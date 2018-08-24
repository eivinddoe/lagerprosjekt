from django import forms
import datetime

class MvpForm(forms.Form):
	pris = forms.IntegerField(label='Pris')
	leveringstid = forms.IntegerField(label='Leveringstid')
	sist_byttet = forms.DateField(label='Sist byttet', initial=datetime.date.today)
	levetid = forms.IntegerField(label='Levetid')

	KONSEKVENSER = (
		("Driftsavbrudd", "Driftsavbrudd"),
		("Strømproduksjon", "Strømdproduksjon"),
		("Ingen avbrudd", "Ingen avbrudd"),
	)

	konsekvens = forms.ChoiceField(choices = KONSEKVENSER)