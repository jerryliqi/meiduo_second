from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import CreateUserSerializer


# url(r'^users/$', views.CreateAPIView.as_view())
class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = CreateUserSerializer

# url('^usernames/(?P<username>\w{5, 20})/count$', views.UsernameCountView.as_view())
class UsernameCountView(APIView):
    def get(self, request, username):
        """
        判断前端传入的用户名是否已经存在
        :param request:
        :param username:
        """
        count = User.objects.filter(username=username).count()
        data = {
            "username": username,
            "count": count
        }

        return Response(data)


# url(r'^mobiles/(?P<mobile>1[3-9]/d{9})/count/$', views.MobileCountView.as_view())
class MobileCountView(APIView):

    def get(self, request, mobile):
        """判断前端传入的手机号是否已经存在"""
        count = User.objects.filter(mobile=mobile).count()
        data = {
            "mobile": mobile,
            "count": count
        }
        return Response(data)