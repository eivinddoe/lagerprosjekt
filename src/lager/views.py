from django.shortcuts import render

from .forms import MvpForm

# Create your views here.
def main(request):
	if request.method == 'POST':
		form = MvpForm(request.POST)
		if form.is_valid():
			context = {
			'pris': form.cleaned_data['pris'],
			'leveringstid': form.cleaned_data['leveringstid'],
			'sist_byttet': form.cleaned_data['sist_byttet'],
			'levetid': form.cleaned_data['levetid'],
			'konsekvens': form.cleaned_data['konsekvens'],
			'form': form
			}
	else:
		form = MvpForm()
		context = {
		'form': form
		}	
	return render(request, "index.html", context)