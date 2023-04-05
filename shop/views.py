from django.shortcuts import render
from .models import *
from math import ceil
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
import json
from .utils import *
from .filters import *
from django.db.models import Min,Max
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import F
from functools import reduce
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# def weightProcess(request):
#     data = request.body
#     print("weightSelected", data)
#     return JsonResponse('WeightPRocess..', safe=False)



#     data = json.loads(request.body)

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     else:
#         customer, order = guestOrder(request, data)

#     total = float(data['form']['total'])
#     # order.order_id = order_id

#     if total == order.get_cart_total_with_deliverycharge:
#         order.complete = True
#     order.save()

#     if order.shipping == True:
#         ShippingAddress.objects.create(
#         customer=customer,
#         order=order,
#         address=data['shipping']['address'],
#         city=data['shipping']['city'],
#         state=data['shipping']['state'],
#         zipcode=data['shipping']['zipcode'],
#         )
def processOrder(request):
    data = json.loads(request.body)
    productId = data['productId']
    wholesale = data['wholesale']
    action = data['action']
    print("productId in processOrder",wholesale)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = json.dumps(list(data['items']), indent=4, sort_keys=True, default=str)
    if wholesale:
        subprod = SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale"))
    else:
        subprod = SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Retail"))
    context = {'items':items, 'order': order, 'cartItems': cartItems, 'subprodId': subprod.id}
    return JsonResponse(context)

