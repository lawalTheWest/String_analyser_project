from django.urls import path
from . import views

app_name = 'string_analyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_string, name='analyze'),
]
