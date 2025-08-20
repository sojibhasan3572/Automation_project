from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .forms import RegistrationForm
from .models import OtpToken
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
        else:
            context = {'form': form}
            return render(request, 'register.html', context)
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
    return render(request, 'register.html', context)

def verify_email(request):
    user = get_user_model().objects.get(email=request.user.email)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("login")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "accounts/verify_token.html", context)

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                """
            sender = settings.EMAIL_HOST_USER
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "accounts/resend_otp.html", context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        form = AuthenticationForm()
        context = {'form': form,}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')

