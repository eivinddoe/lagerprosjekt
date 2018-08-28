from datetime import datetime, timedelta
from django.shortcuts import render

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import math
import numpy as np

from .forms import MvpForm

# Create your views here.
def main(request):
    lagerkost = 0.05
    today = datetime.today().date()
    context = {
	'today': today
	}
    if request.method == 'POST':
        form = MvpForm(request.POST)
        if form.is_valid():
            levetid_dager = form.cleaned_data['levetid'] * 365
            tid_inne = (today-form.cleaned_data['sist_byttet']).days
            konsekvens = form.cleaned_data['konsekvens']
            pris = form.cleaned_data['pris']
            lagerkost_dag = pris * lagerkost/365

            context.update({
            'pris': pris,
            'lagerkost_dag': lagerkost_dag,
            'leveringstid': form.cleaned_data['leveringstid'],
            'leveringstid_dager': form.cleaned_data['leveringstid'] * 7,
            'sist_byttet': form.cleaned_data['sist_byttet'],
            'tid_inne': tid_inne,
            'levetid': form.cleaned_data['levetid'],
            'levetid_dager': levetid_dager,
            'konsekvens': form.cleaned_data['konsekvens'],
            'form': form,
            'analyse': True
            })
            
            # Function to compute Weibull cumulative density function
            def WeibullCDF(x, lmbd, k):
                q = pow(x/lmbd, k)
                return 1.0 - math.exp(-q)
            
            # Beregne vektet risiko (nedetidskostnad)
            if konsekvens == 'Driftsavbrudd':
            	nedetidskostnad_dag = 550000
            elif konsekvens == 'Strømproduksjon':
            	nedetidskostnad_dag = 107000
            else:
            	nedetidskostnad_dag = 0

            if tid_inne >= levetid_dager:
            	context.update({
            		'levetid_lager': True
            		})
            	if konsekvens != 'Ingen avbrudd':
            		context.update({
            			'kritisk': True
            			})
            else:
                cdf_start = WeibullCDF(tid_inne, levetid_dager, 5)
                survival = 1-cdf_start
            
                probabilities = []
                for i in range(tid_inne + 1, levetid_dager + 1):
                    probabilities.append((WeibullCDF(i, levetid_dager, 5)-cdf_start)/survival)

                vektet_risiko = [i * nedetidskostnad_dag for i in probabilities]
            
                context.update({
                    'cdf_start': cdf_start,
                    'vektet_risiko': vektet_risiko
            	    })

                # Beregne vektet lagerkostnad
                probabilities_complement = [(1-i) for i in probabilities]
                vektet_lagerkost_dag = [i * lagerkost_dag for i in probabilities_complement]
                vektet_lagerkost = []
                for i in range(1,len(vektet_lagerkost_dag)+1):
                    vektet_lagerkost.append(i * vektet_lagerkost_dag[i-1])

                context.update({
                    'vektet_lagerkost': vektet_lagerkost
                    })

                # Finn kritisk dag
                if konsekvens != 'Ingen avbrudd':
                    i = 0
                    if vektet_risiko[i] > vektet_lagerkost[i]:
                	    kritisk_dato = today + timedelta(days=i)
                	    ontext.update({
                        'kritisk_dag': i,
                        'kritisk_dato': kritisk_dato,
                        'kritisk': True
                        })
                    else:
                        #while vektet_risiko[i] < vektet_lagerkost[i]:
                        #    i += 1
                        for i in range(0, len(vektet_risiko)):
                    	    lagerhold = vektet_risiko[i] > vektet_lagerkost[i]
                    	    if lagerhold:
                    		    i = i
                    		    break

                        kritisk_dato = today + timedelta(days=i)
    
                        context.update({
                        'kritisk_dag': i,
                        'kritisk_dato': kritisk_dato,
                        'kritisk': True
                        })



    else:
        form = MvpForm()
        context = {
        'form': form
        }
    return render(request, "index.html", context)