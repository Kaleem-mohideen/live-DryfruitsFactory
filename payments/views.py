from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from shop.models import *
import datetime
from shop.utils import guestOrder
from .PayTm import Checksum
from django.conf import settings
from django.http import HttpResponse
import requests
from django.contrib import messages
from django.urls import reverse
from shop.utils import *
# import json

# Create your views here.

def initiate_payment(request):
    order_id = datetime.datetime.now().timestamp()
    data = dict(request.POST)

    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        except Order.MultipleObjectsReturned:
            order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
    else:
        if request.method =="POST":
            data['name'] = f"{request.POST.get('fname', '')} {request.POST.get('lname', '')}"
            data['email'] = request.POST.get('email', '')
        customer, order = guestOrder(request, data)

    order.order_id = order_id
    order.save()

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # else:
    #     if request.method =="POST":
    #         name = f"{request.POST.get('fname', '')} {request.POST.get('lname', '')}"
    #         email = request.POST.get('email', '')
    #     customer, created = Customer.objects.get_or_create(email=email,)
    #     customer.name = name
    #     customer.save()
    #     order = Order.objects.create(customer=customer,complete=False,)


    # if total == order.get_cart_total_with_deliverycharge:
    #     order.complete = True
    # order.save()


    if order.shipping == True:
        shippingaddr, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        shippingaddr.address=data['address'][0]
        shippingaddr.city=data['city'][0]
        shippingaddr.state=data['state'][0]
        shippingaddr.zipcode=data['pincode'][0]
        shippingaddr.save()

    email = customer.email
    if not email:
        email = request.user.email
    total = "%.2f" %order.get_cart_total_with_deliverycharge
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(order.order_id)),
        ('CUST_ID', str(email)),
        ('TXN_AMOUNT', str(total)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/payments/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = Checksum.generateSignature(paytm_params, merchant_key)
    
    # transaction.checksum = checksum
    # transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum

    return render(request, 'payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    # paytm will send you post request here
    if request.method == 'POST':
        try:
            received_data = dict(request.POST)

            data = cartData(request)
            print('data',data)
            
            paytm_params = {}
            paytm_checksum = received_data['CHECKSUMHASH'][0]
            for key, value in received_data.items():
                if key == 'CHECKSUMHASH':
                    paytm_checksum = value[0]
                else:
                    print(str(value[0]))
                    paytm_params[key] = str(value[0])
            # Verify checksum
            is_valid_checksum = Checksum.verifySignature(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
            if is_valid_checksum:
                received_data['message'] = "Checksum Matched"
                #if checksum matched then do this to set order to complete
                if request.user.is_authenticated:
                    customer = request.user.customer
                    order, created = Order.objects.get_or_create(customer=customer, order_id=received_data['ORDERID'][0], complete=False)
                else:
                    order, created = Order.objects.get_or_create(order_id=received_data['ORDERID'][0], complete=False)
                #setting the order complete
                # print(received_data['TXNAMOUNT'][0], order.get_cart_total_with_deliverycharge)
                # print(type(received_data['TXNAMOUNT'][0]), type(order.get_cart_total_with_deliverycharge))
                order.save()
                if received_data['RESPCODE'][0]=='01' and received_data['TXNAMOUNT'][0] == '%.2f' %order.get_cart_total_with_deliverycharge:
                    print("++++++++++++++++++++++++++++Entered in equality")
                    response = redirect(f"{reverse('shop:track-order', args=(received_data['ORDERID'][0],))}")
                    # print("cookies c",s.cookies.keys())

                    order.complete = True
                    transactionId = received_data['TXNID'][0]
                    order.transaction_id = transactionId
                    order.save()
                    orderId = received_data['ORDERID'][0]
                    messages.success(request, f'Transaction completed successfully Order Id: {orderId} Transaction Id: {transactionId}')
                    # response = render(request, 'payments/callback.html', context=received_data)
                    response.delete_cookie('cart')
                    return response
                    # return response
            else:
                received_data['message'] = "Checksum Mismatched"
            
            items = data['items']
            cartItems = data['cartItems']
            received_data['items'] = items
            print('cartItems',cartItems)
            received_data['cartItems'] = cartItems
            print('received_data', received_data)
            # response = redirect(f"{reverse('callbackResult', args=(received_data['ORDERID'][0],))}")
            return render(request, 'payments/callback.html', context=received_data)
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

# @csrf_exempt
# def callbackResult(request, context):
#     print("_____context",context)
#     received_data = {}
#     data = cartData(request)
#     items = data['items']
#     cartItems = data['cartItems']
#     received_data['items'] = items
#     print('cartItems',cartItems)
#     received_data['cartItems'] = cartItems
#     print('received_data', received_data)
#     return render(request, 'payments/callback.html', context=received_data)