def checkSwitchToggle(request):

    data = json.loads(request.body)
    value = data.get("value", True) # change here to default to Retail
    print(value)
    print("valuetype", type(value))
    productId = data['productId']
    context = {}
    print(f'price{productId}')
    if SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale"), enabled = True).exists() and value:
        print(productId,"true")
        context.update({productId: "true", f'price{productId}': serializers.serialize('json',SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale"))), 'offer_percentage': SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale")).offer_percentage, 'subproId': SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale")).id})

    elif SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Retail"), enabled = True).exists():
        print(productId,"false")
        context.update({productId: "false", f'price{productId}': serializers.serialize('json',SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Retail"))), 'offer_percentage': SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Retail")).offer_percentage, 'subproId': SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Retail")).id})
    elif SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale"), enabled = True).exists() and not value:
        print(productId,"true")
        context.update({productId: "true", f'price{productId}': serializers.serialize('json',SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale"))), 'offer_percentage': SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale")).offer_percentage, 'subproId': SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale")).id})
    else:
        # product = Product.objects.get(pk = productId)
        # product.enabled = False
        # product.save()
        context.update({productId: "None", f'price{productId}': serializers.serialize('json',Product.objects.filter(pk = productId))})
        print(productId,None)
    print(f'price{productId}',type(context[f'price{productId}']))

    if request.user.is_authenticated and context[productId] != "None" :
        data = cartData(request)
        items = data['items']
        item_listIdQueryset = items.values_list('subProduct', flat=True).distinct()
        print(".....item_listQueryset", item_listIdQueryset)
        if context['subproId'] in item_listIdQueryset:
            context.update({'itemIn' : True})
        else:
            context.update({'itemIn' : False})

    elif context[productId] != "None":
        data = cartData(request)
        items = data['items']

        if items:
            print('items',items)
            subProductIdList = [d['subProduct']['id'] for d in items]
            # subProductIdList = list(items.values_list('subProduct',flat = True))
        else:
            subProductIdList = []
        if context['subproId'] in subProductIdList:
            context.update({'itemIn' : True})
        else:
            context.update({'itemIn' : False})
    print("context", context)
    return JsonResponse(context)

def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    wholesale = data['wholesale']
    print("wholesale", wholesale)



    customer = request.user.customer
    if not customer:
        customer, created = Customer.objects.get_or_create(user = request.user)
    if not customer.name:
            customer.name = request.user.first_name +" "+ request.user.last_name
    if not customer.email:
        print(request.user.email)
        customer.email = request.user.email
    customer.save()
    product = Product.objects.get(id=productId)

    if wholesale and SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale")).exists():
        subproduct = SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Wholesale"))
    elif not wholesale and SubProduct.objects.filter(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Retail")).exists():
        subproduct = SubProduct.objects.get(product = Product.objects.get(pk = productId), productType = ProductType.objects.get(type = "Retail"))
    else:
        pass

    print("subProduct",subproduct)
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except Order.MultipleObjectsReturned:
        order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
    print(order)
    try:
        orderItem, created = OrderItem.objects.get_or_create(order=order, subProduct=subproduct)#, subProduct=subProduct)
    except Order.MultipleObjectsReturned:
        orderItem = OrderItem.objects.filter(order=order, subProduct=subproduct).order_by('id').last()
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if action == 'delete':
        orderItem.delete()
    if orderItem.quantity <= 0:
        orderItem.delete()

    data1 = cartData(request)

    cartItems = data1['cartItems']
    order = model_to_dict(data1['order'])

    items = serializers.serialize('json', data1['items'])

    # data = {'items':items, 'order': order, 'cartItems': cartItems}
    # data1 = json.dumps(data)
    # data1 = str(data)


    if 'strweight' in data:
        weightSelected1 = data['strweight']


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
            o = functionOrderItem(request, selectedWght, orderItem.id)
    print(items)

    get_cart_total = '{0:g}'.format(data1['order'].get_cart_total)
    get_cart_actual_total = '{0:g}'.format(data1['order'].get_cart_actual_total)
    get_cartSavingsfrom_actual_total = '{0:g}'.format(data1['order'].get_cartSavingsfrom_actual_total)
    get_cart_total_with_deliverycharge = '{0:g}'.format(data1['order'].get_cart_total_with_deliverycharge)
    deliverycharge = '{0:g}'.format(data1['order'].deliverycharge)
    gstcharge = '{0:g}'.format(data1['order'].gstcharge)
    print(cartItems)
    context = {'items':items, 'order': order, 'cartItems': cartItems, 'get_cart_total': get_cart_total, 'get_cart_actual_total': get_cart_actual_total, 'get_cartSavingsfrom_actual_total':get_cartSavingsfrom_actual_total, 'get_cart_total_with_deliverycharge': get_cart_total_with_deliverycharge, 'deliverycharge': deliverycharge, 'gstcharge':gstcharge, "subproduct_id": subproduct.id }
    print(data1['items'])
    for i in data1['items']:
        context.update({i.subProduct.id: '{0:g}'.format(i.get_total)})
        context.update({f'{i.subProduct.id}actual_price': '{0:g}'.format(i.get_actual_total)})

    return JsonResponse(context)
    # if request.method == 'POST':
    #     request_getdata = json.loads(request.body.decode('UTF-8'))
    #     print(request_getdata)
    #     if request_getdata:
    #         # data = json.loads(request_getdata)
    #         productId = request_getdata['productId']
    #         action = request_getdata['action']
    #         print('Action:', action)
    #         print('Product:', productId)

    #     customer = request.user.customer
    #     product = Product.objects.get(id=productId)
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)

    #     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    #     if action == 'add':
    #         orderItem.quantity = (orderItem.quantity + 1)
    #     elif action == 'remove':
    #         orderItem.quantity = (orderItem.quantity - 1)

    #     orderItem.save()

    #     if orderItem.quantity <= 0:
    #         orderItem.delete()

    # data = cartData(request)

    # cartItems = data['cartItems']
    # # order = data['order']
    # # items = data['items']
    # # data = {'items':items, 'order': order, 'cartItems': cartItems}
    # # data1 = json.dumps(data)
    # # data1 = str(data)
    # return JsonResponse({'cartItems': cartItems})

def index(request):
    data = cartData(request)
    items = data['items']
    cartItems = data['cartItems']
    products = Product.objects.all()
    # print(products)
    n = len(products)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    # params = {'no_of_slides': nSlides, 'range': range(0, nSlides), 'product': products}
    # All Products- display category wise
    allProds = []
    catprods = Product.objects.values('category', 'id')
    # print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        # print(prod)
        # n1 = len(prod)
        # nSlides1 = n1 // 4 + ceil((n1 / 4) - (n1 // 4))
        allProds.extend(prod)
    # print(allProds)
    params = {'no_of_slides':nSlides, 'range':range(0, nSlides),'product': allProds, 'cartItems':cartItems, 'items':items}
    return render(request, 'shop/index.html', params)

def aboutus(request):
    return render(request, 'shop/aboutus.html')
def contactus(request):
    if request.method =="POST":
        name = request.POST.get('name', '')
        num = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        msg = request.POST.get('msg', '')

        contact = Contact(name=name, email=email, phone=num, msg=msg)
        contact.save()
    return render(request, 'shop/contactus.html')
def productlist(request):
    data = cartData(request)
    items = data['items']
    cartItems = data['cartItems']
    allProds = []
    catprods = Product.objects.values('category', 'id')
    # <QuerySet [{'category': 5, 'id': 1}, {'category': 5, 'id': 2}, {'category': 5, 'id': 3}]>
    cats = sorted({item['category'] for item in catprods})
    # [5]
    for cat in cats:
        # print(cat)
        prod = Product.objects.filter(category=cat)
        # <QuerySet [<Product: Walnut With Shell Superior>, <Product: Almonds Jumbo Size>, <Product: Cashew Nuts Half>]>
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    #Product.objects.aggregate(Min('offer_price'), Max('offer_price'))
    productTypevalue = request.GET.get('productType', 1)
    productType = ProductType.objects.get(id = productTypevalue)
    myProductTypeFilter = ProductTypeFilter(request.GET, queryset=ProductType.objects.all().values_list('pk', flat=True).distinct())
    print("myProductTypeFilter", myProductTypeFilter)
    print("productTypevalue", productTypevalue)
    minMaxPrice= SubProduct.objects.filter(productType= productTypevalue).aggregate(Min('offer_price'), Max('offer_price'))
    #Product.objects.all().values_list('category', flat=True).distinct()
    myFilter = ProductFilter(request.GET, queryset=Product.objects.filter(pk__in = SubProduct.objects.all().values_list('product', flat=True).distinct()).values_list('category', flat=True).distinct())
    print("myFilter",myFilter)
    requestCategory = request.GET.get('category', None)
    print("requestcategory", requestCategory)
    if not (requestCategory=="on" or requestCategory==None):
        if myFilter.is_valid:

            for i in myFilter.qs:
                # a = Product.objects.filter(category=i)
                # print("a", a)
                # minMaxPrice = a.aggregate(Min('offer_price'), Max('offer_price'))
                x = []
                for j in Product.objects.filter(category=i):
                    x.append(SubProduct.objects.filter(product = j, productType= productTypevalue))
                a = reduce(lambda y, z : y|z, x)#x[0].union(*x[1:])
                print("a", a)
                minMaxPrice = a.aggregate(Min('offer_price'), Max('offer_price'))



    # products = Product.objects.all()
    # # print(products)
    # n = len(products)
    # nSlides = n // 4 + ceil((n / 4) - (n // 4))
    # allProds = [[products, range(0, nSlides), nSlides],
    #             [products, range(0, nSlides), nSlides]]
    # print(allProds)
    # minMaxPrice['offer_price__min'] = int(minMaxPrice['offer_price__min'])
    # minMaxPrice['offer_price__max'] = int(minMaxPrice['offer_price__max'])

    params = {'allProds': allProds, 'cartItems':cartItems, 'items':items, 'myFilter': myFilter, 'minMaxPrice':minMaxPrice, 'ProductTypeFilter':myProductTypeFilter}
    params['wholesaleObj'] = ProductType.objects.get(type="Wholesale")
    params['productTypevalue'] = productTypevalue
    params['productType'] = productType
    if request.is_ajax():
        print("(###################################################################")
        is_requestAvailable = all(x  in request.GET for x in['minPrice','maxPrice'])

        if is_requestAvailable:
            prod_Price_Range = request.GET.get('minPrice', minMaxPrice['offer_price__min']), request.GET.get('maxPrice', minMaxPrice['offer_price__max'])
            params['prod_Price_Range'] = prod_Price_Range
        params['prod_Price_Range'] = params.get('prod_Price_Range', ())
        print(params)
        return render(request, 'shop/dup-prod-list.html', params)

    prod_Price_Range = request.GET.get('minPrice', minMaxPrice['offer_price__min']), request.GET.get('maxPrice', minMaxPrice['offer_price__max'])
    params['prod_Price_Range'] = prod_Price_Range
    return render(request, 'shop/product-list.html', params)

def productsingle(request, myid):
    wholesale = request.GET.get('Wholesale', 'true')
    print(type(wholesale))
    print(wholesale)
    itemIn = False
    if wholesale == 'false':
        subprod = SubProduct.objects.filter(product = Product.objects.get(id = myid), productType = ProductType.objects.get(type = "Retail")).first()
    else:
        subprod = SubProduct.objects.filter(product = Product.objects.get(id = myid), productType = ProductType.objects.get(type = "Wholesale")).first()
    print("subprod = ",subprod.id)
    data = cartData(request)
    items = data['items']
    cartItems = data['cartItems']
    productSelected_item = []
    if request.user.is_authenticated:
        productIdList = list(items.values_list('subProduct',flat = True))
        if subprod.id in productIdList:
            itemIn = True
            productSelected_item = items.filter(subProduct =subprod.id).first()
            FR_FIELD = productSelected_item.weightSelected
    else:
        print('items in single',items)
        productIdList = [d['subProduct']['id'] for d in items]
        print('productIdList', productIdList)
        if subprod.id in productIdList:
            itemIn = True
            productSelected_item = [d for d in items if d['subProduct']['id']==subprod.id][0]
            FR_FIELD = productSelected_item['weightSelected']

    product = Product.objects.filter(id= myid)
    if not productSelected_item:
        productSelected_item = {'get_total':subprod.offer_price, 'get_actual_total':subprod.actual_price, 'quantity': 0, 'subProduct': subprod}
        # DEPENDENT_FILED = DB.OBJECT.ALL() # field which has all the drop-down values.
        FR_FIELD = subprod.price_weight # selected drop-down from template


    nid = subprod.id #product[0].id
    prodRelated = SubProduct.objects.filter(~Q(id= nid),product__in=Product.objects.filter(category=subprod.product.category).values_list('pk',flat=True), productType= subprod.productType)#ProductType.objects.get(type="Retail"))#Product.objects.filter( ~Q(id= nid), category=product[0].category)

    p = subprod
    t, created = Weightage.objects.get_or_create(weight=p.price_weight.weight)
    p.available_weights.add(t)
    # print("productSelected_item.subProduct.id", productSelected_item.subProduct.id)
    if request.is_ajax():
        print("I am in ajax")
        return render(request, 'shop/product-singledetailsChange.html', {'productSelected':product[0], 'productSimilar' : prodRelated, 'cartItems':cartItems, 'items':items, 'productSelected_item':productSelected_item, 'FR_FIELD': FR_FIELD, 'wholesale': wholesale, 'itemIn':itemIn})
    return render(request, 'shop/product-single.html', {'productSelected':product[0], 'productSimilar' : prodRelated, 'cartItems':cartItems, 'items':items, 'productSelected_item':productSelected_item, 'FR_FIELD': FR_FIELD, 'wholesale': wholesale, 'itemIn':itemIn})

def RelatedProduct(request, myid):
    wholesale = request.GET.get('Wholesale', 'true')
    if wholesale == 'false':
        subprod = SubProduct.objects.filter(product = Product.objects.get(id = myid), productType = ProductType.objects.get(type = "Retail")).first()
    else:
        subprod = SubProduct.objects.filter(product = Product.objects.get(id = myid), productType = ProductType.objects.get(type = "Wholesale")).first()
    nid = subprod.id
    prodRelated = SubProduct.objects.filter(~Q(id= nid),product__in=Product.objects.filter(category=subprod.product.category).values_list('pk',flat=True), productType= subprod.productType)
    return render(request, 'shop/product-singleRelatedProducts.html', {'productSimilar' : prodRelated, 'wholesale': wholesale})
# AJAX
def load_price(request):
    weightSelected = request.GET.get('weight')
    productId = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity'))
    product = Product.objects.filter(pk = productId).first()
    subproductId = request.GET.get('subproductId')
    subproduct = SubProduct.objects.filter(pk = subproductId).first()
    print("subproduct in load_price", subproduct.id)
    price = subproduct.offer_price
    actual_price = subproduct.actual_price
    price_weight = subproduct.price_weight.weight
    if 'kgs' in weightSelected and 'gms' in weightSelected:
        li = weightSelected.split(' kgs ')
        k = int(li[0])
        g = int(li[1].strip(' gms'))
        selectedWght = k + g/1000
    elif 'kg' in weightSelected and 'gms' in weightSelected:
        li = weightSelected.split(' kg ')
        k = int(li[0])
        g = int(li[1].strip(' gms'))
        selectedWght = k + g/1000
    elif 'kgs' in weightSelected and 'gms' not in weightSelected:
        selectedWght = int(weightSelected.strip(' kgs'))
    elif 'kg' in weightSelected and 'gms' not in weightSelected:
        selectedWght = int(weightSelected.strip(' kg'))
    elif 'gms' in weightSelected and 'kg' not in weightSelected and 'kgs' not in weightSelected:
        selectedWght = int(weightSelected.strip(' gms'))/1000

    x = (price * selectedWght) / price_weight
    y = (actual_price * selectedWght) / price_weight


    if quantity:
        if request.user.is_authenticated:
            customer = request.user.customer
            if not customer:
                customer, created = Customer.objects.get_or_create(user = request.user)
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
            orderItem, created = OrderItem.objects.get_or_create(subProduct=subproduct, order=order, quantity=quantity)
            o = functionOrderItem(request, selectedWght, orderItem.id)
        else:
            pass
    # data = cartData(request)
    # items = data['items']
    # if request.user.is_authenticated:
    #     productIdList = list(items.values_list('product',flat = True))
    #     if productId in productIdList:
    #        productSelected_item = items.filter(product =productId).first()
    #        productSelected_item.
    # else:
    #     productIdList = [d['id'] for d in items]
    #     if productId in productIdList:
    #         productSelected_item = [d for d in items if d['id']==productId][0]

    return JsonResponse(f'{x} - {y}', safe=False)


def payment(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'shop/payment.html', context)

def cart(request):

    data = cartData(request)
    print('data in cart',data)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order': order, 'cartItems': cartItems}
    print('context',context)
    if request.is_ajax():
        return render(request, 'shop/dup-cart.html', context)
    return render(request, 'shop/cart.html', context)

def orderHistory(request):
    if request.user.is_authenticated:
        data = cartData(request)
        # order = data['order']
        ordersHistory = data['ordersHistory']
        cartItems = data['cartItems']
        context = {'ordersHistory': ordersHistory, 'cartItems': cartItems}
    else:
        context = {}
        print("context")
        if request.is_ajax():
            print("ajax data")
            emaildata = request.POST.get('email', None)#json.loads(request.body)
            print("data",emaildata)
            # emaildata = data['email']
            customer, created = Customer.objects.get_or_create(email = emaildata)
            ordersHistory = Order.objects.filter(customer=customer)
            context = {'ordersHistory': ordersHistory}
            print("context-OrderHistory", context)
            return render(request, 'shop/dup-orders-history.html',context)
    return render(request, 'shop/orders-history.html', context)

def trackOrder(request, mytrackid):
    order = Order.objects.get(order_id = mytrackid)
    items = OrderItem.objects.filter(order=order, subProduct__isnull=False)
    return render(request, 'shop/track-order.html', { 'items': items, 'order': order })

# def answer_me(request):
#     data = cartData(request)

#     cartItems = data['cartItems']
#     order = data['order']
#     items = data['items']
#     data = {'items':items, 'order': order, 'cartItems': cartItems}
#     return JsonResponse(data, safe=False)

# @login_required
@csrf_exempt
def get_phases(request):
    productId = request.POST.get('product')
    print("product",productId)
    phases = {}
    try:
        if productId:
            print(SubProduct.objects.values_list('product', 'productType'))
            productTypes ={product: productType for product, productType in SubProduct.objects.values_list('product', 'productType')}
            if int(productId) in productTypes:
                print(productTypes[int(productId)])
                include = ProductType.objects.exclude(pk = productTypes[int(productId)])
                print('include',include)
            else:
                include = ProductType.objects.all()

            print("_____", "here in project")
            # prophases = Product.objects.get(pk=int(product)).phase
            # phases = {pp.phase.title:pp.pk for pp in prophases}
        else:
            include = ProductType.objects.all()
        
    except:
        include = ProductType.objects.all()
        pass
    return JsonResponse(data={"includeQuery":serializers.serialize('json',include)}, safe=False)