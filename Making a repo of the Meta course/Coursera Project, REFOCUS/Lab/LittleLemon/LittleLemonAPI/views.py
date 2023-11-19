from rest_framework import generics

from .models import Category, MenuItem

from .serializers import CategorySerializer, MenuItemSerializer, UserSerializer, UserCartSerializer, OrdersSerializer

from django.contrib.auth.models import User, Group

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class MenuItemOneView(generics.RetrieveUpdateDestroyAPIView, generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class ManagerUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class ManagerOneUserView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrdersSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class OrdersOneView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdersSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class DeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class DeliveryOneCrewView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class CustomerCartView(generics.ListCreateAPIView):
    serializer_class = UserCartSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
