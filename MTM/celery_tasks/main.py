#celery启动文件
from celery import Celery
#为celery使用django配置文件进行设置
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scf.settings')
#创建celery实例
app = Celery('celery_tasks')
#设置broker
app.config_from_object('celery_tasks.config')
#自动检测指定包的任务
app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email_send'])