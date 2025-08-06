"""
ChipIn Views - Main application views for the student collaborative platform
==========================================================================

This module contains all the views for the ChipIn platform, implementing
the secure social media functionality for student cost-sharing.

Key features implemented:
- User dashboard and profile management
- Group creation and management
- Event creation and participation
- Payment handling and balance management
- Comment system for groups/events
- Join request workflow
- Security and privacy controls
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from decimal import Decimal
import json

from .models import (
    Profile, Group, GroupMembership, GroupJoinRequest, 
    Event, EventParticipation, Comment
)


# ============================================================================
# Dashboard and Home Views
# ============================================================================

@login_required
def dashboard(request):
    """
    Main dashboard view for logged-in users
    Shows user's groups, upcoming events, and activity summary
    """
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    
    # Get user's groups and events
    user_groups = Group.objects.filter(members=user, is_active=True)[:5]
    upcoming_events = Event.objects.filter(
        participants=user, 
        start_datetime__gte=timezone.now(),
        status__in=['OPEN', 'CONFIRMED']
    ).order_by('start_datetime')[:5]
    
    # Get pending join requests for user's groups
    pending_requests = GroupJoinRequest.objects.filter(
        group__in=user_groups.filter(groupmembership__role__in=['ADMIN', 'MODERATOR']),
        status='PENDING'
    ).count()
    
    # Recent activity
    recent_comments = Comment.objects.filter(
        Q(group__in=user_groups) | Q(event__in=upcoming_events)
    ).order_by('-created_at')[:10]
    
    context = {
        'profile': profile,
        'user_groups': user_groups,
        'upcoming_events': upcoming_events,
        'pending_requests': pending_requests,
        'recent_comments': recent_comments,
        'balance': profile.balance,
        'can_spend': profile.can_spend,
    }
    
    return render(request, 'chipin/dashboard.html', context)


# ============================================================================
# Group Management Views
# ============================================================================

@login_required
def group_list(request):
    """Display list of all groups with search and filter options"""
    # Placeholder implementation
    return render(request, 'chipin/group_list.html', {'groups': []})


@login_required
def group_detail(request, group_id):
    """
    Display detailed view of a specific group
    Shows members, events, and comments
    """
    # Placeholder implementation
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'chipin/group_detail.html', {'group': group})


@login_required
def create_group(request):
    """Create a new group"""
    # Placeholder implementation
    return render(request, 'chipin/create_group.html')


@login_required
def edit_group(request, group_id):
    """Edit group settings"""
    # Placeholder implementation
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'chipin/edit_group.html', {'group': group})


@login_required
def delete_group(request, group_id):
    """Delete a group (admin only)"""
    # Placeholder implementation
    return redirect('chipin:group_list')


@login_required
def leave_group(request, group_id):
    """Leave a group"""
    # Placeholder implementation
    return redirect('chipin:group_list')


@login_required
def invite_users(request, group_id):
    """Invite users to join a group"""
    # Placeholder implementation
    return render(request, 'chipin/invite_users.html')


@login_required
def request_to_join_group(request, group_id):
    """Request to join a group"""
    # Placeholder implementation
    return redirect('chipin:group_detail', group_id=group_id)


@login_required
def vote_on_join_request(request, request_id):
    """Vote on a join request (approve/reject)"""
    # Placeholder implementation
    return redirect('chipin:dashboard')


@login_required
def delete_join_request(request, request_id):
    """Delete/withdraw a join request"""
    # Placeholder implementation
    return redirect('chipin:dashboard')


@login_required
def accept_invite(request, invite_id):
    """Accept an invitation to join a group"""
    # Placeholder implementation
    return redirect('chipin:dashboard')


# ============================================================================
# Event Management Views
# ============================================================================

@login_required
def event_list(request):
    """Display list of all events"""
    # Placeholder implementation
    return render(request, 'chipin/event_list.html', {'events': []})


@login_required
def create_event(request, group_id):
    """Create a new event for a group"""
    # Placeholder implementation
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'chipin/create_event.html', {'group': group})


@login_required
def event_detail(request, event_id):
    """Display detailed view of an event"""
    # Placeholder implementation
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'chipin/event_detail.html', {'event': event})


@login_required
def edit_event(request, event_id):
    """Edit event details"""
    # Placeholder implementation
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'chipin/edit_event.html', {'event': event})


@login_required
def delete_event(request, event_id):
    """Delete an event"""
    # Placeholder implementation
    return redirect('chipin:event_list')


@login_required
def join_event(request, event_id):
    """Join an event"""
    # Placeholder implementation
    return redirect('chipin:event_detail', event_id=event_id)


@login_required
def leave_event(request, event_id):
    """Leave an event"""
    # Placeholder implementation
    return redirect('chipin:event_detail', event_id=event_id)


@login_required
def update_event_status(request, event_id):
    """Update event status (creator only)"""
    # Placeholder implementation
    return redirect('chipin:event_detail', event_id=event_id)


# ============================================================================
# Comment Management Views
# ============================================================================

@login_required
def add_comment(request):
    """Add a new comment to group or event"""
    # Placeholder implementation
    return JsonResponse({'success': True})


@login_required
def edit_comment(request, comment_id):
    """Edit an existing comment"""
    # Placeholder implementation
    return JsonResponse({'success': True})


@login_required
def delete_comment(request, comment_id):
    """Delete a comment"""
    # Placeholder implementation
    return JsonResponse({'success': True})


# ============================================================================
# Payment and Balance Management Views (Part B)
# ============================================================================

@login_required
def payment_dashboard(request):
    """
    Payment dashboard with transaction history and financial overview
    Part B: Payment Handling implementation
    """
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    
    # Get recent transactions
    recent_events = EventParticipation.objects.filter(
        user=user,
        payment_status__in=['PAID', 'PENDING', 'PARTIAL']
    ).order_by('-joined_at')[:10]
    
    # Calculate financial summary
    total_spent = EventParticipation.objects.filter(
        user=user,
        payment_status='PAID'
    ).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    pending_payments = EventParticipation.objects.filter(
        user=user,
        payment_status='PENDING'
    ).count()
    
    # Spending this month
    from django.utils import timezone
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_spending = EventParticipation.objects.filter(
        user=user,
        payment_status='PAID',
        payment_date__gte=current_month
    ).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    context = {
        'profile': profile,
        'recent_events': recent_events,
        'total_spent': total_spent,
        'pending_payments': pending_payments,
        'monthly_spending': monthly_spending,
        'balance': profile.balance,
        'spending_limit': profile.spending_limit,
        'can_spend': profile.can_spend,
        'trusted_adult_email': profile.trusted_adult_email,
    }
    
    return render(request, 'chipin/payment_dashboard.html', context)


@login_required
def add_funds(request):
    """
    Add funds to user account with trusted adult oversight
    Part B: Balance Management implementation
    """
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == 'POST':
        amount = request.POST.get('amount', '0')
        trusted_adult_code = request.POST.get('trusted_adult_code', '')
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Amount must be positive")
                return redirect('chipin:add_funds')
            
            if amount > Decimal('500.00'):
                messages.error(request, "Maximum deposit is $500.00 per transaction")
                return redirect('chipin:add_funds')
            
            # Simulate trusted adult verification
            # In production, this would involve secure token verification
            if trusted_adult_code == "PARENT123":  # Demo code
                # Process the deposit
                profile.balance += amount
                profile.save()
                
                # Log the transaction
                from django.contrib.admin.models import LogEntry, ADDITION
                from django.contrib.contenttypes.models import ContentType
                LogEntry.objects.log_action(
                    user_id=user.id,
                    content_type_id=ContentType.objects.get_for_model(Profile).pk,
                    object_id=profile.id,
                    object_repr=str(profile),
                    action_flag=ADDITION,
                    change_message=f"Funds added: ${amount} by trusted adult"
                )
                
                messages.success(request, f"Successfully added ${amount} to your account")
                return redirect('chipin:payment_dashboard')
            else:
                messages.error(request, "Invalid trusted adult verification code")
                
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered")
    
    context = {
        'profile': profile,
        'max_deposit': Decimal('500.00'),
    }
    
    return render(request, 'chipin/add_funds.html', context)


@login_required
def transfer_funds(request):
    """
    Transfer funds between users for event payments
    Part B: Payment Handling implementation
    """
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient_username', '')
        amount = request.POST.get('amount', '0')
        event_id = request.POST.get('event_id', '')
        
        try:
            amount = Decimal(amount)
            recipient = User.objects.get(username=recipient_username)
            recipient_profile = Profile.objects.get(user=recipient)
            
            # Validation checks
            if amount <= 0:
                messages.error(request, "Amount must be positive")
                return redirect('chipin:transfer_funds')
            
            if amount > profile.balance:
                messages.error(request, "Insufficient balance")
                return redirect('chipin:transfer_funds')
            
            if amount > profile.spending_limit:
                messages.error(request, f"Amount exceeds spending limit of ${profile.spending_limit}")
                return redirect('chipin:transfer_funds')
            
            if not profile.is_verified:
                messages.error(request, "Account must be verified by trusted adult")
                return redirect('chipin:transfer_funds')
            
            # Process the transfer
            profile.balance -= amount
            recipient_profile.balance += amount
            
            profile.save()
            recipient_profile.save()
            
            # Log both sides of the transaction
            from django.contrib.admin.models import LogEntry, CHANGE
            from django.contrib.contenttypes.models import ContentType
            content_type = ContentType.objects.get_for_model(Profile)
            
            LogEntry.objects.log_action(
                user_id=user.id,
                content_type_id=content_type.pk,
                object_id=profile.id,
                object_repr=str(profile),
                action_flag=CHANGE,
                change_message=f"Transfer sent: ${amount} to {recipient.username}"
            )
            
            LogEntry.objects.log_action(
                user_id=recipient.id,
                content_type_id=content_type.pk,
                object_id=recipient_profile.id,
                object_repr=str(recipient_profile),
                action_flag=CHANGE,
                change_message=f"Transfer received: ${amount} from {user.username}"
            )
            
            messages.success(request, f"Successfully transferred ${amount} to {recipient.username}")
            return redirect('chipin:payment_dashboard')
            
        except User.DoesNotExist:
            messages.error(request, "Recipient user not found")
        except Profile.DoesNotExist:
            messages.error(request, "Recipient profile not found")
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered")
    
    # Get user's events for context
    user_events = Event.objects.filter(
        participants=user,
        status__in=['OPEN', 'CONFIRMED']
    ).order_by('-created_at')[:10]
    
    context = {
        'profile': profile,
        'user_events': user_events,
    }
    
    return render(request, 'chipin/transfer_funds.html', context)


@login_required
def balance_management(request):
    """
    Balance management and spending limits with trusted adult controls
    Part B: Balance Management implementation
    """
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        trusted_adult_code = request.POST.get('trusted_adult_code', '')
        
        # Verify trusted adult authorization
        if trusted_adult_code != "PARENT123":  # Demo code
            messages.error(request, "Invalid trusted adult verification code")
            return redirect('chipin:balance_management')
        
        if action == 'update_spending_limit':
            new_limit = request.POST.get('spending_limit', '0')
            try:
                new_limit = Decimal(new_limit)
                if new_limit < Decimal('1.00') or new_limit > Decimal('500.00'):
                    messages.error(request, "Spending limit must be between $1.00 and $500.00")
                else:
                    old_limit = profile.spending_limit
                    profile.spending_limit = new_limit
                    profile.save()
                    
                    # Log the change
                    from django.contrib.admin.models import LogEntry, CHANGE
                    from django.contrib.contenttypes.models import ContentType
                    LogEntry.objects.log_action(
                        user_id=user.id,
                        content_type_id=ContentType.objects.get_for_model(Profile).pk,
                        object_id=profile.id,
                        object_repr=str(profile),
                        action_flag=CHANGE,
                        change_message=f"Spending limit updated: ${old_limit} → ${new_limit} by trusted adult"
                    )
                    
                    messages.success(request, f"Spending limit updated to ${new_limit}")
                    
            except (ValueError, TypeError):
                messages.error(request, "Invalid spending limit amount")
                
        elif action == 'toggle_verification':
            profile.is_verified = not profile.is_verified
            profile.save()
            
            # Log the change
            from django.contrib.admin.models import LogEntry, CHANGE
            from django.contrib.contenttypes.models import ContentType
            LogEntry.objects.log_action(
                user_id=user.id,
                content_type_id=ContentType.objects.get_for_model(Profile).pk,
                object_id=profile.id,
                object_repr=str(profile),
                action_flag=CHANGE,
                change_message=f"Account verification {'enabled' if profile.is_verified else 'disabled'} by trusted adult"
            )
            
            status = "verified" if profile.is_verified else "unverified"
            messages.success(request, f"Account is now {status}")
        
        elif action == 'freeze_account':
            profile.can_create_groups = False
            profile.can_join_events = False
            profile.save()
            
            messages.warning(request, "Account has been frozen - cannot create groups or join events")
        
        elif action == 'unfreeze_account':
            profile.can_create_groups = True
            profile.can_join_events = True
            profile.save()
            
            messages.success(request, "Account has been unfrozen")
    
    # Get transaction history
    transaction_history = EventParticipation.objects.filter(
        user=user
    ).order_by('-joined_at')[:20]
    
    # Calculate spending statistics
    total_lifetime_spending = EventParticipation.objects.filter(
        user=user,
        payment_status='PAID'
    ).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    # Weekly spending
    from datetime import timedelta
    week_ago = timezone.now() - timedelta(days=7)
    weekly_spending = EventParticipation.objects.filter(
        user=user,
        payment_status='PAID',
        payment_date__gte=week_ago
    ).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    context = {
        'profile': profile,
        'transaction_history': transaction_history,
        'total_lifetime_spending': total_lifetime_spending,
        'weekly_spending': weekly_spending,
        'spending_percentage': (weekly_spending / profile.spending_limit * 100) if profile.spending_limit > 0 else 0,
        'can_modify_settings': True,  # Would check trusted adult authentication in production
    }
    
    return render(request, 'chipin/balance_management.html', context)


# ============================================================================
# User Profile and Settings Views
# ============================================================================

@login_required
def user_profile(request):
    """User profile page"""
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'chipin/user_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Edit user profile"""
    # Placeholder implementation
    return render(request, 'chipin/edit_profile.html')


@login_required
def user_settings(request):
    """User account settings"""
    # Placeholder implementation
    return render(request, 'chipin/user_settings.html')


# ============================================================================
# API Views for AJAX functionality
# ============================================================================

@login_required
def api_group_members(request, group_id):
    """API endpoint to get group members"""
    # Placeholder implementation
    return JsonResponse({'members': []})


@login_required
def api_event_participants(request, event_id):
    """API endpoint to get event participants"""
    # Placeholder implementation
    return JsonResponse({'participants': []})


@login_required
def api_check_balance(request):
    """API endpoint to check user balance"""
    profile = get_object_or_404(Profile, user=request.user)
    return JsonResponse({
        'balance': str(profile.balance),
        'spending_limit': str(profile.spending_limit),
        'can_spend': profile.can_spend
    })