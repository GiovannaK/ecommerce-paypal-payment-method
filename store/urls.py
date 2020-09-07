from django.urls import  path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    #User
    path('login/', views.loginPage, name="login_form"),
    path('register/', views.register, name="register"),
    path('shipping_info/', views.shippingInfo, name="shipping_info"),
    path('profile/', views.profile, name="profile"),
    path('update_user_info/', views.updateUserInfo, name="update_user_info"),
    path('update_shipping_info/', views.updateShippingInfo, name="update_shipping_info"),
    path('logout/', views.logoutUser, name="logout_user"),
    
    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"), name="reset_password"),
    
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_sent.html'), name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"), name="password_reset_confirm"),
    
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_complete.html"), name="password_reset_complete"),
    
    #Products
    path('', views.store, name="store"),
    path('search/', views.search, name="search"),
    path('categories/<slug:slug>/', views.categories, name="categories"),
    path('details/<slug:slug>/', views.details, name="details"),

    # cart
    path('cart/', views.cart, name="cart"),
    path('addtocart/', views.Addtocart.as_view(), name="addtocart"),
    path('removefromcart/', views.RemoveFromCart.as_view(), name="removefromcart"),
    
    #order
    path('payment/<int:pk>/', views.payment, name="payment"),
    path('close_order/', views.closeOrder, name="close_order"),
    path('save_order/', views.saveOrder, name="save_order"),
    path('order_detail/<int:pk>/', views.orderDetail, name="order_detail"),
]