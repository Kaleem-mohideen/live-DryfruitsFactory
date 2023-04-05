import django_filters

from .models import *
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _


class ProductFilter(django_filters.FilterSet):
    # category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit();'}))
    category = django_filters.ChoiceFilter(choices=[], label='Category', empty_label=None, widget=forms.RadioSelect(attrs={'class': 'form-control'})) #'onchange': 'this.form.submit();'
    print("category",category)

    class Meta:
        model = Product
        fields = ['category']
        # filter_overrides = {
        # models.CharField:{
        # 'filter_class' : django_filters.ChoiceFilter,
        # 'extra' : lambda f: {
        # 'widget': forms.RadioSelect
        # }
        # }
        # }

    def __init__(self, *args, **kwargs):
            super(ProductFilter, self).__init__(*args, **kwargs)
            try:
                # print(args[0])
                # print("kwargs",kwargs)
                self.filters['category'].extra['choices'] = [(Category.objects.get(id=x).id, Category.objects.get(id=x)) for x in Product.objects.filter(pk__in = SubProduct.objects.all().values_list('product', flat=True).distinct()).values_list('category', flat=True).distinct() if x is not None] #Product.objects.all().values_list('category', flat=True).distinct()
                # print("self.filters['category'].extra['choices']",self.filters['category'].extra['choices'])
            except (KeyError, AttributeError):
                pass

class ProductTypeFilter(django_filters.FilterSet):
    productType = django_filters.ChoiceFilter(choices=[], label='ProductType',  empty_label=None, widget=forms.RadioSelect(attrs={'class': 'form-control1'}))
    print("productType",productType)
    class Meta:
        model = SubProduct
        fields = ['productType']


    def __init__(self, data=None, *args, **kwargs):
        print('data', data)
        if not data:
            data = data.copy()
            data.setdefault("productType", ProductType.objects.get(type='Retail').id)
            print("-==-=-==-==--==-==-data",data)
        super(ProductTypeFilter, self).__init__(data, *args, **kwargs)
        # self.initial['idparent']   = self.instance.parent_identity()
        try:
            # print('data',data)
            # print("kwargs",kwargs)
            self.filters['productType'].extra['choices'] = [(x.id, x) for x in ProductType.objects.all()]
            # print("self.filters['productType'].extra['choices']",self.filters['productType'].extra['choices'])
        except (KeyError, AttributeError) as e:
            # print("")
            pass

