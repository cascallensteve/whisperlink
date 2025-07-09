#!/usr/bin/env python
"""
Setup script for WhisperLink Anonymous Feedback Platform
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a system command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Main setup function."""
    print("Setting up WhisperLink Anonymous Feedback Platform...")
    print("=" * 50)
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected.")
        print("   It's recommended to use a virtual environment.")
        print("   Create one with: python -m venv venv")
        print("   Activate it with: venv\\Scripts\\activate (Windows) or source venv/bin/activate (macOS/Linux)")
        print()
    
    # Install dependencies
    print("📦 Installing dependencies...")
    if run_command("pip install -r requirements.txt"):
        print("✅ Dependencies installed successfully!")
    else:
        print("❌ Failed to install dependencies.")
        return
    
    # Make migrations
    print("\n🔄 Creating database migrations...")
    if run_command("python manage.py makemigrations"):
        print("✅ Migrations created successfully!")
    else:
        print("❌ Failed to create migrations.")
        return
    
    # Run migrations
    print("\n🗄️  Running database migrations...")
    migration_result = run_command("python manage.py migrate")
    if migration_result:
        print("✅ Database migrations completed successfully!")
    else:
        print("⚠️  Database migrations failed. This might be due to database connectivity issues.")
        print("   Please check your database credentials in settings.py")
    
    # Collect static files
    print("\n📁 Collecting static files...")
    if run_command("python manage.py collectstatic --noinput"):
        print("✅ Static files collected successfully!")
    else:
        print("⚠️  Failed to collect static files.")
    
    # Create superuser prompt
    print("\n👤 Do you want to create a superuser account? (y/n): ", end="")
    if input().lower() in ['y', 'yes']:
        print("Creating superuser...")
        os.system("python manage.py createsuperuser")
    
    print("\n🎉 Setup completed!")
    print("=" * 50)
    print("Next steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Visit http://127.0.0.1:8000 in your browser")
    print("3. Register an account and start using WhisperLink!")
    print("\nAdmin panel: http://127.0.0.1:8000/admin (if you created a superuser)")

if __name__ == "__main__":
    main()
