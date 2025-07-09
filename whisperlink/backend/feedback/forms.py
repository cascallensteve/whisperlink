from django import forms
from .models import AnonymousFeedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = AnonymousFeedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your honest thoughts...',
                'rows': 6,
                'maxlength': 1000,
            }),
        }
        labels = {
            'message': 'Your Anonymous Feedback',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].help_text = 'Your feedback will be completely anonymous. Be honest, kind, and constructive.'


class AIFeedbackForm(forms.Form):
    user_input = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your thoughts in your own words... AI will help make it more constructive and professional.',
            'rows': 4,
            'maxlength': 500,
        }),
        label='Your Raw Thoughts',
        help_text='Describe what you think about this person in your own words. AI will help refine it into constructive feedback.',
        max_length=500
    )
