from django.urls import path

from election import views

app_name = 'election'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:citizenship_number>/fill/form/', views.election_fill_form_view, name='election_form')
    
]
