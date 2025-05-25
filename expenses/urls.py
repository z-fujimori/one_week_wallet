from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_expense, name='create_expense'),
    path('month/', views.monthly , name="monthly"),
    path('week_data/', views.get_week_data, name='get_week_data'),
] 