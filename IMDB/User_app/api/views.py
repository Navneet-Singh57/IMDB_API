from rest_framework.decorators import api_view
from .serializers import RegistraionSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .. import models



@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=200)

@api_view(['POST'])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistraionSerializer(data = request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successfull"
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user=account).key
            data['token'] = token
            
        else:
            data = serializer.errors
        
        return Response(data)