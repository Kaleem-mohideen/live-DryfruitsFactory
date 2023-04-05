from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    path('', views.index, name= 'ShopHome'),
    path('aboutus/', views.aboutus, name= 'ShopAbout'),
    path('contactus/', views.contactus, name= 'ShopContact'),
    path('productlist/', views.productlist, name= 'Prod_list'),
    path('get_phases/', views.get_phases, name= 'get_phases'),
    path("productsingle/<int:myid>/", views.productsingle, name= 'Prod_single'),
    path("productsingleRelated/<int:myid>/", views.RelatedProduct, name= 'Prod_singleRelated'),
    path('payment/', views.payment, name= 'Payment'),
    path('cart/', views.cart, name= 'Cart'),
    path('update_item/', views.updateItem, name= 'update_item'),
    path('process_order/', views.processOrder, name="process_order"),
    # path('weight_process/', views.weightProcess, name="process_order"),
    path('ajax/load-price/', views.load_price, name='ajax_load_price'), # AJAX
    path('order-history/', views.orderHistory, name='orderHistory'),
    path('checkSwitchToggle/', views.checkSwitchToggle, name='checkSwitchToggle'),
    path(r"trackOrder/(?P<mytrackid>\d+\.\d{2})/$", views.trackOrder, name='track-order'),
    # path(r'^ajax/get_response/$', views.answer_me, name='get_response')
]
