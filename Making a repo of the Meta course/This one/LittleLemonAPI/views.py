from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import MenuItem, Cart, OrderItem, Order
from .serializer import Myserializer, Cartserializer, orderserializer, Orderitemserializer, orderserializer1, Manager
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q

@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def menuitems(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        ser = Myserializer(items, many=True)
        return Response(ser.data)
    elif request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists():
            ser_data = Myserializer(data=request.data)
            ser_data.is_valid(raise_exception=True)
            ser_data.save()
            return Response(ser_data.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'You are not allowed'}, status=status.HTTP_403_FORBIDDEN)
        
class Menuitem(generics.DestroyAPIView, generics.RetrieveUpdateAPIView, generics.ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    lookup_url_kwarg = 'menuItem'
    queryset = MenuItem.objects.all()
    serializer_class = Myserializer
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    

class Assign_Manager(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAdminUser]
    queryset = Group.objects.get(name='Manager').user_set.all()
    serializer_class = Manager
    def post(self, request):
        group = Group.objects.get(name='Manager')
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            group.user_set.add(user)
        return Response({'success'}, 201)
    
class Remove_manager(generics.RetrieveDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = 'userId'
    serializer_class = Manager
    queryset = Group.objects.get(name='Manager').user_set
    def delete(self, request, userId,*args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            group = Group.objects.get(name='Manager')
            user = User.objects.get(pk=userId)
            group.user_set.remove(user)
            return Response({"user successfully removed"})
        else:
            return Response({"Forbidden"}, 403)
    
    
class Assign_Delivery(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAdminUser]
    queryset = Group.objects.get(name='Delivery crew').user_set.all()
    serializer_class = Manager
    def post(self, request):
        group = Group.objects.get(name='Delivery crew')
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            group.user_set.add(user)
        return Response({'success'}, 201)

class Remove_delivery(generics.RetrieveDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = 'userId'
    serializer_class = Manager
    queryset = Group.objects.get(name='Delivery crew').user_set

    def delete(self, request, userId,*args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            group = Group.objects.get(name='Delivery crew')
            user = User.objects.get(pk=userId)
            group.user_set.remove(user)
            return Response({"user successfully removed"})
        else:
            return Response({"Forbidden"}, 403)
        
class cart(generics.DestroyAPIView, generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = Cartserializer
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        request.data._mutable = True
        request.data['user'] = user.id
        request.data._mutable = False
        return super().create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        Cart.objects.filter(user=user).delete()
        return Response({'success'}, 204)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def order_views(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
            orderitems = OrderItem.objects.select_related('order', 'menuitem').all()
            ser = orderserializer(orders, many=True)
            ser1 = Orderitemserializer(orderitems, many=True)
            return Response({'orders':ser.data,
                             'orderitems':ser1.data})
        
        elif request.user.groups.filter(name='Delivery crew').exists():
            user = request.user
            orders = Order.objects.filter(delivery_crew=user)
            orderitems = OrderItem.objects.select_related('order', 'menuitem')
            ser = orderserializer(orders, many=True)
            ser1 = Orderitemserializer(orderitems, many=True)
            return Response({'orders':ser.data,
                             'orderitems':ser1.data})
        
        else:
            user = request.user
            orders = Order.objects.filter(user=user)
            orderitems = OrderItem.objects.select_related('order', 'menuitem')
            ser = orderserializer(orders, many=True)
            ser1 = Orderitemserializer(orderitems, many=True)
            return Response({'orders':ser.data,
                             'orderitems':ser1.data})
    elif request.method == 'POST':
            user = request.user
            cart = Cart.objects.filter(user=user)
            cart_obj = Cart._meta.get_field('menuitem')
            if cart:
                menuitem = cart.menuitem
                quantity = cart.quantity
                price = cart.price
                unit_price = cart.unit_price
            ser = Orderitemserializer(data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            OrderItem.objects.create(user=user, menuitem=menuitem, quantity=quantity, price=price, unit_price=unit_price)
            return Response({"successfully created new order, cart items has also been added to order"}, 201)