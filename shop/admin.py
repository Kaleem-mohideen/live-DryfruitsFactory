from django.contrib import admin

# Register your models here.
from .models import *
from django.db.models import Count, Q
from functools import partial
from django.forms.models import modelformset_factory
from .forms import *

# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
# admin.site.register(ProductType)

admin.site.register(Contact)
# admin.site.register(Category)
# admin.site.register(Weightage)

# @admin.register(SubProduct)
class MySubProductModel(admin.ModelAdmin):
    model = SubProduct
    ordering = ['product', 'productType']
    list_display = ( 'product', 'productType', 'offer_price', 'actual_price', 'price_weight', 'ava_quantity', 'enabled')
    filter_horizontal = ('available_weights',)

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj # Capture instance before the form gets generated
        print("self.instance",self.instance)
        return super(MySubProductModel, self).get_form(request, obj=obj, **kwargs)
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        print("db",db_field)
        if db_field.name == 'product' and not self.instance:
            a = [product_id for product_id, count in SubProduct.objects.values_list('product').annotate(cc=Count('product')) if count==2]
            kwargs['queryset'] = Product.objects.exclude(pk__in = a)
        # if db_field.name == 'productType':
        #     kwargs['queryset'] = 
            
        return super(MySubProductModel, self).formfield_for_foreignkey(db_field, request=request, **kwargs)

    class Media:
        js = ("shop/js/selectajax.js",)
admin.site.register(SubProduct, MySubProductModel)


@admin.register(Weightage)
class MyWeightageModel(admin.ModelAdmin):
    model = Weightage
    ordering = ['weight']
    list_display = ( 'weight', 'enabled', 'id')

@admin.register(ShippingAddress)
class MyShippingAddressModel(admin.ModelAdmin):
    model = ShippingAddress
    list_display = ( 'customer', 'order', 'address', 'city', 'state', 'zipcode', 'date_added')

@admin.register(Product)
class MyProductModel(admin.ModelAdmin):
    model = Product
    list_display = ( 'product_name', 'image', 'category', 'enabled', 'desc')


# admin.site.register(SubProduct)

@admin.register(Category)
class MyCategoryModel(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'category_name', 'enabled')

@admin.register(Customer)
class MyCustomerModel(admin.ModelAdmin):
    model = Customer
    list_display = ('user', 'name', 'email')

@admin.register(OrderItem)
class MyOrderItemModel(admin.ModelAdmin):
    model = OrderItem
    list_display = ('subProduct', 'order', 'quantity', 'weightSelected', 'get_total', 'date_added')

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj # Capture instance before the form gets generated
        return super(MyOrderItemModel, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'weightSelected' and self.instance:
            # restrict role queryset to those related to this instance:
            kwargs['queryset'] = self.instance.subProduct.available_weights.all()
            # kwargs['initial'] = self.instance.product.price_weight
        return super(MyOrderItemModel, self).formfield_for_foreignkey(db_field, request=request, **kwargs)

@admin.register(StatusTrack)
class MyStatusTrackModel(admin.ModelAdmin):
    readonly_fields = ('status', )
    def has_add_permission(self, request):
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and StatusTrack.objects.all().count()>=2:
            retVal = False
        return retVal

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ProductType)
class MyProductTypeModel(admin.ModelAdmin):
    readonly_fields = ('type', )
    def has_add_permission(self, request):
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and ProductType.objects.all().count()>=2:
            retVal = False
        return retVal

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(DeliveryCharge)
class MyDeliveryChargeModel(admin.ModelAdmin):

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and DeliveryCharge.objects.exists():
            retVal = False
        return retVal
        # return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(GSTCharge)
class MyGSTChargeModel(admin.ModelAdmin):

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and GSTCharge.objects.exists():
            retVal = False
        return retVal
        # return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Order)
class MyOrderModel(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'customer', 'get_cart_total_with_deliverycharge', 'complete', 'status', 'get_cart_total', 'deliverycharge', 'gstcharge', 'date_ordered', 'order_id', 'transaction_id')
    list_filter = ('customer', 'complete')
    search_fields = ['customer__email', 'customer__name', 'date_ordered']
    list_editable = ['status']
    radio_fields = {"status": admin.VERTICAL}
    # readonly_fields = ('complete', )
    def get_exclude(self, request, obj=None):
        if obj and obj.complete == False:
            # When you create new data the obj is None
            return ("status", )
        return super().get_exclude(request, obj)
    def get_changelist_form(self, request, **kwargs):
        return OrderStatusChangeListForm

    # def get_readonly_fields(self, request, obj=None):
    #     if obj and obj.complete == False:
    #         return ["status"]
    #     else:
    #         return []

# admin.site.register(Order, MyOrderModel)
# The file where you configure your admin
# admin.site.register(Order, MyModelAdmin)
