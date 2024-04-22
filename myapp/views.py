from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from myapp.authentication import APIKeyAuthentication
from .serializers import PublicUserSerializer, UserSerializer, UserAPIKeySerializer
from .models import CustomUser, PublicUser, UserAPIKey
from rest_framework.permissions import IsAuthenticated


class CreateUserAPIView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            try:
                with transaction.atomic():  # Ensures all or nothing is committed to the database
                    user = user_serializer.save()
                    # Automatically create an API key when the user is created
                    api_keys, created = UserAPIKey.objects.get_or_create(user=user)
                    api_key_serializer = UserAPIKeySerializer(api_keys)
                    
                return Response({
                    'user': user_serializer.data,
                    'api_keys': api_key_serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetUserAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"error": "User Id Is Required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(CustomUser, pk=user_id)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    

class CreatePublicUserView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        public_user_serializer = PublicUserSerializer(data=request.data)
        if public_user_serializer.is_valid():
            try:
                with transaction.atomic():
                    user = public_user_serializer.save()
                    return Response({
                        'public_user': public_user_serializer.data
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        else:
            return Response(public_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetPublicUserView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"error" : "User Name Is Required."}, status== status.HTTP_400_BAD_REQUEST)
        
        public_user = get_object_or_404(PublicUser, username=username)
        public_user_serializer = PublicUserSerializer(public_user)
        return Response(public_user_serializer.data, status=status.HTTP_200_OK)
