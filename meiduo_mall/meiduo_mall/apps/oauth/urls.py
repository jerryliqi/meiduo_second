from django.conf.urls import url

from . import views


urlpatterns = [
    # 获取扫码url
    url(r'^qq/authorization/$', views.QQAuthorURLView.as_view()),
    # QQ登录认证
    url(r'^qq/user/$', views.QQAuthorUserView.as_view()),
]