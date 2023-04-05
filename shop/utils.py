import json
from .models import *

def weightProcess(request, weightSelected1):


    if isinstance(weightSelected1, str) and weightSelected1:

        if 'kgs' in weightSelected1 and 'gms' in weightSelected1:
            li = weightSelected1.split(' kgs ')
            k = int(li[0])
            g = int(li[1].strip(' gms'))
            selectedWght = k + g/1000
        elif 'kg' in weightSelected1 and 'gms' in weightSelected1:
            li = weightSelected1.split(' kg ')
            k = int(li[0])
            g = int(li[1].strip(' gms'))
            selectedWght = k + g/1000
        elif 'kgs' in weightSelected1 and 'gms' not in weightSelected1:
            selectedWght = int(weightSelected1.strip(' kgs'))
        elif 'kg' in weightSelected1 and 'gms' not in weightSelected1:
            selectedWght = int(weightSelected1.strip(' kg'))
        elif 'gms' in weightSelected1 and 'kg' not in weightSelected1 and 'kgs' not in weightSelected1:
            selectedWght = int(weightSelected1.strip(' gms'))/1000
        return selectedWght
    return weightSelected1

def cookieCart(request):

    #Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print("========================",cart)
    # print("cart['1']",type(list(cart['1'].keys())[0]))
    # {'1': {'true': {'quantity': 4, 'selectedweight': 0}, 'false': {'quantity': 2, 'selectedweight': 0}}, '5': {'false': {'quantity': 1, 'selectedweight': 0}}}
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'get_cartSavingsfrom_actual_total':0, 'get_cart_actual_total':0, 'shipping':False}
    cartItems = order['get_cart_items']
 #{"1":{"quantity":1,"selectedweight":0},"5":{"quantity":1,"selectedweight":0}}
    print('cart', cart)
    for i in cart:
        for j in cart[i]:
        #We use try block to prevent items in cart that may have been removed from causing error
            try:
                if j == 'true':
                    subprod = SubProduct.objects.get(product = Product.objects.get(id = i), productType = ProductType.objects.get(type = "Wholesale"))
                elif j == 'false':
                    subprod = SubProduct.objects.get(product = Product.objects.get(id = i), productType = ProductType.objects.get(type = "Retail"))
                    print(subprod)
                if(cart[i][j]['quantity']>0): #items with negative quantity = lot of freebies
                    cartItems += cart[i][j]['quantity']
                    weightNumber = weightProcess(request, cart[i][j]['selectedweight'])

                    product = Product.objects.get(id=i)
                    if not weightNumber:
                        weightNumber = subprod.price_weight.weight
                    print('weightNumber',weightNumber)
                    total = (((subprod.offer_price * weightNumber) / subprod.price_weight.weight) * cart[i][j]['quantity'])
                    actual_total = (((subprod.actual_price * weightNumber) / subprod.price_weight.weight) * cart[i][j]['quantity'])
                    savings_total = ((((subprod.actual_price-subprod.offer_price)* weightNumber)/ subprod.price_weight.weight) * cart[i][j]['quantity'])
                    selectedWeight = Weightage.objects.filter(weight = weightNumber).first()

                    order['get_cart_total'] += total
                    order['get_cart_actual_total'] += actual_total
                    order['get_cart_items'] += cart[i][j]['quantity']
                    order['get_cartSavingsfrom_actual_total'] += savings_total
                    



                    item = {
                    'id':product.id,
                    'subProduct':{'id':subprod.id, 'productType':subprod.productType,'pub_date':subprod.pub_date, 'offer_price':subprod.offer_price, 'actual_price':subprod.actual_price, 'ava_quantity':subprod.ava_quantity,
                    'price_weight':subprod.price_weight, 'available_weights': subprod.available_weights.all(),
                    'product': {'id':product.id, 'product_name':product.product_name, 'desc':product.desc, 'pub_date':product.pub_date, 'category':product.category, 'imageURL':product.imageURL, 'digital':product.digital}},
                    'quantity':cart[i][j]['quantity'], 'get_total':total, 'get_actual_total':actual_total, 'get_savings_total': savings_total, 'weightSelected':selectedWeight,
                    }
                    items.append(item)

                    if product.digital == False:
                        order['shipping'] = True
            except:# Exception as e:
                #print('except', e)
                pass
    deliverycharge = DeliveryCharge.objects.all().first().delivery_charge
    gstcharge = GSTCharge.objects.all().first().gst_charge
    order['deliverycharge'] = deliverycharge if deliverycharge else 0
    order['gstcharge'] = gstcharge if gstcharge else 0
    order['get_cart_total_with_deliverycharge'] = order['deliverycharge'] + order['gstcharge'] + order['get_cart_total']
    return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        print(request.user)
        customer, created = Customer.objects.get_or_create(user = request.user)
        ordersHistory = Order.objects.filter(customer=customer)
        if not customer.name:
            customer.name = request.user.first_name +" "+ request.user.last_name
        if not customer.email:
            print(request.user.email)
            customer.email = request.user.email
        customer.save()
        try:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        except Order.MultipleObjectsReturned:
            order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()

        items = OrderItem.objects.filter(order=order, subProduct__isnull=False)
        cartItems = order.get_cart_items


    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        # print('items', items)
        # print('order', order)
        print('cartItems',cartItems)
        ordersHistory = []
    return {'cartItems':cartItems ,'order':order, 'items':items, 'ordersHistory': ordersHistory}

def guestOrder(request, data):
    name = data['name']
    email = data['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
            email=email,
            )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )

    for item in items:
        subproduct = SubProduct.objects.get(id=item['subProduct']['id'])
        orderItem = OrderItem.objects.create(
            subProduct=subproduct,
            order=order,
            quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
            weightSelected = item['weightSelected']
        )
    return customer, order


def functionOrderItem(request, s, i):
    obj = Weightage.objects.get(weight = s)

    return OrderItem.objects.filter(id = i).update(weightSelected =obj.id)
