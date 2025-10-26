from django.urls import path
from . import views


urlpatterns = [
    # allow both with and without trailing slash to avoid client confusion
    path('strings', views.ListCreateStringView.as_view()),
    path('strings/', views.ListCreateStringView.as_view()),

    path('strings/filter-by-natural-language', views.NaturalLanguageFilterView.as_view()),
    path('strings/filter-by-natural-language/', views.NaturalLanguageFilterView.as_view()),

    path('strings/<path:string_value>', views.RetrieveDeleteStringView.as_view()),
    path('strings/<path:string_value>/', views.RetrieveDeleteStringView.as_view()),
]