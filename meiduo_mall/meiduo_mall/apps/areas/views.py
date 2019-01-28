from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Area
from .serializers import AreaSerializer, SubAreaSerializer


class AreaViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    行政区划信息
    """
    pagination_class = None

    def get_queryset(self):
        """指定查询集"""
        if self.action == "list":
            return Area.objects.filter(parent_id=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        """指定序列化器"""
        if self.action == "list":
            return AreaSerializer
        else:
            return SubAreaSerializer