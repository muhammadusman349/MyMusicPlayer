from django.urls import path
from .views import (
                    RegistrationApi,
                    LoginApiView,
                    ChangePasswordView,
                    ForgetPasswordView,
                    ResetPasswordView,
                    UserView,
                    )
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [
    path("",                            RegistrationApi.as_view(),              name='register'),
    path("user/" ,                      UserView.as_view(),                     name ='user-list'),
    path("login/",                      LoginApiView.as_view(),                 name='login'),
    path('token-refresh/',              jwt_views.TokenRefreshView.as_view(),   name='token_refresh'),
    path('changepassword/',             ChangePasswordView.as_view(),           name='change-password'),
    path('forget/password/',            ForgetPasswordView.as_view(),           name='forget-password'),
    path('reset/password/',             ResetPasswordView.as_view(),            name='reset-password'),
]