import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class RegisterSerializer(ModelSerializer):
    token = serializers.CharField(read_only=True)
    sms_code = serializers.CharField(required=True, max_length=6, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = 'username', 'password', 'mobile', 'token', 'sms_code'

        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 6,
                         'max_length': 16,
                         'error_messages': {
                             'min_length': '仅允许6-16个字符的密码',
                             'max_length': '仅允许6-16个字符的密码'
                         }
                         },
            'uername': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            }
        }

    def validate_mobile(self, value):
        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号格式不正确')

        return value

    def validate(self, attrs):
        sms_code = attrs.get('sms_code')
        mobile = attrs.get('mobile')
        redis_conn = get_redis_connection('code')
        redis_sms_code = redis_conn.get('sms_%s' % mobile)

        if redis_sms_code is None:
            raise serializers.ValidationError('短信验证码已过期')

        if redis_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):
        del validated_data['sms_code']

        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        from rest_framework_jwt.settings import api_settings
        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user
