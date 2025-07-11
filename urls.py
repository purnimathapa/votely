from django.urls import path
from . import views

urlpatterns = [
    path('', views.election_list, name='election_list'),
    path('create/', views.election_create, name='election_create'),
    path('<int:pk>/', views.election_detail, name='election_detail'),
    path('<int:pk>/edit/', views.election_edit, name='election_edit'),
    path('<int:pk>/delete/', views.election_delete, name='election_delete'),
    path('<int:pk>/results/', views.election_results, name='election_results'),
    path('<int:election_pk>/candidates/add/', views.candidate_create, name='candidate_create'),
    path('candidates/<int:pk>/edit/', views.candidate_edit, name='candidate_edit'),
    path('candidates/<int:pk>/delete/', views.candidate_delete, name='candidate_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
] 