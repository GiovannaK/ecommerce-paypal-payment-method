from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.text import slugify
import re
from utils.validacpf import valida_cpf
from utils import utils

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome da categoria')
    slug = models.SlugField(unique=True, blank=True, null=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)   
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'    
    

class Product(models.Model):  
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoria')
    name = models.CharField(max_length=200, verbose_name='Nome')
    price =  models.FloatField(verbose_name='Preço')
    description = models.TextField(verbose_name='Descrição')
    image = models.ImageField(upload_to='product_images/%Y/%m/', blank=True, null=True, verbose_name='Imagem(Opcional)')
    slug = models.SlugField(unique=True, blank=True, null=True)
    digital = models.BooleanField(default=False, null=True)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    # formatting price replacing . to ,
    def get_formated_price(self):
        return utils.formatting_price(self.price)
    get_formated_price.short_description = 'Preço'    

    
    # add slug 
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)   


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'  
        ordering = ['-id']  


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produto')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nome')
    price = models.FloatField(verbose_name='Preço')
    stock = models.PositiveIntegerField(default=1, verbose_name='Estoque')

    def __str__(self):
        return self.name or self.product.name
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    total = models.FloatField(verbose_name='Total')
    qtd_total = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        verbose_name='Status',
        default='C',
        max_length=1,
        choices = (
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),

        )
    )

    def __str__(self):
        return f'Pedido N. {self.pk}'
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Pedido')
    product = models.CharField(max_length=200, verbose_name='Produto')
    product_id = models.PositiveIntegerField(verbose_name='Id do Produto')
    variation = models.CharField(max_length=200, verbose_name='Variação')
    variation_id = models.PositiveIntegerField(verbose_name='Id da Variação')
    price = models.FloatField(verbose_name='Preço')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    image = models.CharField(max_length=2000, verbose_name='Imagem')


    def __str__(self):
        return f'Item do {self.order}'

    class Meta:
        verbose_name='Item do pedido'
        verbose_name_plural='Itens do pedido'    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    birth_date = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    address = models.CharField(max_length=50, verbose_name='Endereço')
    number = models.CharField(max_length=5, verbose_name='Número')
    complement = models.CharField(max_length=30, verbose_name='Complemento')
    neighborhood = models.CharField(max_length=30, verbose_name='Bairro')
    cep = models.CharField(max_length=8, verbose_name='CEP')
    city = models.CharField(max_length=30, verbose_name='Cidade')
    state = models.CharField(
        max_length=2,
        verbose_name='estado',
        default='PR',
        choices= (
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.user}'
    
    
    def clean(self):
        error_messages = {}
        
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido!'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:    
            error_messages['cep'] = 'CEP inválido, digite os 8 dígitos do CEP!'

        if error_messages:
            raise ValidationError(error_messages)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'