#!/usr/bin/env python3
"""
Generate a new Django secret key for production deployment
"""

from django.core.management.utils import get_random_secret_key

def generate_secret_key():
    """Generate a new Django secret key"""
    secret_key = get_random_secret_key()
    print("🔑 Generated new Django secret key:")
    print(f"SECRET_KEY={secret_key}")
    print("\n📝 Add this to your Vercel environment variables:")
    print(f"Variable name: SECRET_KEY")
    print(f"Variable value: {secret_key}")
    print("\n⚠️  Keep this secret key secure and don't share it publicly!")
    return secret_key

if __name__ == "__main__":
    generate_secret_key()
