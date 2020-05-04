from django.conf.urls.static import static
from django.urls import path

from accounts import views
from base import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_change/', views.password_change_view, name='password_change')
]