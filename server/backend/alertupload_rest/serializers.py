from rest_framework import serializers
from detection.models import UploadAlert

class UploadAlertSerializer(serializers.ModelSerializer):
    
    class Meta:
         model = UploadAlert
         fields = ('pk', 'image', 'user_ID', 'location', 'date_created', 'alert_receiver')