from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.paginator import Paginator
import copy
from .models import *
from . import models
from .forms import ProfileForm, UserForm, UpdateUserInfo

# User

def error404(request, exception):
    return render(request, 'store/404.html')


def loginPage(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)    
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('profile')
        else:
            messages.info(request, 'Usuário ou senha incorretos!')

    context = {'categories':categories}
    return render(request, 'store/login.html', context)

@login_required(login_url='login_form')
def logoutUser(request):
    logout(request)
    return redirect('store')


def register(request):
    categories = Category.objects.all()
    userform = UserForm()

    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            userform.save()  
            user = userform.cleaned_data.get('username')
            return redirect('login_form')  
        else:
            messages.error(request, 'Verifique se as informações estão corretas!')
             
    context = {'userform':userform, 'categories':categories}
    return render(request, 'store/register.html', context)


@login_required(login_url='login_form')
def shippingInfo(request):
    profile = request.user
    profileform = ProfileForm()
    if request.user.is_authenticated: 
        if request.method == 'POST':
            profileform = ProfileForm(request.POST)
            if profileform.is_valid():
                profile = profileform.save(commit=False)
                profile.user = request.user
                profile.save() 
                messages.success(
                    request, 
                    'Informações de entrega adicionadas com sucesso!'
                ) 
                return redirect('profile')
            else:
                messages.error(request, 'Verifique se as informações estão corretas!')
                
    context = {'profileform':profileform}
    return render(request, 'store/shipping_info.html', context)


@login_required(login_url='login_form')
def updateShippingInfo(request):
    profile = request.user.profile
    profileform = ProfileForm(instance=profile)
    if request.user.is_authenticated: 
        if request.method == 'POST':
            profileform = ProfileForm(request.POST, instance=profile)
            if profileform.is_valid():
                profile.save() 
                messages.success(
                    request, 
                    'Informações de entrega atualizadas com sucesso!'
                ) 
                return redirect('profile') 
        
            else:
                messages.error(request, 'Verifique se as informações estão corretas!')
    
    context = {'profileform':profileform,}
    return render(request, 'store/shipping_info.html', context)
        

@login_required(login_url='login_form')
def updateUserInfo(request):
    cart = copy.deepcopy(request.session.get('cart', {}))
    user = request.user
    updateuserform = UpdateUserInfo(instance=user)
    if request.user.is_authenticated: 
        if request.method == 'POST':
            updateuserform = UpdateUserInfo(request.POST, instance=user)
            if updateuserform.is_valid():
                updateuserform.save()  
                messages.success(
                    request, 
                    'Informações pessoais atualizadas com sucesso!'
                ) 
                request.session['cart'] = cart
                request.session.save()
                return redirect('login_form')
            else:
                messages.error(request, 'Verifique se as informações estão corretas!')

    context = {'updateuserform':updateuserform}
    return render(request, 'store/update_user.html', context)


@login_required(login_url='login_form')
def profile(request):
    categories = Category.objects.all()
    
    context = {'categories':categories,}
    return render(request, 'store/profile.html', context)


#products

def store(request):
    products = Product.objects.all()[:10]
    categories = Category.objects.all()
    
    context = {'products':products, 'categories':categories,}
    return render(request, 'store/index.html', context)


def search(request):
    query = request.GET.get('q', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query)
        |Q(description__icontains=query))
        categories = Product.objects.filter(Q(category__name__icontains=query))
    else:
        products = Product.objects.all()   
        categories = Product.objects.all()

    context = {'products':products, 'categories':categories}    
    return render(request, 'store/index.html', context)     
    
    
def details(request, slug):
    product = Product.objects.get(slug=slug)
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {'product':product, 'products':products, 
    'categories':categories,}
    return render(request, 'store/details.html', context)


