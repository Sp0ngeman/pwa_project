from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['parent__name', 'name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    @property
    def full_path(self):
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    
    priority = models.CharField(
        max_length=10,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('URGENT', 'Urgent')
        ],
        default='MEDIUM'
    )
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['completed', '-priority', 'due_date', '-created_at']
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.title}"
    
    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False
    
    @property
    def priority_display(self):
        priority_icons = {
            'LOW': '🟢',
            'MEDIUM': '🟡', 
            'HIGH': '🟠',
            'URGENT': '🔴'
        }
        return f"{priority_icons.get(self.priority, '')} {self.get_priority_display()}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    trusted_adult_email = models.EmailField()
    trusted_adult_phone = models.CharField(max_length=20)
    
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    spending_limit = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('50.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    is_verified = models.BooleanField(default=False)
    can_create_groups = models.BooleanField(default=True)
    can_join_events = models.BooleanField(default=True)
    
    privacy_level = models.CharField(
        max_length=20,
        choices=[
            ('PUBLIC', 'Public'),
            ('FRIENDS', 'Friends only'),
            ('PRIVATE', 'Private')
        ],
        default='FRIENDS'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
    
    @property
    def can_spend(self):
        return self.balance > 0 and self.is_verified
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='joined_groups')
    is_public = models.BooleanField(default=False)
    requires_approval = models.BooleanField(default=True)
    max_members = models.PositiveIntegerField(default=50)
    
    default_split_method = models.CharField(
        max_length=20,
        choices=[
            ('EQUAL', 'Split equally'),
            ('CUSTOM', 'Custom amounts'),
            ('PERCENTAGE', 'Percentage-based')
        ],
        default='EQUAL'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (Creator: {self.creator.username})"
    
    @property
    def member_count(self):
        return self.members.count()
    
    @property
    def can_add_members(self):
        return self.is_active and self.member_count < self.max_members


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    
    total_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    cost_per_person = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    
    participants = models.ManyToManyField(
        User, 
        through='EventParticipation', 
        related_name='participating_events'
    )
    max_participants = models.PositiveIntegerField(default=20)
    min_participants = models.PositiveIntegerField(default=2)
    
    requires_payment = models.BooleanField(default=True)
    payment_deadline = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('DRAFT', 'Draft'),
            ('OPEN', 'Open for registration'),
            ('FULL', 'Full'),
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Completed')
        ],
        default='DRAFT'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_datetime']
    
    def __str__(self):
        return f"{self.title} - {self.group.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        if self.total_cost and self.participants.count() > 0:
            self.cost_per_person = self.total_cost / self.participants.count()
        super().save(*args, **kwargs)
    
    @property
    def participant_count(self):
        return self.participants.count()
    
    @property
    def can_join(self):
        return (self.status == 'OPEN' and 
                self.participant_count < self.max_participants)


class EventParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    custom_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Payment pending'),
            ('PAID', 'Payment completed'),
            ('PARTIAL', 'Partial payment'),
            ('REFUNDED', 'Refunded'),
            ('WAIVED', 'Waived')
        ],
        default='PENDING'
    )
    amount_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    
    attendance_status = models.CharField(
        max_length=20,
        choices=[
            ('CONFIRMED', 'Will attend'),
            ('MAYBE', 'Maybe'),
            ('DECLINED', 'Declined'),
            ('NO_RESPONSE', 'No response')
        ],
        default='CONFIRMED'
    )
    
    class Meta:
        unique_together = ['user', 'event']
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.user.username} → {self.event.title} ({self.payment_status})"
    
    @property
    def amount_owed(self):
        if self.custom_amount:
            return max(self.custom_amount - self.amount_paid, Decimal('0.00'))
        return max(self.event.cost_per_person - self.amount_paid, Decimal('0.00'))


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('DEPOSIT', 'Deposit'),
            ('TRANSFER', 'Transfer'),
            ('EVENT_PAYMENT', 'Event payment'),
            ('REFUND', 'Refund'),
            ('WITHDRAWAL', 'Withdrawal'),
            ('ADJUSTMENT', 'Adjustment')
        ]
    )
    
    event = models.ForeignKey(
        Event, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='transactions'
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('COMPLETED', 'Completed'),
            ('FAILED', 'Failed'),
            ('CANCELLED', 'Cancelled'),
            ('REFUNDED', 'Refunded')
        ],
        default='PENDING'
    )
    
    description = models.TextField(blank=True)
    reference_code = models.CharField(max_length=50, blank=True)
    requires_adult_approval = models.BooleanField(default=False)
    approved_by_adult = models.BooleanField(default=False)
    adult_approval_date = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type}: ${self.amount} from {self.sender.username} to {self.recipient.username}"
    
    @property
    def is_large_transaction(self):
        return self.amount > Decimal('100.00')