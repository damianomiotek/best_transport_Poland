from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class SimpleAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleAddress
        fields = '__all__'


class ExtendAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendAddress
        fields = '__all__'


class BestTransDataSerializer(serializers.ModelSerializer):
    address = SimpleAddressSerializer(many=False)

    class Meta:
        model = BestTransData
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    address = SimpleAddressSerializer(many=False)

    class Meta:
        model = Company
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    address = SimpleAddressSerializer(many=False)

    class Meta:
        model = Profile
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class OffersVehiclesSerializer(serializers.ModelSerializer) :
    class Meta:
        model = OffersVehicles
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    loading_place = ExtendAddressSerializer()
    destination = ExtendAddressSerializer()
    vehicles = OffersVehiclesSerializer(many=True)

    class Meta:
        model = Offer
        fields = '__all__'


class OrdersOffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersOffers
        fields = '__all__'


class OrdersLoadingPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersLoadingPlaces
        fields = '__all__'


class OrdersDestinationPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersDestinationPlaces
        fields = '__all__'


class OrdersDriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersDrivers
        fields = '__all__'


class OrdersVehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersVehicles
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    performer = BestTransDataSerializer(many=False)
    offer = OrdersOffersSerializer(source='offer', many=True)
    loading_places = OrdersLoadingPlacesSerializer(source='loading_place', many=True)
    destinations = OrdersDestinationPlacesSerializer(source='destination_place', many=True)
    drivers = OrdersDriversSerializer(source='driver', many=True)
    vehicles = OrdersVehiclesSerializer(source='vehicle', many=True)

    class Meta:
        model = Order
        fields = '__all__'


class ResponsesProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsesProfiles
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    receiver = ResponsesProfilesSerializer(source='profile', many=True)

    class Meta:
        model = ResponseToCustomer
        fields = '__all__'


class InquiriesOffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiriesOffers
        fields = '__all__'


class InquiriesOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiriesOrders
        fields = '__all__'


class InquiriesResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiriesResponses
        fields = '__all__'


class InquirySerializer(serializers.ModelSerializer):
    offers = InquiriesOffersSerializer(source='coffer', many=True)
    orders = InquiriesOrdersSerializer(source='order', many=True)
    responses = InquiriesResponsesSerializer(source='response', many=True)

    class Meta:
        model = Inquiry
        fields = '__all__'
