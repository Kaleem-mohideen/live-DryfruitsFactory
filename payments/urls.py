from django.urls import path
from .views import initiate_payment, callback #, callbackResult

urlpatterns = [
    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
    # path(r'callbackResult/(?P<context>\d+\.\d{2})/$', callbackResult, name = 'callbackResult')
]
