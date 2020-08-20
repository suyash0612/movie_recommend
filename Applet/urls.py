from django.urls import path , include
from . import views

urlpatterns = [path('', views.index , name='index'),
               path('test/', views.test , name='test'),
               path('test/request_data/', views.request_data , name='request_data'),
               path('test/request_choice/', views.request_choice , name='request_choice'),
               ]