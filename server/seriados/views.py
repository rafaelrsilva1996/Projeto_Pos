import re
from django.http import HttpResponse
from django.shortcuts import render
from django.template import context

from .models import Episodio, Serie

def series_lista(request):
    lista_series = Serie.objects.all()
    context = {'lista_series': lista_series}
    return render(request, 'series_lista.html', context)

def episodio_detalhes(request, pk):
    e = Episodio.objects.get(pk=pk)
    return HttpResponse("Titulo: {} <br/> Data: {} <br/> Temporada: {}".format(
        e.titulo, e.data, e.temporada
    ))

def episodio_lista_nota(request, nota):
    objects = Episodio.objects.filter(reviewepisodio__nota=nota)
    context = {'objects': objects, 'nota':nota}
    return render(request, 'episodio_lista_nota.html', context)