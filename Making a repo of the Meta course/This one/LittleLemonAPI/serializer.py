from rest_framework import serializers
from .models import MenuItem, Cart, OrderItem, Order

class Myserializer(serializers.ModelSerializer):
    #category = serializers.StringRelatedField()
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category']
        depth=1

class Manager(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
        
class Cartserializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='cal_price', read_only=True)
    def cal_price(self, a:Cart):
        return a.unit_price * a.quantity

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price','price']

class orderserializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total', 'date']

class orderserializer1(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total', 'date', 'delivery_crew']

class Orderitemserializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
       