from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    # 判断前端传入的用户名是否已经存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断前端传入的手机号是否已经存在
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 用户注册模块
    url(r'^users/$', views.UserView.as_view()),
    # jwt登录
    url(r'^authorizations/$', obtain_jwt_token),
    # 用户详情
    url(r'^user/$', views.UserDetailView.as_view()),
    # 发送邮箱
    url(r'^email/$', views.EmailView.as_view()),
    # 验证邮箱
    url(r'^email/verification/$', views.VerifyEmailView.as_view()),
]