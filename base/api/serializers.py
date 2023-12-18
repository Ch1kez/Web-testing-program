from rest_framework import serializers
from .models import Mail, Target, Tuser, Test, WebsiteTable

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = '__all__'

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'

class TuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tuser
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class WebsiteTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteTable
        fields = '__all__'
