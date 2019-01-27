from rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划序列化器
    如果查询所有省时,它代表省的序列化器
    如果查询单个省时,此序列化器代表的是省下面的一个一个市
    如果查询单个市时,此序列化器代表的是市下面的一个一个区
    """

    class Meta:
        model = Area
        fields = ["id", "name"]


class SubAreaSerializer(serializers.ModelSerializer):
    """
    子行政区序列化器
    此序列化器只有在查询单一视图时才会使用,
    如果查某个省时,此序列化器代表这个省,subs里面装着这个省下面的所有市
    如果查某个市时,此序列化器代表这个市,subs里面装着这个市下面的所有区/县
    """
    # 关联序列化时尽量定义只做序列化输出
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ["id", "name", "subs"]