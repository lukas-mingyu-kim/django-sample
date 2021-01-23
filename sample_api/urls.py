from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sample_api import views


router = DefaultRouter()

urlpatterns = [

    path('login', views.UserLoginApiView.as_view()),
    path('users/<int:user_id>/accounts', views.AccountApiView.as_view()),
    path('users/<int:user_id>/deposit', views.DepositWithdrawApiView.as_view(), name='deposit'),
    path('users/<int:user_id>/withdraw', views.DepositWithdrawApiView.as_view(), name='withdraw'),
    path('', include(router.urls))

]
