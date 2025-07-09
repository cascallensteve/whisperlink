# WhisperLink - Anonymous Feedback Platform

A Django-based web platform that allows users to receive anonymous feedback from others to build self-awareness and foster honest communication.

## Features

- **User Registration & Authentication**: Simple account creation and login system
- **Unique Feedback Links**: Each user gets a unique shareable link for receiving feedback
- **Anonymous Feedback**: Complete anonymity for feedback senders
- **Dashboard**: Personal dashboard to view all received feedback
- **Mobile-Friendly**: Responsive design that works on all devices
- **Privacy-Focused**: No tracking of feedback senders beyond IP addresses for security

## About the Developer

WhisperLink is developed by **Bro Cascallen**, Founder of **Technova Brocoder** - a technology company focused on creating meaningful digital experiences that foster authentic human connections.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd whisperlink
   ```

2. **Set up virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**:
   - Update database credentials in `whisperlink_backend/settings.py`
   - The current configuration uses Supabase PostgreSQL

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### For Users Receiving Feedback:
1. Register for an account
2. Go to your dashboard to get your unique feedback link
3. Share the link with friends, family, or colleagues
4. Check your dashboard to view received feedback

### For Feedback Senders:
1. Visit a user's unique feedback link
2. Write your anonymous feedback
3. Submit - no registration required

## Project Structure

```
whisperlink/
├── backend/
│   ├── feedback/                 # Main Django app
│   │   ├── models.py            # User profiles and feedback models
│   │   ├── views.py             # All views and logic
│   │   ├── forms.py             # Form definitions
│   │   ├── urls.py              # URL patterns
│   │   ├── admin.py             # Admin configuration
│   │   ├── signals.py           # Django signals
│   │   ├── templates/           # HTML templates
│   │   │   ├── feedback/        # App-specific templates
│   │   │   └── registration/    # Auth templates
│   │   └── static/              # CSS, JS, images
│   │       └── css/
│   │           └── style.css    # Custom styles
│   ├── whisperlink_backend/     # Django project settings
│   │   ├── settings.py          # Main settings
│   │   ├── urls.py              # Root URL configuration
│   │   └── wsgi.py              # WSGI application
│   ├── manage.py                # Django management script
│   └── requirements.txt         # Python dependencies
└── README.md                    # This file
```

## Database Schema

### UserProfile Model
- `user` - One-to-one relationship with Django's User model
- `unique_link` - UUID field for the shareable feedback link
- `created_at` - Timestamp of profile creation

### AnonymousFeedback Model
- `recipient` - Foreign key to UserProfile
- `message` - Text field for the feedback content
- `submitted_at` - Timestamp of feedback submission
- `ip_address` - IP address of sender (for security)

## Security Features

- **Anonymous Feedback**: No user identification stored with feedback
- **IP Logging**: Only IP addresses are logged for security purposes
- **CSRF Protection**: Django's built-in CSRF protection
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **Password Validation**: Strong password requirements

## Customization

### Styling
- Modify `feedback/static/css/style.css` for custom styling
- The design uses Bootstrap 5 with custom CSS overrides
- Responsive design optimized for mobile devices

### Features
- Add email notifications for new feedback
- Implement feedback categories or tags
- Add feedback analytics and insights
- Create API endpoints for mobile apps

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please open an issue in the repository.
