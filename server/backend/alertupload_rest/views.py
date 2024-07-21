from alertupload_rest.serializers import UploadAlertSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from twilio.rest import Client
from alertupload_rest.serializers import UploadAlertSerializer


import re
from django.conf import settings

@api_view(['POST'])
def post_alert(request):
    
    serializer = UploadAlertSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        send_twilio_message()
    else:
        return JsonResponse({'error': 'Unable to process the data!'}, status=400)
    
    return Response(request.META.get('HTTP_AUTHORIZATION'))
from django.http import JsonResponse

def alarm_toggle(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        if state == 'on':
            # Turn alarm on
            print('Alarm turned on')
        elif state == 'off':
            # Turn alarm off
            print('Alarm turned off')
        return JsonResponse({'message': 'Alarm state updated'})
    return JsonResponse({'error': 'Invalid request'})

def send_twilio_message():
    # Your Twilio credentials
    account_sid = 'ACfa1354afc1ae839eeb2ca0b641114ab4'
    auth_token = '2ebffd22969d8c66c845e9207871f1be'
    
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    try:
        # Create and send the message
        message = client.messages.create(
            from_='+17065286370',
            body=f'Alert, accident has been detected at CCTV1!',
            to='+263780517601'
        )
        
        print("Message SID:", message.sid)  # Print the SID for reference
    except Exception as e:
        print("An error occurred while sending the Twilio message:", str(e))