def categories(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {'category':category, 'products':products, 
    'categories':categories, 'page_obj':page_obj}
    return render(request, 'store/categories.html', context)


#cart
@login_required(login_url='login_form')
def cart(request):
    categories = Category.objects.all()
    
    context = {'categories':categories}
    return render(request, 'store/cart.html', context)


class Addtocart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', 
            reverse('store')
        )
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            messages.error(
                self.request,
                'Produto inexistente'
            )
            return redirect(http_referer)
        variation = get_object_or_404(models.Variation, id=variation_id)
        
        variation_stock = variation.stock
        product = variation.product
        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unity_price = variation.price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''    

        if variation.stock < 1:
            messages.error(
                self.request,
                'Estoque insuficiente!'
            )
            return redirect(http_referer)
        
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()
        cart = self.request.session['cart']  

        if variation_id in cart:
            quantity_cart = cart[variation_id]['quantity']
            quantity_cart += 1

            if variation_stock < quantity_cart:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantity_cart}x no'
                    f'produto {product_name}! Adicionamos {variation_stock}x'
                    f'no seu carrinho'
                )
                quantity_cart = variation_stock

            cart[variation_id]['quantity'] = quantity_cart
            cart[variation_id]['quantitative_price'] = unity_price * quantity_cart    
        
        else:
            cart[variation_id] = {
                'product_id':product_id,
                'product_name':product_name,
                'variation_name':variation_name,
                'variation_id':variation_id,
                'unity_price':unity_price,
                'quantitative_price': unity_price,
                'quantity':1,
                'slug':slug,
                'image':image,
            }

        self.request.session.save()  
        messages.success(
            self.request,
            f'Produto {product_name} {variation_name} adicionado ao seu carrinho!'
            f' {cart[variation_id]["quantity"]}X'
        )

        return redirect(http_referer)


class RemoveFromCart(View):

    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', 
            reverse('store')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]  

        messages.success(
            self.request,
            f'Produto {cart["product_name"]} {cart["variation_name"]} '
            f'foi removido do seu carrinho!'
        )  

        del self.request.session['cart'][variation_id] 
        self.request.session.save()
        return redirect(http_referer)

# Order
@login_required(login_url='login_form')
def payment(request, pk):
    order = Order.objects.get(pk=pk)
    categories = Category.objects.all()
    
    context = {'order':order, 'categories':categories}
    return render(request, 'store/payment.html', context)
    


@login_required(login_url='login_form')    
def saveOrder(request):
    if not request.session.get('cart'):
        messages.error(
            request, 
            'Carrinho vazio!'
        )
        return redirect('profile')

    cart = request.session.get('cart')
    cart_id_variations = [v for v in cart]
    bd_variations = list(Variation.objects.select_related('product')
    .filter(id__in=cart_id_variations)
    
    )

    for variation in bd_variations:
        vid = str(variation.id)
        
        stock = variation.stock
        qtd_cart = cart[vid]['quantity']
        unt_price = cart[vid]['unity_price']

        error_msg_stock = ''

        if stock < qtd_cart:
            cart[vid]['quantity'] = stock
            cart[vid]['quantitative_price'] = stock * unt_price

            error_msg_stock = 'Estoque insuficiente para alguns produtos do seu carrinho.'\
            ' Reduzimos a quantidade de alguns produtos, verifique'\
            ' no seu carrinho quais produtos sofreram alterações.'

            if error_msg_stock:
                messages.error(
                    request,
                    error_msg_stock
                )

                request.session.save()
                return redirect('cart')
        
        qtd_total_cart = utils.cart_total_qt(cart)
        total_price_cart = utils.cart_totals(cart)

        order = Order(
            user = request.user,
            total = total_price_cart,
            status='C',
            qtd_total = qtd_total_cart,
        )

        order.save()
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    quantity=v['quantity'],
                    image=v['image'],
                )for v in cart.values()
            ]
        )
    
        del request.session['cart']
        return redirect(
            reverse(
                'payment',
                kwargs={
                    'pk': order.pk
                }
            )
        )
    
    
@login_required(login_url='login_form')
def closeOrder(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'store/close_order.html', context)


@login_required(login_url='login_form')
def orderDetail(request, pk):
    order = Order.objects.get(pk=pk)
    categories = Category.objects.all()
    
    context = {'order':order, 'categories':categories}
    return render(request, 'store/order_detail.html', context)
