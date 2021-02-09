from django.shortcuts import render
from django.http import JsonResponse
import json
from . models import *

# Create your views here.
def home(request):
    
     return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        name=request.POST['name']
        number=request.POST['number']
        email=request.POST['email']
        password=request.POST['password']
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        zipcode=request.POST['zipcode']
        login_obj = UserLogin(email=email,password=password)
        login_obj.save()
        fkey=UserLogin.objects.get(email=email)
        details_obj = UserDetails(name=name,number=number,address=address,city=city,state=state,country=country,zipcode=zipcode,fk_username=fkey)
        details_obj.save()
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        login_exist = UserLogin.objects.filter(email=email).exists()
        if login_exist:
            login_obj = UserLogin.objects.filter(email=email)
            if login_obj[0].password == password:
                request.session['user_session'] = login_obj[0].id
                return render(request,'store.html')
            else:
                return render(request,'home.html', {'alert_flag':True})
        else:
            return render(request,'home.html', {'alert_flag':True})
    return render(request,'home.html')


def store(request):
    id = request.session['user_session']
    customer = UserLogin.objects.get(id=id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store.html', context)

def cart(request):
    id = request.session['user_session']
    customer = UserLogin.objects.get(id=id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def buy(request):
    context = {}
    return render(request, 'buy.html', context)

def logout(request):
    return render(request, 'home.html')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    id = request.session['user_session']

    customer = UserLogin.objects.get(id=id)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)