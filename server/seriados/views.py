import re
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import context
from django.views.generic import TemplateView, ListView, View, DetailView

from .models import Episodio, Serie, Temporada

def prepare_data_list(objects, fields_name):
    labels = list()
    for field_name in fields_name:
        field = objects.model._meta.get_field(field_name)
        labels.append(field.verbose_name)
    
    rows = list()
    for _object in objects:
        row = dict()
        rows.append(row)
        row['pk'] = _object.pk
        row['data'] = list()
        for field_name in fields_name:
            row['data'].append(getattr(_object, field_name))
    
    return labels, rows

def prepare_data_detail(_object, fields_name):
    data = model_to_dict(_object)
    rows = list()
    for field_name in fields_name:
        field = _object._meta.get_field(field_name)
        rows.append({'label': field.verbose_name, 'value': data[field_name]})
    return rows

def series_list(request):
    search = request.GET.get('search', "")
    objects = Serie.objects.filter(nome__contains=search)
    labels, rows = prepare_data_list(objects, ['nome'])
    context = {
        'title': "Séries",
        'labels': labels,
        'rows': rows,
        'detail_url': 'seriados:series_details',
        'list_url': 'seriados:series_list',
    }
    return render(request, 'list.html', context)

def series_details(request, pk):
    _object = get_object_or_404(Serie, pk=pk)
    context = {
        'title': "Série",
        'data': prepare_data_detail(_object, ['nome']),
    }
    return render(request, 'details.html', context)

def episodio_list(request):
    search = request.GET.get('search', "")
    objects = Episodio.objects.filter(titulo__contains=search)
    labels, rows = prepare_data_list(objects, ['titulo', 'data'])
    context = {
        'title': "Episódios",
        'labels': labels,
        'rows':rows,
        'detail_url': 'seriados:episodio_details',
        'list_url': 'seriados:episodio_list',
        }
    return render(request, 'list.html', context)

def episodio_details(request, pk):
    _object = get_object_or_404(Episodio, pk=pk)
    context = {
        'title': "Episódio",
        'data': prepare_data_detail(_object, ['titulo', 'data', 'temporada']),
    }
    return render(request, 'details.html', context)

def episodio_nota_list(request, nota):
    search = request.GET.get('search', "")
    objects = Episodio.objects.filter(reviewepisodio__nota=nota if nota else search)
    context = {
        'objects': objects,
        'nota':nota,
        'detail_url': 'seriados:episodio_details',
    }
    return render(request, 'episodio_nota_list.html', context)


class Contact(TemplateView):
    template_name = 'contact.html'


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})


class TemporadaListView(ListView):
    template_name = 'list.html'
    model = Temporada
    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search', "")
        objects = Temporada.objects.filter(serie__nome__contains=search)
        labels, rows = prepare_data_list(objects, ['numero', 'serie'])

        context = super().get_context_data(**kwargs)
        context['title'] = 'Temporadas'
        context['book_list'] = objects
        context['labels'] = labels
        context['rows'] = rows
        context['detail_url'] = 'seriados:temporada_details'
        context['list_url'] = 'seriados:temporada_list'
        return context

class TemporadaDetailView(View):
    def get(self, request, pk):
        _object = get_object_or_404(Temporada, pk=pk)
        context = {
            'title': "Temporada",
            'data': prepare_data_detail(_object, ['numero', 'serie']),
        }
        return render(request, 'details.html', context)