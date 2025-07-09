from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.db import connection
from django.db.utils import OperationalError
from .models import UserProfile, AnonymousFeedback
from .forms import FeedbackForm, AIFeedbackForm
from .ai_service import ai_service
import json
import urllib.parse


def home(request):
    """Home page view"""
    return render(request, 'feedback/home.html')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard showing received feedback"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    feedback_list = AnonymousFeedback.objects.filter(recipient=profile)
    feedback_link = request.build_absolute_uri(profile.get_feedback_link())
    
    context = {
        'profile': profile,
        'feedback_list': feedback_list,
        'feedback_link': feedback_link,
    }
    return render(request, 'feedback/dashboard.html', context)


def feedback_form(request, link_id):
    """Anonymous feedback submission form"""
    profile = get_object_or_404(UserProfile, unique_link=link_id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        ai_form = AIFeedbackForm(request.POST)
        
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.recipient = profile
            feedback.ip_address = get_client_ip(request)
            feedback.save()
            
            # Store delete token in session for showing delete link
            request.session[f'feedback_delete_token_{feedback.id}'] = str(feedback.delete_token)
            
            messages.success(request, 'Your feedback has been submitted anonymously!')
            return redirect('feedback_success')
        
        elif ai_form.is_valid() and 'generate_preview' in request.POST:
            # Generate AI preview
            user_input = ai_form.cleaned_data['user_input']
            generated_message = ai_service.generate_feedback(user_input, profile.user.username)
            
            context = {
                'form': form,
                'ai_form': ai_form,
                'profile': profile,
                'generated_preview': generated_message,
                'original_input': user_input,
                'show_preview': True,
            }
            return render(request, 'feedback/feedback_form.html', context)
        
        elif 'confirm_ai_feedback' in request.POST:
            # Confirm and submit AI feedback
            user_input = request.POST.get('original_input')
            generated_message = request.POST.get('generated_message')
            
            feedback = AnonymousFeedback.objects.create(
                recipient=profile,
                message=generated_message,
                original_input=user_input,
                is_ai_generated=True,
                ip_address=get_client_ip(request)
            )
            
            # Store delete token in session
            request.session[f'feedback_delete_token_{feedback.id}'] = str(feedback.delete_token)
            
            messages.success(request, 'Your AI-enhanced feedback has been submitted anonymously!')
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
        ai_form = AIFeedbackForm()
    
    context = {
        'form': form,
        'ai_form': ai_form,
        'profile': profile,
    }
    return render(request, 'feedback/feedback_form.html', context)


def feedback_success(request):
    """Success page after feedback submission"""
    return render(request, 'feedback/feedback_success.html')


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def profile_settings(request):
    """User profile settings"""
    profile = request.user.userprofile
    feedback_link = request.build_absolute_uri(profile.get_feedback_link())
    
    context = {
        'profile': profile,
        'feedback_link': feedback_link,
    }
    return render(request, 'feedback/profile_settings.html', context)


def delete_feedback(request, delete_token):
    """Delete feedback using delete token"""
    feedback = get_object_or_404(AnonymousFeedback, delete_token=delete_token)
    
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Your feedback has been deleted successfully!')
        return redirect('home')
    
    context = {
        'feedback': feedback,
    }
    return render(request, 'feedback/delete_feedback.html', context)


@login_required
def delete_received_feedback(request, feedback_id):
    """Delete feedback that user received"""
    try:
        feedback = get_object_or_404(AnonymousFeedback, id=feedback_id, recipient__user=request.user)
    except:
        messages.error(request, 'Feedback not found or you do not have permission to delete it.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback has been deleted from your dashboard!')
        return redirect('dashboard')
    
    context = {
        'feedback': feedback,
    }
    return render(request, 'feedback/delete_received_feedback.html', context)


def share_whatsapp(request, link_id):
    """Generate WhatsApp sharing link"""
    profile = get_object_or_404(UserProfile, unique_link=link_id)
    feedback_link = request.build_absolute_uri(profile.get_feedback_link())
    
    message = f"Hi! I'd love to get your honest feedback about me. You can share your thoughts anonymously here: {feedback_link}"
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(message)}"
    
    return redirect(whatsapp_url)


def about_developer(request):
    """About the developer page"""
    return render(request, 'feedback/about_developer.html')


def health_check(request):
    """Health check endpoint to test database connectivity"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except OperationalError as e:
        db_status = f"error: {str(e)}"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    status = {
        'database': db_status,
        'status': 'healthy' if db_status == 'connected' else 'unhealthy'
    }
    
    return JsonResponse(status)
