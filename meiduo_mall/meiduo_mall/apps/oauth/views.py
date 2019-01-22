from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from QQLoginTool.QQtool import  OAuthQQ
from django.conf import settings
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .models import OAuthQQUser
from .utils import generate_save_user_token



# '/oauth/qq/user/?code='
class QQAuthorUserView(GenericAPIView):

    serializer_class = "序列化器"

    def get(self, request):
        # 提取code请求参数
        code = request.query_params.get("code")
        if not code:
            return Response({"message": "缺少code"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建工具对象
        oauthqq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)

        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauthqq.get_access_token(code)
            # 使用access_token向QQ服务器请求openid
            openid = oauthqq.get_open_id(access_token)
        except Exception:
            return Response({"message": "QQ服务器异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 使用openid查询该QQ用户是否在商城绑定过
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果没绑定过,创建用户并绑定openid
            # 为了能够在后续的绑定用户操作中前端可以使用openid，在这里将openid签名后响应给前端
            # 签名方式为itsdangerous
            access_token_openid = generate_save_user_token(openid)
            return Response({"access_token": access_token_openid})
        else:
            # 如果绑定过,直接生成JWT token, 并返回
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 获取oauth_user关联的user
            user = oauth_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = {
                "token": token,
                "user_id": user.id,
                "username": user.username
            }
            return response


class QQAuthorURLView(APIView):
    """
    提供QQ登录页面网址
    https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=xxx&redirect_uri=xxx&state=xxx
    """

    def get(self, request):
        """返回QQ扫码URL"""
        # 获取参数next的来源
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next = request.query_params.get("next")
        if not next:
            next = "/"

        # # QQ登录参数
        # QQ_CLIENT_ID = '101474184'
        # QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
        # QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
        # 创建OAuthQQ工具对象
        oauthqq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI
        )

        # 调用SDK中的方法获取到拼接好的扫码url
        login_url = oauthqq.get_qq_url()

        # 返回响应
        return Response({"login_url": login_url})

