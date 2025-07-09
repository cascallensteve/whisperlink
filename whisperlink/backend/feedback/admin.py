from django.contrib import admin
from .models import UserProfile, AnonymousFeedback


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'unique_link', 'created_at']
    readonly_fields = ['unique_link']


@admin.register(AnonymousFeedback)
class AnonymousFeedbackAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'submitted_at', 'ip_address']
    list_filter = ['submitted_at']
    readonly_fields = ['submitted_at', 'ip_address']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('recipient__user')
