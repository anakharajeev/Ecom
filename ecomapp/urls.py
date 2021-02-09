from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('signup', views.signup, name='signup'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
    path('store/', views.store, name='store'),
	path('cart/', views.cart, name='cart'),
	path('update_item/', views.updateItem, name='update_item'),
	path('buy/', views.buy, name='buy'),

]