from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password change URLs
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feedback/<uuid:link_id>/', views.feedback_form, name='feedback_form'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('delete-feedback/<uuid:delete_token>/', views.delete_feedback, name='delete_feedback'),
    path('delete-received-feedback/<int:feedback_id>/', views.delete_received_feedback, name='delete_received_feedback'),
    path('share-whatsapp/<uuid:link_id>/', views.share_whatsapp, name='share_whatsapp'),
    path('about-developer/', views.about_developer, name='about_developer'),
    path('health/', views.health_check, name='health_check'),
]
