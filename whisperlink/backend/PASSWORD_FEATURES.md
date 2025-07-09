# Password Management Features

This document explains the new password management features added to WhisperLink.

## Features Added

### 1. Password Change
- **URL**: `/password-change/`
- **Access**: Logged-in users only
- **Location**: Available in Profile Settings
- Users can change their password by providing their current password and new password

### 2. Password Reset (Forgot Password)
- **URL**: `/password-reset/`
- **Access**: Available on login page
- **Process**: 
  1. User enters email address
  2. System sends reset link via email
  3. User clicks link to set new password
  4. Redirects to login with success message

### 3. Enhanced AI Feedback Generation
- **Upgraded Model**: Now uses Meta-Llama-3.1-70B-Instruct-Turbo (previously Mixtral-8x7B)
- **Improved Prompts**: More comprehensive and detailed feedback generation
- **Higher Token Limit**: Increased from 500 to 1000 tokens for longer responses
- **Better Structure**: Generates structured feedback with clear sections

## Setup Instructions

### 1. Email Configuration
Copy `.env.example` to `.env` and configure:

```bash
# Gmail configuration (recommended)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Use App Password, not regular password

# Together AI for enhanced feedback
TOGETHER_API_KEY=your-together-api-key
```

### 2. Gmail App Password Setup
1. Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
2. Generate an App Password for "Mail"
3. Use this password in EMAIL_HOST_PASSWORD

### 3. Testing
- For development: Email backend prints to console
- For production: Configure SMTP settings in settings.py

## URLs Added

```python
# Password change URLs
path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

# Password reset URLs  
path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
```

## Templates Created

- `password_change_done.html` - Success page after password change
- `password_reset.html` - Password reset request form
- `password_reset_done.html` - Email sent confirmation
- `password_reset_confirm.html` - New password form
- `password_reset_complete.html` - Password reset success

## Error Handling

- Added better error handling for delete feedback operations
- Graceful fallback when AI API fails
- User-friendly error messages for missing feedback

## Security Features

- Uses Django's built-in password reset tokens
- Secure password validation
- Rate limiting through Django's built-in mechanisms
- Environment variable configuration for sensitive data
