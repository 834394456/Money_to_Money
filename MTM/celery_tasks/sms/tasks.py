"""
1.必须要让celery的实例的装饰器装饰
2.需要celery 自动检测指定包的任务
"""
from celery_tasks.main import app
from libs.yuntongxun.sms import CCP

@app.task
def celery_send_sms_code(mobile,code):

    CCP().send_template_sms(mobile,[code,5],1)