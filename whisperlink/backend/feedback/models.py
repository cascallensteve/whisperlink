from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_feedback_link(self):
        return f"/feedback/{self.unique_link}/"


class AnonymousFeedback(models.Model):
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_feedback')
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_ai_generated = models.BooleanField(default=False)
    original_input = models.TextField(null=True, blank=True)  # Store original user input before AI processing
    delete_token = models.UUIDField(default=uuid.uuid4, editable=False)  # For anonymous deletion
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Feedback for {self.recipient.user.username} at {self.submitted_at}"
    
    def get_delete_link(self):
        return f"/delete-feedback/{self.delete_token}/"
