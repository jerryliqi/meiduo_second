from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    # url(路径, 函数视图， name=路由的名称)
    # 如果没有指定base_name（路由名称前缀），它会去找queryset(查询集所指定的模型，以模型名小写做为路由名称前缀)
]

router = DefaultRouter()
router.register(r'areas', views.AreaViewSet, base_name="areas")
urlpatterns += router.urls
