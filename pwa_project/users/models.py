"""
Users App Models - Authentication and Profile Management for ChipIn
==================================================================

This module handles user authentication, profiles, and security features
specifically designed for the ChipIn student platform.

Key Features:
- Secure user registration and authentication
- Student profile management with trusted adult oversight
- Balance and spending limit management
- Privacy and safety controls
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, EmailValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
import uuid


class UserSession(models.Model):
    """
    Track user sessions for security monitoring
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-login_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a new user is created"""
    if created:
        from chipin.models import Profile
        Profile.objects.create(
            user=instance,
            student_id=f"STU{instance.id:06d}",  # Generate student ID
            trusted_adult_email='parent@example.com',
            trusted_adult_phone='555-0123'
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()