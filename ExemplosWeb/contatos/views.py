from django.shortcuts import render, get_object_or_404
from contatos.models import Pessoa
from django.views.generic.base import View
from contatos.forms import ContatoModel2Form
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls.base import reverse_lazy
import json
from django.views.decorators.http import require_GET

# Create your views here.

class ContatoListView(View):
    def get(self, request, *args, **kwargs):
        pessoas = Pessoa.objects.all()
        context = { 'pessoas': pessoas, }
        return render(request, 'contatos/listaContatos.html', context)

class ContatoCreateView(View):
    def get(self, request, *args, **kwargs):
        contexto = {
            'formulario': ContatoModel2Form, 
            }
        return render(request, "contatos/criaContato.html", contexto) 
    def post(self, request, *args, **kwargs):
        formulario = ContatoModel2Form(request.POST)
        if formulario.is_valid():
            contato = formulario.save()
            contato.save()
            return HttpResponseRedirect(reverse_lazy("contatos:lista-contatos"))

class ContatoUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        pessoa = Pessoa.objects.get(pk=pk)
        formulario = ContatoModel2Form(instance=pessoa)
        context = {'pessoa': formulario, }
        return render(request,'contatos/atualizaContato.html', context)
    def post(self, request, pk, *args, **kwargs):
        pessoa = get_object_or_404(Pessoa, pk=pk)
        formulario = ContatoModel2Form(request.POST, instance=pessoa)
        if formulario.is_valid():
            pessoa = formulario.save() # cria uma pessoa com os dados do formulário
            pessoa.save() # salva uma pessoa no banco de dados
            return HttpResponseRedirect(reverse_lazy("contatos:lista-contatos"))
        else:
            contexto = {'pessoa': formulario, }
            return render(request,'contatos/atualizaContato.html', contexto)

class ContatoDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        pessoa = Pessoa.objects.get(pk=pk)
        contexto = {'pessoa': pessoa, }
        return render(request,'contatos/apagaContato.html', contexto)
    
    def post(self, request, pk, *args, **kwargs):
        pessoa = Pessoa.objects.get(pk=pk)
        pessoa.delete()
        return HttpResponseRedirect(reverse_lazy("contatos:lista-contatos"))

@require_GET
def verificaEmail(request):

    if "@" not in request.GET.get('email'):
        resposta = {
                'emailValido':
                    'False'
        }
        return JsonResponse(resposta)
    else:
        resposta = {
                'emailValido':
                    'True'
        }
        return JsonResponse(resposta)
