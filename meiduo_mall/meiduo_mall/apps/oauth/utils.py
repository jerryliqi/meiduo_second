from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer, BadData
from django.conf import settings

from . import constants



def generate_save_user_token(openid):
    """
    生成保存用户数据的token
    :param openid: 用户的openid
    :return: token
    """
    """对openid进行加密"""
    # 1.创建序列化器
    # expires_in过期时间
    serializer = TJSSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.QQ_OPENID_ENCRYPTION)

    # 2.构造数据
    data = {
        "openid": openid
    }
    # 3.dumps进行加密(返回默认是byte类型)
    access_token_bytes = serializer.dumps(data)

    # 4.返回响应数据
    return access_token_bytes.decode()


def check_save_user_token(access_token):
    """解密"""
    # 1.创建序列化器
    serializer = TJSSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.QQ_OPENID_ENCRYPTION)
    # 2.loads进行解密
    try:
        data = serializer.loads(access_token)
    except BadData:
        return None
    else:
        return data.get("openid")