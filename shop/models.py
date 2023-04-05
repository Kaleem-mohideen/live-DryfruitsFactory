from django.db import models
# from django.contrib.auth.models import User
from django.apps import apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
import django.dispatch
from django.conf import settings

# from django.utils.translation import gettext as _
# from shop.models import Order
# Create your models here.

# def default_subject(sender, instance, using):
#     instance.price = instance.product.price_weight.weight
# pre_save.connect(default_subject, sender=OrderItem)

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.email
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Weightage(models.Model):
    weight = models.FloatField(max_length=200, unique=True, validators = [MinValueValidator(0.001)])
    enabled = models.BooleanField(default=True)

    def __str__(self):
        kilograms = int(self.weight)
        grams = (self.weight - kilograms) * 1000
        kg, g = int(kilograms), int(grams % 1000)
        if kg == 0:
            return f'{g} gms'
        elif g == 0:
            if kg == 1:
                return f'{kg} kg'
            return f'{kg} kgs'
        elif kg == 1:
            return str(f'{kg} kg {g} gms')
        return str(f'{kg} kgs {g} gms')


class DeliveryCharge(models.Model):
    delivery_charge = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return str(self.delivery_charge)

class GSTCharge(models.Model):
    gst_charge = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return str(self.gst_charge)

class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context=None):
        if value is None:
            return value
        return int(value) # return 0/1

class ProductType(models.Model):
    # completed = CustomBooleanField()
    type = models.CharField(max_length=200, default = "", verbose_name='Product Available In')
    def __str__(self):
        return  str(self.type)

class StatusTrack(models.Model):
    # completed = CustomBooleanField()
    status = models.CharField(max_length=200, default = "", verbose_name='Product Status')
    def __str__(self):
        return  str(self.status)

class MyModelManager(models.Manager):
    def get_queryset(self):
        self.model.list_delivery_charge = DeliveryCharge.objects.all()
        self.model.list_gst_charge = GSTCharge.objects.all()
        self.model.list_subproduct = SubProduct.objects.all()
        return super(MyModelManager, self).get_queryset()

class Product(models.Model):
    # Categories = (('1', 'Dry Fruit Mix'), ('2','Dry Fruits'), ('3', 'Seeds'), ('4', 'Spices'), ('5','Gift Box'))
    product_id = models.AutoField
    product_name = models.CharField(max_length=200)
    # ava_quantity = models.PositiveIntegerField(default = 100, verbose_name='Each user can choose Quantity of this Product upto')
    desc = models.TextField(max_length=500, default="", verbose_name='Description')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Published date')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'enabled': True})
    # offer_price = models.FloatField()
    # actual_price = models.FloatField()
    # price_weight = models.ForeignKey(Weightage, on_delete=models.SET_NULL, null=True, related_name='price_weight', db_column='price_weight', limit_choices_to={'enabled': True})
    digital = models.BooleanField(default=False,null=True, blank=True)
    enabled = models.BooleanField(default=True,null=True, blank=True)
    image = models.ImageField(upload_to= "shop/images", null=True, blank=True)
    # available_weights = models.ManyToManyField(Weightage, related_name='available_weights', db_column='available_weights', null=True, blank=True, limit_choices_to={'enabled': True})

    objects = models.Manager()
    subproducts_objects = MyModelManager()
    default_changes = None

    def __str__(self):
        return  self.product_name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/media/shop/images/blank.png'
        return url


def default_changes(sender, instance, *args, **kwargs):
    print('instance.primary_key',instance)
    print(id(instance), id(None))
    try:
        if not instance.enabled:
            
            # print('subproducts_objects', subproducts_objects)
            modelManagerObject =sender.subproducts_objects.all()
            print('modelManagerObject', modelManagerObject)
            subproductObject = modelManagerObject.model.list_subproduct.all()
            print('subproductObject', subproductObject.filter(product = instance))
            qs = subproductObject.filter(product = instance)
            qs.update(enabled=False)

    except AttributeError:
        print('AttributeError')
        pass
post_save.connect(default_changes, sender=Product)

class SubProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    productType = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, verbose_name='Product Available In')
    offer_price = models.FloatField()
    actual_price = models.FloatField()
    price_weight = models.ForeignKey(Weightage, on_delete=models.SET_NULL, null=True, related_name='price_weights', db_column='price_weight', limit_choices_to={'enabled': True})
    ava_quantity = models.PositiveIntegerField(default = 100, verbose_name='Each user can choose Quantity of this Product upto')
    enabled = models.BooleanField(default=True,null=True, blank=True)
    available_weights = models.ManyToManyField(Weightage, related_name='available_weight', db_column='available_weight', null=True, blank=True, limit_choices_to={'enabled': True})
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Created date')

    def __str__(self):
        return str(self.product)

    @property
    def offer_percentage(self):
        total = 100 * (self.actual_price - self.offer_price) / self.actual_price
        return total

