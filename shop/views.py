from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

# MERCHANT_KEY = 'Your-Merchant-key';

# Create your views here.


def index(request):

    allProd = []
    catProd = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProd}
    for cat in cats:
        products = Product.objects.filter(category=cat)
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProd.append([products, range(1, nSlides), nSlides])

    params = {'allProd': allProd}
    return render(request, 'shop/index.html', params)


def searchMatch(item, query):
    if query in item.desc.lower() or query in item.product_name.lower() or query == item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProd = []
    catProd = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProd}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        products = [item for item in prodtemp if searchMatch(item, query)]
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))

        if len(products) != 0:
            allProd.append([products, range(1, nSlides), nSlides])

    params = {'allProd': allProd, 'msg': ""}
    if len(allProd) == 0 or len(query) < 4:
        params = {
            'msg': "Sorry we can not understand your query. Please make sure to enter relevant Search."}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')

        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.time})
                    response = json.dumps({"status": "success", "updates": updates, "itemJson": order[0].itemJson},
                                          default=str)
                    # response = json.dumps([updates, order[0].itemJson], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def productView(request, myid):
    # Fetching product by id
    products = Product.objects.filter(id=myid)
    return render(request, 'shop/productView.html', {'product': products[0]})


def checkout(request):
    if request.method == "POST":
        itemJson = request.POST.get('itemJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        orders = Order(itemJson=itemJson, name=name, email=email, phone=phone, address=address, city=city, state=state,
                       zip_code=zip_code, amount=amount)
        orders.save()

        # This is for tracking order.
        update = OrderUpdate(order_id=orders.order_id,
                             update_desc="Your order has been placed.")
        update.save()

        # This is for alert/thank msg after placing order.
        thank = True
        id = orders.order_id

        # Here we will send post request to paytm to accept money from user and transfer to us
        # Remove this from commet to activate paytm payment
        # param_dict = {
        #     'MID': 'Your-Merchant-ID',
        #     'ORDER_ID': str(orders.order_id),
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'shop/paytm.html', {'param_dict': param_dict})

        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' +
                  response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def demopayment(request):
    return render(request, 'shop/demopayment.html')


def thankyou(request):
    return render(request, 'shop/thankyou.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(
                    request, "Oops! Username is already in use. Try another Username.")
                return redirect('/shop/register')
            elif User.objects.filter(email=email).exists():
                messages.info(
                    request, "Oops! Email is already registerd. Try another Email.")
                return redirect('/shop/register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                first_name=first_name, last_name=last_name)
                user.save()
                messages.info(
                    request, "Well Done! You have successfully signed up. Login now!")
                return redirect('/shop/login')
        else:
            messages.info(
                request, "Oops! Password not matching. Please confirm your Password.")
            return redirect('/shop/register')

    else:
        return render(request, 'shop/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, "Welcome! You have successfully signed in!")
            return redirect('/shop')
        else:
            messages.info(request, "Oops! Invalid Credentials!")
            return redirect('/shop/login')
    else:
        return render(request, 'shop/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/shop')
