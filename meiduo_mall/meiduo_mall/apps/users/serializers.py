import re

from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="确认密码", write_only=True)
    sms_code = serializers.CharField(label="短信验证码", write_only=True)
    allow = serializers.CharField(label="同意协议", write_only=True)
    token = serializers.CharField(label="登录状态token", read_only=True)  # 增加token字段

    class Meta:
        model = User
        fields = ["id", "username", "password", "password2", "mobile", "sms_code", "allow", "token"]
        # 补充字段
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 追加单个字段校验
    def validate_mobile(self, value):
        """校验手机号"""
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("手机格式错误")

        return value

    def validate_allow(self, value):
        """校验是否同意协议"""

        if value != "true":
            raise serializers.ValidationError("请同意用户协议")

        return value

    # 字段联合校验
    def validate(self, data):
        """验证两次密码是否一致及短信验证码是否正确"""
        # 验证两次密码一致性
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("密码不一致,请重新输入")

        mobile = data["mobile"]
        sms_code = data["sms_code"]
        # 验证码是否正确
        redis_conn = get_redis_connection("verify_code")
        # redis取出的数据类型为bytes类型
        real_sms_code = redis_conn.get("sms_%s" % mobile).decode("utf-8")
        if not real_sms_code:
            raise serializers.ValidationError("无效验证码")
        if sms_code != real_sms_code:
            raise serializers.ValidationError("验证码输入有误")

        return data

    # 重写create方法,validated_data是一个字典
    def create(self, validated_data):
        """创建注册用户"""
        # 将模型中没有的字段去除
        # del validated_data["password2"]

        validated_data.pop("password2")
        validated_data.pop("sms_code")
        validated_data.pop("allow")

        # 创建用户模型对象
        # user = super().create(validated_data)
        user = User(**validated_data)
        # 将用户密码加密
        user.set_password(validated_data["password"])
        # 储存注册用户信息
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user


