from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    JobApplicationListView,
    JobApplicationDetailView,
    JobApplicationCreateView,
    JobApplicationUpdateView,
    JobApplicationDeleteView,
    register,
    index,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyListView,
    CompanyDeleteView
)
urlpatterns = [
    # Home / Index
    path('', views.index, name='index'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Job Application URLs
    path('applications/', views.JobApplicationListView.as_view(), name='jobapplication_list'),
    path('applications/new/', views.JobApplicationCreateView.as_view(), name='jobapplication_create'),
    path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='jobapplication_detail'),
    path('applications/<int:pk>/edit/', views.JobApplicationUpdateView.as_view(), name='jobapplication_update'),
    path('applications/<int:pk>/delete/', views.JobApplicationDeleteView.as_view(), name='jobapplication_delete'),

    # Company CRUD URLs
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/new/', CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
]
