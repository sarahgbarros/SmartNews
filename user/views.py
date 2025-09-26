from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import UserPreference
from news.models import NewsCategory
from django.db import transaction
from user.serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from user.serializers import UserRegistrationSerializer, UserLoginSerializer


class RegisterViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'access': access_token
            }, status=status.HTTP_201_CREATED)

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,        
                samesite='Strict',
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'access': access_token
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Strict',
            )
            return response

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class UserPreferenceViewSet(viewsets.GenericViewSet):
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = UserPreference.objects.filter(user=request.user)
        category_names = list(queryset.values_list('category__name', flat=True))
    
        return Response(category_names, status=status.HTTP_200_OK)

    def create(self, request):
        category_names = request.data.get('categories', []) 

        if not isinstance(category_names, list):
            return Response({"detail": "O campo 'categories' deve ser uma lista de nomes."}, status=400)

        try:
            with transaction.atomic():
                user = request.user
                
                UserPreference.objects.filter(user=user).delete()

                if NewsCategory.objects.filter(name__in=category_names).exists():
                    valid_categories = NewsCategory.objects.filter(name__in=category_names)
                else:
                    return Response({'detail': 'Nenhuma categoria válida encontrada.'}, status=400)
                
                new_preferences = [
                    UserPreference(user=user, category=cat)
                    for cat in valid_categories
                ]
                UserPreference.objects.bulk_create(new_preferences)

            return Response({'status': 'Preferências salvas com sucesso'}, status=200)

        except Exception as e:
            return Response({'detail': f'Erro interno ao salvar: {e}'}, status=500)


