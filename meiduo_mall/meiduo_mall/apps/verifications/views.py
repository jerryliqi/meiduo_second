from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response
import random
import logging

from . import constants
from meiduo_mall.libs.yuntongxun.sms import CCP


# 创建日志输出器对象,在settings中定义了一个名为django的日志器
logger = logging.getLogger("django")


# r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$'
class SMSCodeView(APIView):
    """发送短信"""

    def get(self, request, mobile):
        # 连接redis数据库, 对应2号仓库
        redis_conn = get_redis_connection("verify_code")
        # 每次发送短信验证码之前先判断短信验证码是否过期  GET key
        flag_sms = redis_conn.get("flag_sms_%s" % mobile)
        if flag_sms:
            return Response({"message": "重复发送"}, status=status.HTTP_400_BAD_REQUEST)

        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        # 将生成的短信验证码储存到redis数据库,有效期60秒  SETEX key seconds value
        print(sms_code)
        redis_conn.setex("code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 储存一个发过短信的标识,以免频繁发送短信
        redis_conn.setex("flag_sms_%s" % mobile, constants.SEND_SMS_CODE_TNTERVAL, 1)
        logger.info(sms_code)

        # 利用云通讯第三方平台发送短信
        CCP.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)

        return Response({"message": "ok"})

