from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse
from .models import Task, Category, Profile, Group, Event, EventParticipation, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db import transaction
from decimal import Decimal

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

@login_required
def index(request):
    user_tasks = Task.objects.filter(user=request.user)
    completed_tasks = user_tasks.filter(completed=True).count()
    pending_tasks = user_tasks.filter(completed=False).count()
    overdue_tasks = [task for task in user_tasks.filter(completed=False) if task.is_overdue]
    categories = Category.objects.all().order_by('parent__name', 'name')
    
    user_groups = Group.objects.filter(members=request.user)
    user_events = Event.objects.filter(participants=request.user)
    
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'student_id': f'STU{request.user.id:05d}',
            'trusted_adult_email': 'parent@example.com',
            'trusted_adult_phone': '555-0123'
        }
    )
    
    context = {
        "tasks": user_tasks,
        "categories": categories,
        "completed_count": completed_tasks,
        "pending_count": pending_tasks,
        "overdue_count": len(overdue_tasks),
        "user_groups": user_groups,
        "user_events": user_events,
        "profile": profile,
    }
    
    return render(request, "chipin/index.html", context)

@login_required
def add(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created successfully!")
            return HttpResponseRedirect(reverse("chipin:index"))
    else:
        form = NewTaskForm()
    
    categories = Category.objects.all()
    return render(request, "chipin/add.html", {
        "form": form,
        "categories": categories
    })

@login_required
def get_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    tasks_data = []
    
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'category': task.category.name if task.category else None,
            'priority': task.priority,
            'priority_display': task.priority_display,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'completed': task.completed,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'is_overdue': task.is_overdue,
            'created_at': task.created_at.isoformat(),
        })
    
    return JsonResponse({'tasks': tasks_data})

@login_required
def get_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'category': task.category.name if task.category else None,
        'priority': task.priority,
        'priority_display': task.priority_display,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'completed': task.completed,
        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        'is_overdue': task.is_overdue,
        'created_at': task.created_at.isoformat(),
    }
    
    return JsonResponse(data)

