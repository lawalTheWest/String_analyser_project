from django.urls import path
from . import views


urlpatterns = [
    # single endpoint for list + create
    path('strings', views.ListCreateStringView.as_view()),
    path('strings/<str:string_value>', views.RetrieveDeleteStringView.as_view()),
    path('strings/filter-by-natural-language', views.NaturalLanguageFilterView.as_view()),
]