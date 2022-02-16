import imp
import re
from tkinter.tix import Form
from django import template
from django.forms import fields
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import context
from django.urls import reverse

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Episodio, Revisor, Serie, Temporada, ReviewEpisodio
from .forms import SerieForm, TemporadaForm, RevisorForm, ReviewEpisodioForm

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
        'insert_url': 'seriados:serie_insert',
        'update_url': 'seriados:serie_update',
        'delete_url': 'seriados:serie_delete',
    }
    return render(request, 'list.html', context)

def series_details(request, pk):
    _object = get_object_or_404(Serie, pk=pk)
    context = {
        'title': "Série",
        'data': prepare_data_detail(_object, ['nome']),
        'update_url': 'seriados:serie_update',
        'delete_url': 'seriados:serie_delete',
        'pk': pk,
    }
    return render(request, 'details.html', context)

def serie_insert(request):
    if request.method == 'GET':
        form = SerieForm()
    elif request.method == 'POST':
        form = SerieForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            obj = Serie(nome = nome)
            obj.save()
            return HttpResponseRedirect(reverse(
                'seriados:series_details',
                kwargs = {'pk': obj.pk}
            ))

    return render(request, 'form_base.html', {
        'form': form,
        'target_url': 'seriados:serie_insert',
    })


class SerieUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Serie
    fields = ['nome']


class SerieDeleteView(DeleteView):
    template_name = "serie_confirm_delete.html"
    model = Serie

    def get_success_url(self):
        return reverse('seriados:serie_list')

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
        'insert_url': 'seriados:episodio_insert',
        'update_url': 'seriados:episodio_update',
        'delete_url': 'seriados:episodio_delete',
        }
    return render(request, 'list.html', context)

def episodio_details(request, pk):
    _object = get_object_or_404(Episodio, pk=pk)
    context = {
        'title': "Episódio",
        'data': prepare_data_detail(_object, ['titulo', 'data', 'temporada']),
        'update_url': 'seriados:episodio_update',
        'delete_url': 'seriados:episodio_delete',
        'pk': pk,
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


class EpisodioCreateView(CreateView):
    template_name = 'form_generic.html'
    model = Episodio
    fields = ['temporada', 'data', 'titulo']


class EpisodioUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Episodio
    fields = ['temporada', 'data', 'titulo']


class EpisodioDeleteView(DeleteView):
    template_name = "episodio_confirm_delete.html"
    model = Episodio

    def get_success_url(self):
        return reverse('seriados:episodio_list')


class Contact(TemplateView):
    template_name = 'contact.html'


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})


class TemporadaListView(View):
    def get(self, request):
        search = request.GET.get('search', "")
        objects = Temporada.objects.filter(serie__nome__contains=search)
        labels, rows = prepare_data_list(objects, ['numero', 'serie'])
        context = {
            'book_list': objects,
            'title': 'Temporadas',
            'labels': labels,
            'rows': rows,
            'detail_url': 'seriados:temporada_details',
            'list_url': 'seriados:temporada_list',
            'insert_url': 'seriados:temporada_insert',
            'update_url': 'seriados:temporada_update',
            'delete_url': 'seriados:temporada_delete',
        }
        return render(request, 'list.html', context)

class TemporadaDetailView(View):
    def get(self, request, pk):
        _object = get_object_or_404(Temporada, pk=pk)
        context = {
            'title': "Temporada",
            'data': prepare_data_detail(_object, ['numero', 'serie']),
            'update_url': 'seriados:temporada_update',
            'delete_url': 'seriados:temporada_delete',
            'pk': pk,
        }
        return render(request, 'details.html', context)


class TemporadaCreateView(CreateView):
    template_name = "form_generic.html"
    form_class = TemporadaForm


class TemporadaUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Temporada
    fields = ['serie', 'numero']


class TemporadaDeleteView(DeleteView):
    template_name = "temporada_confirm_delete.html"
    model = Temporada

    def get_success_url(self):
        return reverse('seriados:temporada_list')


class RevisorListView(ListView):
    template_name = 'revisor_list.html'
    model = Revisor


class RevisorDetailView(DetailView):
    template_name = 'revisor_details.html'
    model = Revisor


class RevisorCreateView(CreateView):
    template_name = "form_generic.html"
    form_class = RevisorForm


class RevisorUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Revisor
    fields = ['user']


class RevisorDeleteView(DeleteView):
    template_name = "revisor_confirm_delete.html"
    model = Revisor

    def get_success_url(self):
        return reverse('seriados:revisor_list')


class ReviewEpisodioListView(ListView):
    template_name = 'reviewepisodio_list.html'
    model = ReviewEpisodio


class ReviewEpisodioDetailView(DetailView):
    template_name = 'reviewepisodio_details.html'
    model = ReviewEpisodio


class ReviewEpisodioCreateView(CreateView):
    template_name = "form_generic.html"
    form_class = ReviewEpisodioForm


class ReviewEpisodioUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = ReviewEpisodio
    fields = ['episodio', 'revisor', 'nota']


class ReviewEpisodioDeleteView(DeleteView):
    template_name = "reviewepisodio_confirm_delete.html"
    model = ReviewEpisodio

    def get_success_url(self):
        return reverse('seriados:reviewepisodio_list_list')