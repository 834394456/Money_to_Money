import re

from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView, CreateAPIView

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers.register_login import RegisterSerializer


class SmsCodeAPIView(APIView):
    def get(self, request, mobile):
        # 接收数据
        query_params = request.query_params
        # 验证数据
        if not re.match(r'1[3-9]\d{9}', mobile):
            return Response({})
        # 生成验证码
        from random import randint
        sms_code = '%06d' % randint(0, 999999)
        # 云通讯发送短信
        from celery_tasks.sms.tasks import celery_send_sms_code
        celery_send_sms_code.delay(mobile, sms_code)
        # 保存验证码到redis
        redis_conn = get_redis_connection('code')
        print(sms_code)
        redis_conn.setex('sms_%s' % mobile, 300, sms_code)
        return Response({'success': 'true', 'sms_code': sms_code, 'message':' '})


class RegisterAPIView(CreateAPIView):

    queryset = User

    serializer_class = RegisterSerializer