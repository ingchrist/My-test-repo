from django.urls import path

# from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('partners/login/', views.PartnersLoginAPIView.as_view(),
         name='partners/login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('partners/register/', views.PartnersRegisterAPIView.as_view(),
         name='partners/register'),
    path('register/verify-email/',
         views.ValidateEmailVerificationTokenView.as_view(), name='verify_email'),
    path('partners/register/verify-email/',
         views.ValidateEmailVerificationPartnersTokenView.as_view(),
         name='partners_verify_email'),
    path('resend-email/', views.ResendEmailVerificationView.as_view(),
         name='resend_email'),

    path('forget-password/',
         views.ForgetPasswordView.as_view(), name='forget_password'),
    path('forget-password/validate-token/',
         views.ValidateResetPasswordTokenView.as_view(), name='validate-reset-token'),
    path('forget-password/reset/', views.ForgetResetPasswordView.as_view(),
         name='forget_password_reset'),

    # JWT
    path('token/user/refresh/',
         views.TokenRefreshAPIView.as_view(), name='token_refresh'),
    path('token/user/validate/',
         views.TokenVerifyAPIView.as_view(), name='token_validate'),

    path('user/', views.UserAPIView.as_view(), name='user_data'),
    path('user/change-password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('user/profile/update/',
         views.ProfileAPIView.as_view(), name='detail_profile'),

    path('utils/add-newsletter/',
         views.NewsletterAPICreate.as_view(), name='newsletter_add'),
]
