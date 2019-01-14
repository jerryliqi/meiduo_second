import logging

from celery_tasks.main import app
from .yuntongxun.sms import CCP
from . import constants


logger = logging.getLogger("django")

# 验证码短信模板
SMS_CODE_TEMP_ID = 1


@app.task(name="send_sms_code")
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码
    :param mobile: 手机号
    :param sms_code: 验证码
    """
    # 利用云通讯第三方平台发送短信

    try:
        result = CCP.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], SMS_CODE_TEMP_ID)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
