from django.urls import path, re_path, include, register_converter

from . import views

app_name = 'seriados'

urlpatterns = [
    path('series/', views.series_lista, name='series_lista'),

    path('episodio/<int:pk>/', views.episodio_detalhes, name='episodio_detalhes'),

    path('episodios/nota/<str:nota>/', views.episodio_lista_nota, name='episodio_lista_nota'),
]