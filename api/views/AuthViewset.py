from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers.authSerializer import LoginSerializer, UserSerializer, RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not (serializer.is_valid()):
                return Response({
                    'message': 'Invalid data.',
                    'errors': serializer.errors,
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            norm_email = email.lower()
            user = authenticate(email = norm_email, password = password)
            if user is None:
                return Response({
                    'message': 'Invalid username or password',
                    # 'errors': serializer.errors,
                }, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_active:
                return Response({
                    'message': 'Your account is blocked, Please contact admin.',
                    # 'errors': serializer.errors,
                }, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'message': 'Login successful',
                'user': user_serializer.data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, 200)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterView(viewsets.generics.CreateAPIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Invalid data',
                    'errors': serializer.errors,
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        serializer.save()

        return Response({
            'message': 'Account created successfully',
            'success': True,
        })