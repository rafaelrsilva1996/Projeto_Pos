import re
from django.http import HttpResponse
from django.shortcuts import render
from django.template import context

from .models import Episodio, Serie, Temporada

def series_lista(request):
    lista_series = Serie.objects.all()
    context = {'lista_series': lista_series}
    return render(request, 'series_lista.html', context)

def series_detalhes(request, pk):
    serie = Serie.objects.get(pk=pk)
    temporada = Temporada.objects.get(serie_id=pk)
    return HttpResponse("Nome: {} <br/> Temporadas: {}".format(
        serie.nome, temporada.numero
    ))

def episodio_detalhes(request, pk):
    e = Episodio.objects.get(pk=pk)
    return HttpResponse("Titulo: {} <br/> Data: {} <br/> Temporada: {}".format(
        e.titulo, e.data, e.temporada
    ))

def episodio_lista_nota(request, nota):
    objects = Episodio.objects.filter(reviewepisodio__nota=nota)
    context = {'objects': objects, 'nota':nota}
    return render(request, 'episodio_lista_nota.html', context)