@csrf_exempt
@login_required
def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            category = None
            if data.get('category'):
                category, created = Category.objects.get_or_create(name=data['category'])
            
            due_date = None
            if data.get('due_date'):
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            
            task = Task.objects.create(
                user=request.user,
                title=data['title'],
                description=data.get('description', ''),
                category=category,
                priority=data.get('priority', 'MEDIUM'),
                due_date=due_date
            )
            
            return JsonResponse({
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'completed': task.completed,
                    'priority': task.priority,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required
def update_task(request, task_id):
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            data = json.loads(request.body)
            
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'priority' in data:
                task.priority = data['priority']
            if 'due_date' in data:
                if data['due_date']:
                    task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                else:
                    task.due_date = None
            if 'category' in data:
                if data['category']:
                    category, created = Category.objects.get_or_create(name=data['category'])
                    task.category = category
                else:
                    task.category = None
            
            task.save()
            
            return JsonResponse({
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'completed': task.completed,
                    'priority': task.priority,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task_title = task.title
            task.delete()
            
            messages.success(request, f"Task '{task_title}' deleted successfully!")
            return HttpResponseRedirect(reverse("chipin:index"))
            
        except Exception as e:
            messages.error(request, f"Error deleting task: {str(e)}")
            return HttpResponseRedirect(reverse("chipin:index"))
    
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
@login_required
def toggle_task(request, task_id):
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task.completed = not task.completed
            task.save()
            
            status = "completed" if task.completed else "reopened"
            messages.success(request, f"Task '{task.title}' {status}!")
            return HttpResponseRedirect(reverse("chipin:index"))
            
        except Exception as e:
            messages.error(request, f"Error updating task: {str(e)}")
            return HttpResponseRedirect(reverse("chipin:index"))
    
    return HttpResponseNotAllowed(['POST'])

@login_required
def task_stats(request):
    user_tasks = Task.objects.filter(user=request.user)
    
    stats = {
        'total': user_tasks.count(),
        'completed': user_tasks.filter(completed=True).count(),
        'pending': user_tasks.filter(completed=False).count(),
        'overdue': len([task for task in user_tasks.filter(completed=False) if task.is_overdue]),
        'by_priority': {
            'HIGH': user_tasks.filter(priority='HIGH', completed=False).count(),
            'MEDIUM': user_tasks.filter(priority='MEDIUM', completed=False).count(),
            'LOW': user_tasks.filter(priority='LOW', completed=False).count(),
            'URGENT': user_tasks.filter(priority='URGENT', completed=False).count(),
        },
        'by_category': {}
    }
    
    for category in Category.objects.all():
        count = user_tasks.filter(category=category, completed=False).count()
        if count > 0:
            stats['by_category'][category.name] = count
    
    return JsonResponse(stats)

@csrf_exempt
@login_required
def bulk_update(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_ids = data.get('task_ids', [])
            action = data.get('action', '')
            
            tasks = Task.objects.filter(id__in=task_ids, user=request.user)
            
            if action == 'complete':
                tasks.update(completed=True)
                count = tasks.count()
                return JsonResponse({
                    'success': True, 
                    'message': f'{count} tasks marked as completed'
                })
            elif action == 'delete':
                count = tasks.count()
                tasks.delete()
                return JsonResponse({
                    'success': True, 
                    'message': f'{count} tasks deleted'
                })
            elif action == 'set_priority':
                priority = data.get('priority', 'MEDIUM')
                tasks.update(priority=priority)
                count = tasks.count()
                return JsonResponse({
                    'success': True, 
                    'message': f'{count} tasks updated to {priority} priority'
                })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def payment_dashboard(request):
    user = request.user
    
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'student_id': f'STU{user.id:05d}',
            'trusted_adult_email': 'parent@example.com',
            'trusted_adult_phone': '555-0123'
        }
    )
    
    recent_events = EventParticipation.objects.filter(
        user=user,
        payment_status__in=['PAID', 'PENDING', 'PARTIAL']
    ).order_by('-joined_at')[:10]
    
    total_spent = EventParticipation.objects.filter(
        user=user,
        payment_status='PAID'
    ).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    pending_payments = EventParticipation.objects.filter(
        user=user,
        payment_status='PENDING'
    ).count()
    
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
    user = request.user
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'student_id': f'STU{user.id:05d}',
            'trusted_adult_email': 'parent@example.com',
            'trusted_adult_phone': '555-0123'
        }
    )
    
    if request.method == 'POST':
        amount = request.POST.get('amount', '0')
        trusted_adult_code = request.POST.get('trusted_adult_code', '')
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Amount must be positive")
                return HttpResponseRedirect(reverse('chipin:add_funds'))
            
            if amount > Decimal('500.00'):
                messages.error(request, "Maximum deposit is $500.00 per transaction")
                return HttpResponseRedirect(reverse('chipin:add_funds'))
            
            if trusted_adult_code == "PARENT123":
                profile.balance += amount
                profile.save()
                
                Transaction.objects.create(
                    sender=user,
                    recipient=user,
                    amount=amount,
                    transaction_type='DEPOSIT',
                    status='COMPLETED',
                    description=f"Funds added by trusted adult",
                    approved_by_adult=True,
                    adult_approval_date=timezone.now()
                )
                
                messages.success(request, f"Successfully added ${amount} to your account")
                return HttpResponseRedirect(reverse('chipin:payment_dashboard'))
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
    user = request.user
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'student_id': f'STU{user.id:05d}',
            'trusted_adult_email': 'parent@example.com',
            'trusted_adult_phone': '555-0123'
        }
    )
    
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient_username', '')
        amount = request.POST.get('amount', '0')
        
        try:
            amount = Decimal(amount)
            recipient = User.objects.get(username=recipient_username)
            recipient_profile, _ = Profile.objects.get_or_create(
                user=recipient,
                defaults={
                    'student_id': f'STU{recipient.id:05d}',
                    'trusted_adult_email': 'parent@example.com',
                    'trusted_adult_phone': '555-0123'
                }
            )
            
            if amount <= 0:
                messages.error(request, "Amount must be positive")
                return HttpResponseRedirect(reverse('chipin:transfer_funds'))
            
            if amount > profile.balance:
                messages.error(request, "Insufficient balance")
                return HttpResponseRedirect(reverse('chipin:transfer_funds'))
            
            if amount > profile.spending_limit:
                messages.error(request, f"Amount exceeds spending limit of ${profile.spending_limit}")
                return HttpResponseRedirect(reverse('chipin:transfer_funds'))
            
            if not profile.is_verified:
                messages.error(request, "Account must be verified by trusted adult")
                return HttpResponseRedirect(reverse('chipin:transfer_funds'))
            
            with transaction.atomic():
                profile.balance -= amount
                recipient_profile.balance += amount
                
                profile.save()
                recipient_profile.save()
                
                Transaction.objects.create(
                    sender=user,
                    recipient=recipient,
                    amount=amount,
                    transaction_type='TRANSFER',
                    status='COMPLETED',
                    description=f"Transfer from {user.username} to {recipient.username}",
                    processed_at=timezone.now()
                )
            
            messages.success(request, f"Successfully transferred ${amount} to {recipient.username}")
            return HttpResponseRedirect(reverse('chipin:payment_dashboard'))
            
        except User.DoesNotExist:
            messages.error(request, "Recipient user not found")
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered")
    
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
    user = request.user
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'student_id': f'STU{user.id:05d}',
            'trusted_adult_email': 'parent@example.com',
            'trusted_adult_phone': '555-0123'
        }
    )
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        trusted_adult_code = request.POST.get('trusted_adult_code', '')
        
        if trusted_adult_code != "PARENT123":
            messages.error(request, "Invalid trusted adult verification code")
            return HttpResponseRedirect(reverse('chipin:balance_management'))
        
        if action == 'update_spending_limit':
            new_limit = request.POST.get('spending_limit', '0')
            try:
                new_limit = Decimal(new_limit)
                if new_limit < Decimal('1.00') or new_limit > Decimal('500.00'):
                    messages.error(request, "Spending limit must be between $1.00 and $500.00")
                else:
                    profile.spending_limit = new_limit
                    profile.save()
                    messages.success(request, f"Spending limit updated to ${new_limit}")
                    
            except (ValueError, TypeError):
                messages.error(request, "Invalid spending limit amount")
                
        elif action == 'toggle_verification':
            profile.is_verified = not profile.is_verified
            profile.save()
            status = "verified" if profile.is_verified else "unverified"
            messages.success(request, f"Account is now {status}")
        
        elif action == 'freeze_account':
            profile.can_create_groups = False
            profile.can_join_events = False
            profile.save()
            messages.warning(request, "Account has been frozen")
        
        elif action == 'unfreeze_account':
            profile.can_create_groups = True
            profile.can_join_events = True
            profile.save()
            messages.success(request, "Account has been unfrozen")
    
    transaction_history = Transaction.objects.filter(
        Q(sender=user) | Q(recipient=user)
    ).order_by('-created_at')[:20]
    
    total_lifetime_spending = Transaction.objects.filter(
        sender=user,
        status='COMPLETED',
        transaction_type__in=['TRANSFER', 'EVENT_PAYMENT']
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    from datetime import timedelta
    week_ago = timezone.now() - timedelta(days=7)
    weekly_spending = Transaction.objects.filter(
        sender=user,
        status='COMPLETED',
        transaction_type__in=['TRANSFER', 'EVENT_PAYMENT'],
        created_at__gte=week_ago
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    context = {
        'profile': profile,
        'transaction_history': transaction_history,
        'total_lifetime_spending': total_lifetime_spending,
        'weekly_spending': weekly_spending,
        'spending_percentage': (weekly_spending / profile.spending_limit * 100) if profile.spending_limit > 0 else 0,
        'can_modify_settings': True,
    }
    
    return render(request, 'chipin/balance_management.html', context)