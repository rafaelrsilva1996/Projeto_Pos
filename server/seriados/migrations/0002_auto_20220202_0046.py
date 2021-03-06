# Generated by Django 3.2.11 on 2022-02-02 00:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seriados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewEpisodio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.CharField(choices=[('A', 'Excelente'), ('B', 'Bom'), ('C', 'Ruim')], default='B', max_length=1)),
            ],
        ),
        migrations.RenameModel(
            old_name='Epsidio',
            new_name='Episodio',
        ),
        migrations.CreateModel(
            name='Revisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviews_episodios', models.ManyToManyField(through='seriados.ReviewEpisodio', to='seriados.Episodio')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='reviewepisodio',
            name='episodio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seriados.episodio'),
        ),
        migrations.AddField(
            model_name='reviewepisodio',
            name='revisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seriados.revisor'),
        ),
    ]
