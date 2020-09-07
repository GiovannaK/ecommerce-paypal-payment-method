# Generated by Django 3.0.5 on 2020-08-14 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_auto_20200814_0052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(verbose_name='Total')),
                ('status', models.CharField(choices=[('A', 'Aprovado'), ('C', 'Criado'), ('R', 'Reprovado'), ('P', 'Pendente'), ('E', 'Enviado'), ('F', 'Finalizado')], default='C', max_length=1, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=200, verbose_name='Produto')),
                ('product_id', models.PositiveIntegerField(verbose_name='Id do Produto')),
                ('variation', models.CharField(max_length=200, verbose_name='Variação')),
                ('variation_id', models.PositiveIntegerField(verbose_name='Id da Variação')),
                ('price', models.FloatField(verbose_name='Preço')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('image', models.CharField(max_length=2000, verbose_name='Imagem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Order', verbose_name='Pedido')),
            ],
            options={
                'verbose_name': 'Item do pedido',
                'verbose_name_plural': 'Itens do pedido',
            },
        ),
    ]