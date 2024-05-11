from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

from django.http import JsonResponse
from rest_framework.decorators import api_view


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        # Получите новые значения first_name и last_name из запроса
        new_first_name = request.data.get('first_name')
        new_last_name = request.data.get('last_name')

        # Проверьте, чтобы новые значения не были пустыми
        if not new_first_name or not new_last_name:
            return Response({"error": "Both first name and last name are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Обновите значения first_name и last_name пользователя
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.save()

        return Response({"message": "User information updated successfully"},
                        status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if not username or not new_password:
            return Response({"error": "Both username and new password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User with this username does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        # Хешируем новый пароль
        hashed_password = make_password(new_password)

        # Обновляем пароль пользователя
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."},
                        status=status.HTTP_200_OK)

@api_view(['GET'])
def user_data_view(request):
    user = request.user
    # if not user.is_authenticated:
    #     return JsonResponse({"error": "Authentication credentials were not provided."}, status=401)

    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_teacher': user.is_teacher,
        
        # Add more fields as needed
    }
        
    return JsonResponse(user_data)

class UserDataView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # if not user.is_authenticated:
        #     return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            # 'email': user.email,
            'is_teacher': user.is_teacher,
            'username': user.username,
            # Добавьте больше полей при необходимости
        }

        return Response(user_data)


# from rest_framework import generics
# from .models import User
# from .serializers import UserSerializer

class UserList(APIView):
 
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

