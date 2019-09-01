from django.db import models
from django.contrib.auth.models import User


class Cargo(models.Model):
    wrapping = models.CharField(max_length=256, default="")
    pallets_number = models.IntegerField()
    remarks = models.TextField(max_length=256, default="")


class SimpleAddress(models.Model):
    place_name = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    post_code = models.CharField(max_length=128)
    post_place = models.CharField(max_length=256)
    country = models.CharField(max_length=128)


class ExtendAddress(models.Model):
    date = models.DateTimeField()
    hour = models.CharField(max_length=32)
    place = models.ForeignKey(SimpleAddress, on_delete=models.SET_NULL, null=True)
    palette_number = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(max_length=256, default="")


class BestTransData(models.Model):
    address = models.OneToOneField(SimpleAddress, on_delete=models.CASCADE)
    tax_number = models.CharField(default="123 456 78 90", max_length=32)
    email = models.CharField(default='kontakt@besttrans.com.pl', max_length=32)
    phone_number = models.CharField(default='111222333', max_length=32)


class Company(models.Model):
    address = models.ForeignKey(SimpleAddress, on_delete=models.SET_NULL, null=True, blank=True)
    tax_number = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    tax_number = models.CharField(max_length=64, null=True, blank=True)
    address = models.ForeignKey(SimpleAddress, on_delete=models.SET_NULL, null=True, blank=True)


class Driver(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    card_drive_number = models.CharField(max_length=64)
    address = models.ForeignKey(SimpleAddress, on_delete=models.SET_NULL, null=True)


class Vehicle(models.Model):
    brand = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    kind = models.CharField(max_length=64, null=True, blank=True)
    registration_number = models.CharField(max_length=32)


class Offer(models.Model):
    loading_place = models.OneToOneField(ExtendAddress, related_name='loading_place_offer', on_delete=models.SET_NULL,
                                         null=True)
    destination = models.OneToOneField(ExtendAddress, related_name='destination_place_offer', on_delete=models.SET_NULL,
                                       null=True)
    pallets_number = models.IntegerField()
    vehicles = models.ManyToManyField(Vehicle, through='OffersVehicles', through_fields=('offer', 'vehicle'))
    remarks = models.TextField(max_length=512, default="")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    is_active = models.BooleanField(default=True)
    language = models.CharField(max_length=32, null=True, blank=True)


class OffersVehicles(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    performer = models.ForeignKey(BestTransData, on_delete=models.SET_NULL, null=True)
    offers = models.ManyToManyField(Offer, through='OrdersOffers', through_fields=('order', 'offer'), blank=True)
    loading_places = models.ManyToManyField(ExtendAddress, related_name='order_loading_places',
                                            through='OrdersLoadingPlaces', through_fields=('order', 'loading_place'))
    destinations = models.ManyToManyField(ExtendAddress, related_name='order_destination_places',
                                          through='OrdersDestinationPlaces', through_fields=('order', 'destination_place'))
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)
    drivers = models.ManyToManyField(Driver, through='OrdersDrivers', through_fields=('order', 'driver'),
                                     blank=True)
    vehicles = models.ManyToManyField(Vehicle, through='OrdersVehicles', through_fields=('order', 'vehicle'),
                                      blank=True)
    remarks = models.TextField(max_length=256, default="")
    price = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)


class OrdersOffers(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True)


class OrdersLoadingPlaces(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    loading_place = models.ForeignKey(ExtendAddress, on_delete=models.SET_NULL, null=True)


class OrdersDestinationPlaces(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    destination_place = models.ForeignKey(ExtendAddress, on_delete=models.SET_NULL, null=True)


class OrdersDrivers(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)


class OrdersVehicles(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)


class ResponseToCustomer(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField(max_length=500)
    date = models.DateTimeField()
    readed = models.BooleanField(default=False)
    receiver = models.ManyToManyField(Profile, related_name='responses_profiles', through='ResponsesProfiles',
                                      through_fields=('response', 'profile'))


class ResponsesProfiles(models.Model):
    response = models.ForeignKey(ResponseToCustomer, on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)


class Inquiry(models.Model):
    title = models.CharField(max_length=64)
    customer = models.ForeignKey(Profile, related_name='inquiries_customer', on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey(User, related_name='inquiries_admin', on_delete=models.SET_NULL, null=True)
    text_or_remarks = models.TextField(max_length=500)
    date = models.DateTimeField()
    email = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    readed = models.BooleanField(default=False)
    offers = models.ManyToManyField(Offer, related_name='inquiries_offers', through='InquiriesOffers',
                                    through_fields=('inquiry', 'offer'), blank=True)
    orders = models.ManyToManyField(Order, related_name='inquiries_orders', through='InquiriesOrders',
                                    through_fields=('inquiry', 'order'), blank=True)
    responses = models.ManyToManyField(ResponseToCustomer, related_name='inquiries_responses', through='InquiriesResponses',
                                       through_fields=('inquiry', 'response'), blank=True)


class InquiriesOffers(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.SET_NULL, null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True)


class InquiriesOrders(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)


class InquiriesResponses(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.SET_NULL, null=True)
    response = models.ForeignKey(ResponseToCustomer, on_delete=models.SET_NULL, null=True)
