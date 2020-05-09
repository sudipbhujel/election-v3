from django.conf.urls.static import static
from django.urls import path

from accounts import views
from base import settings

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_change/', views.password_change_view, name='password_change'),

    path('reset_password_confirm/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('reset_password/', views.ResetPasswordRequestView.as_view(),
         name='reset_password'),
]
