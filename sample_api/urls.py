from django.urls import path

from sample_api import views


urlpatterns = [

    path('balance/', views.AtmApiView.as_view()),

]