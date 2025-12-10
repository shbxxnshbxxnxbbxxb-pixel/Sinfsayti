from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('students/', views.student_list_view, name='student_list'),
    path('students/<int:pk>/', views.student_detail_view, name='student_detail'),
    path('weekly-leader/', views.weekly_leader_view, name='weekly_leader'),
]