@django.dispatch.receiver(models.signals.post_init, sender=SubProduct)
def set_default_product_initials(sender, instance, *args, **kwargs):
    """
    Set the default value for `available_weights` on the `instance`.

    :param sender: The `SubProduct` class that sent the signal.
    :param instance: The `SubProduct` instance that is being
        initialised.
    :return: None.
    """

    if instance.pk:
        instance.available_weights.add(instance.price_weight.id)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    order_id = models.CharField(max_length=10000, null=True)
    transaction_id = models.CharField(max_length=50000, null=True)
    status = models.ForeignKey(StatusTrack, on_delete=models.SET_NULL, null=True, blank=True)
    # delivery_charge = models.ForeignKey(DeliveryCharge, on_delete=models.SET_DEFAULT, null=True)

    objects = models.Manager()
    extracharge_objects = MyModelManager()
    get_cart_total_with_deliverycharge = None
    deliverycharge = None
    gstcharge = None
    def __str__(self):
        return str(self.id)


    # @property
    def get_cart_total_with_deliverycharge(self):
        # modelManagerObject =Order.extracharge_objects.all()
        # # modelManagerObject =Order.extracharge_objects
        # print(modelManagerObject)
        # transportCharge_first = modelManagerObject.model.list_delivery_charge.first()
        if not self.deliverycharge and not self.gstcharge:#transportCharge_first.delivery_charge:
            return self.get_cart_total
        elif not self.deliverycharge and self.gstcharge:
            return self.get_cart_total + int(self.gstcharge)
        elif not self.gstcharge and self.deliverycharge:
            return self.get_cart_total + int(self.deliverycharge)
        total = self.get_cart_total + int(self.deliverycharge) + int(self.gstcharge)#transportCharge_first.delivery_charge)
        return total
    get_cart_total_with_deliverycharge.short_description = 'Total (including DeliveryCharge and GST)'
    get_cart_total_with_deliverycharge = property(get_cart_total_with_deliverycharge)
    # @property
    def deliverycharge(self):
        modelManagerObject =Order.extracharge_objects.all()

        transportCharge_first = modelManagerObject.model.list_delivery_charge.first()
        if not transportCharge_first.delivery_charge:
            return 0
        return transportCharge_first.delivery_charge
    deliverycharge.short_description = 'Delivery Charge'
    deliverycharge = property(deliverycharge)

    def gstcharge(self):
        modelManagerObject =Order.extracharge_objects.all()

        taxCharge_first = modelManagerObject.model.list_gst_charge.first()
        if not taxCharge_first.gst_charge:
            return 0
        return taxCharge_first.gst_charge
    gstcharge.short_description = 'GST Charge'
    gstcharge = property(gstcharge)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.subProduct.product.digital == False:
                shipping = True
        return shipping

    # @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    get_cart_total.short_description = 'Cart Total'
    get_cart_total = property(get_cart_total)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cartSavingsfrom_actual_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_savings_total for item in orderitems])
        return total
        
    # @property
    def get_cart_actual_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_actual_total for item in orderitems])
        return total
    get_cart_actual_total.short_description = 'Cart Actual Total'
    get_cart_actual_total = property(get_cart_actual_total)
        
    

class OrderItem(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    subProduct = models.ForeignKey(SubProduct, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    weightSelected = models.ForeignKey(Weightage, on_delete=models.SET_NULL, null=True,db_constraint=False) #models.ManyToManyField('Weightage', through='Product')

    @classmethod
    def get_default_orderitem_weight(self):
        """ get a default value for action status; create new status if not available """
        return self.subProduct.price_weight.weight

    @property
    def get_total(self):
        total = ((self.subProduct.offer_price * self.weightSelected.weight) /self.subProduct.price_weight.weight) * self.quantity
        return total

    @property
    def get_savings_total(self):
        total = (((self.subProduct.actual_price-self.subProduct.offer_price) * self.weightSelected.weight) /self.subProduct.price_weight.weight) * self.quantity
        return total

    @property
    def get_actual_total(self):
        total = ((self.subProduct.actual_price * self.weightSelected.weight) /self.subProduct.price_weight.weight) * self.quantity
        return total

@django.dispatch.receiver(models.signals.post_init, sender=OrderItem)
def set_default_orderitem_initials(sender, instance, *args, **kwargs):
    """
    Set the default value for `subject_initials` on the `instance`.

    :param sender: The `LoremIpsum` class that sent the signal.
    :param instance: The `LoremIpsum` instance that is being
        initialised.
    :return: None.
    """
    # print("instance.weightSelected", instance.weightSelected)
    if not instance.weightSelected:
        # print(instance.subProduct)
        instance.weightSelected = instance.subProduct.price_weight

#     @classmethod
#     def get_default_orderitem_weight(self):
#         """ get a default value for action status; create new status if not available """
#         return self.product.price_weight.weight

#     @property
#     def get_total(self):
#         total = ((self.product.offer_price * self.weightSelected.weight) /self.product.price_weight.weight) * self.quantity
#         return total

#     @property
#     def get_savings_total(self):
#         total = (((self.product.actual_price-self.product.offer_price) * self.weightSelected.weight) /self.product.price_weight.weight) * self.quantity
#         return total

#     @property
#     def get_actual_total(self):
#         total = ((self.product.actual_price * self.weightSelected.weight) /self.product.price_weight.weight) * self.quantity
#         return total

# @django.dispatch.receiver(models.signals.post_init, sender=OrderItem)
# def set_default_orderitem_initials(sender, instance, *args, **kwargs):
#     """
#     Set the default value for `subject_initials` on the `instance`.

#     :param sender: The `LoremIpsum` class that sent the signal.
#     :param instance: The `LoremIpsum` instance that is being
#         initialised.
#     :return: None.
#     """
#     if not instance.weightSelected:
#         instance.weightSelected = instance.product.price_weight

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    msg = models.CharField(max_length=500, default="")
    phone = models.CharField(max_length=16, default="")


    def __str__(self):
        return  self.name
