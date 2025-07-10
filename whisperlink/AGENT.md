# WhisperLink Agent Configuration

## Build/Test/Lint Commands
- **Dev server**: `cd backend && python manage.py runserver`
- **Migrations**: `cd backend && python manage.py makemigrations && python manage.py migrate`
- **Test**: `cd backend && python manage.py test` (for all tests) or `python manage.py test feedback.tests.TestSpecificCase` (single test)
- **Create superuser**: `cd backend && python manage.py createsuperuser`
- **Collectstatic**: `cd backend && python manage.py collectstatic`
- **Shell**: `cd backend && python manage.py shell`

## Architecture
- **Django 5.1.5** monolith with PostgreSQL (Supabase)
- **Main app**: `feedback/` - handles user profiles, anonymous feedback, AI processing
- **Core models**: `UserProfile` (UUID links), `AnonymousFeedback` (with delete tokens)
- **Database**: Uses PostgreSQL with environment-based config (.env file)
- **Deployment**: Vercel-ready with WhiteNoise for static files

## Code Style
- **Import order**: Django imports, third-party, local (standard Django convention)
- **Models**: Use `__str__` methods, `Meta` classes for ordering, UUID fields for security
- **Views**: Function-based views with decorators (`@login_required`, `@csrf_exempt`)
- **Forms**: Django forms in `forms.py`, custom validation methods
- **Naming**: Snake_case for variables/functions, CamelCase for models, lowercase for URLs
- **Error handling**: Django messages framework, try/except for model operations
- **Templates**: Bootstrap 5 + custom CSS, responsive design patterns
