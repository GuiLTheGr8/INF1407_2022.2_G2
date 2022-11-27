from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def homepage(request):

    getDay = datetime.date.today()
    getTime = datetime.datetime.now()

    dia = getDay.strftime("%d/%m/%Y")
    horas = getTime.hour
    minutos = getTime.minute
    segundos = getTime.second

    if horas < 12:
        cumprimento = "Bom dia!"
    elif horas < 18:
        cumprimento = "Boa tarde!"
    else:
        cumprimento = "Boa noite!"

    context = {'dia': dia, 'horas': horas, 'minutos': minutos, 'segundos': segundos, 'cumprimento': cumprimento}
    return render(request, 'ExemplosWeb/index.html', context)

def homeSec(request):
    return render (request, 'registro/homeSec.html')

def registro(request):
    if request.method == 'POST':
        # cria o usuário no banco de dados
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('sec-home')
        else:
          context = {'form': formulario, }
        return render(request, 'registro/registro.html', context)
    else:
        # exibe o formulário para criar o usuário
        formulario = UserCreationForm()
    context = {'form': formulario, }
    return render(request, 'registro/registro.html', context)

@login_required
def secreto(request):
    return render(request, 'particular/paginaSecreta.html')