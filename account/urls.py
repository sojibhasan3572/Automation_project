from django.urls import path
from . import views 
app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("verify-email/<slug:username>/<uidb64>/", views.auto_active_verify_email, name="auto_verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    
]