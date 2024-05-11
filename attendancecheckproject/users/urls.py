from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserAPIView, MyTokenObtainPairView, ChangeUserInfo, \
    ChangePasswordAPIView, UserDataView, UserList

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register-user'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('change-user-info/', ChangeUserInfo.as_view(), name='change-user-info'),

    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),

    path('user_data/',UserDataView.as_view()),
    path('get/users/', UserList.as_view(), name='user_list'),
]
