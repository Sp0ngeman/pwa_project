"""
ChipIn App Models - Secure Social Media Platform for Students
=============================================================

This module defines the core models for the ChipIn platform:
- Group: Student collaborative groups for event cost sharing
- GroupJoinRequest: Requests to join existing groups
- Event: Events with shared costs
- Comment: Comments on groups/events
- Profile: Extended user profile information

ChipIn enables students to:
1. Form groups for collaborative spending
2. Create events with shared costs
3. Manage balances securely with trusted adult oversight
4. Chat and organize events safely
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Profile(models.Model):
    """
    Extended user profile for ChipIn platform
    Links to Django's built-in User model with additional student-specific fields
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Student information
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique student identifier")
    date_of_birth = models.DateField(help_text="Used for age verification and parental controls")
    
    # Financial security - trusted adult oversight
    trusted_adult_email = models.EmailField(help_text="Email of parent/guardian who manages balance")
    trusted_adult_phone = models.CharField(max_length=20, help_text="Emergency contact number")
    
    # Account balance and limits
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Current account balance - managed by trusted adult"
    )
    spending_limit = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('50.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Maximum spending limit per transaction"
    )
    
    # Account settings
    is_verified = models.BooleanField(default=False, help_text="Account verified by trusted adult")
    can_create_groups = models.BooleanField(default=True, help_text="Permission to create new groups")
    can_join_events = models.BooleanField(default=True, help_text="Permission to join events")
    
    # Privacy and safety
    privacy_level = models.CharField(
        max_length=20,
        choices=[
            ('PUBLIC', 'Public - visible to all students'),
            ('FRIENDS', 'Friends only'),
            ('PRIVATE', 'Private - invitation only')
        ],
        default='FRIENDS',
        help_text="Profile visibility setting"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__username']
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - ID: {self.student_id}"
    
    @property
    def can_spend(self):
        """Check if user has sufficient balance for spending"""
        return self.balance > 0 and self.is_verified
    
    @property
    def full_name(self):
        """Get user's full name or username as fallback"""
        return self.user.get_full_name() or self.user.username


class Group(models.Model):
    """
    Collaborative groups for students to organize and share event costs
    Groups provide a secure environment for financial collaboration
    """
    # Basic group information
    name = models.CharField(max_length=100, help_text="Group name visible to members")
    description = models.TextField(help_text="Description of group purpose and activities")
    
    # Group management
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_groups',
        help_text="User who created this group"
    )
    members = models.ManyToManyField(
        User, 
        through='GroupMembership', 
        related_name='joined_groups',
        help_text="All group members"
    )
    
    # Group settings
    is_public = models.BooleanField(
        default=False, 
        help_text="Public groups can be discovered by other students"
    )
    requires_approval = models.BooleanField(
        default=True, 
        help_text="New members need approval from admin/creator"
    )
    max_members = models.PositiveIntegerField(
        default=50, 
        help_text="Maximum number of group members"
    )
    
    # Financial settings
    default_split_method = models.CharField(
        max_length=20,
        choices=[
            ('EQUAL', 'Split equally among participants'),
            ('CUSTOM', 'Custom amounts per participant'),
            ('PERCENTAGE', 'Percentage-based splitting')
        ],
        default='EQUAL',
        help_text="Default method for splitting event costs"
    )
    
    # Group status
    is_active = models.BooleanField(default=True, help_text="Active groups can create events")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"
    
    def __str__(self):
        return f"{self.name} (Creator: {self.creator.username})"
    
    @property
    def member_count(self):
        """Get current number of group members"""
        return self.members.count()
    
    @property
    def can_add_members(self):
        """Check if group can accept new members"""
        return self.is_active and self.member_count < self.max_members


class GroupMembership(models.Model):
    """
    Through model for Group-User relationship with additional member data
    Tracks member roles, join dates, and permissions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    # Member role and permissions
    role = models.CharField(
        max_length=20,
        choices=[
            ('ADMIN', 'Group Administrator'),
            ('MODERATOR', 'Group Moderator'),
            ('MEMBER', 'Regular Member')
        ],
        default='MEMBER',
        help_text="Member's role and permissions level"
    )
    
    # Member status
    is_active = models.BooleanField(default=True, help_text="Active membership status")
    can_invite_others = models.BooleanField(default=False, help_text="Permission to invite new members")
    can_create_events = models.BooleanField(default=True, help_text="Permission to create group events")
    
    # Timestamps
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'group']
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name} ({self.role})"


class GroupJoinRequest(models.Model):
    """
    Requests to join groups that require approval
    Handles the approval workflow for new group members
    """
    # Request details
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='join_requests',
        help_text="User requesting to join the group"
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='join_requests',
        help_text="Group being requested to join"
    )
    
    # Request message and reasoning
    message = models.TextField(
        blank=True, 
        help_text="Optional message from user explaining why they want to join"
    )
    
    # Request status tracking
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Awaiting approval'),
            ('APPROVED', 'Request approved'),
            ('REJECTED', 'Request rejected'),
            ('WITHDRAWN', 'Request withdrawn by user')
        ],
        default='PENDING',
        help_text="Current status of the join request"
    )
    
    # Approval workflow
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_requests',
        help_text="Group admin/moderator who reviewed this request"
    )
    review_message = models.TextField(
        blank=True, 
        help_text="Optional message from reviewer"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'group']
        ordering = ['-created_at']
        verbose_name = "Group Join Request"
        verbose_name_plural = "Group Join Requests"
    
    def __str__(self):
        return f"{self.user.username} → {self.group.name} ({self.status})"


class Event(models.Model):
    """
    Events created by groups with shared costs and participant management
    Core functionality for collaborative expense sharing
    """
    # Basic event information
    title = models.CharField(max_length=200, help_text="Event title/name")
    description = models.TextField(help_text="Detailed event description")
    
    # Event organization
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='events',
        help_text="Group organizing this event"
    )
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_events',
        help_text="Group member who created this event"
    )
    
    # Event scheduling
    start_datetime = models.DateTimeField(help_text="Event start date and time")
    end_datetime = models.DateTimeField(help_text="Event end date and time")
    location = models.CharField(max_length=255, help_text="Event location/venue")
    
    # Financial details
    total_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Total cost of the event"
    )
    cost_per_person = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Calculated cost per participant (auto-calculated)"
    )
    
    # Participant management
    participants = models.ManyToManyField(
        User, 
        through='EventParticipation', 
        related_name='participating_events',
        help_text="Users participating in this event"
    )
    max_participants = models.PositiveIntegerField(
        default=20, 
        help_text="Maximum number of participants"
    )
    min_participants = models.PositiveIntegerField(
        default=2, 
        help_text="Minimum participants required for event to proceed"
    )
    
    # Event settings
    requires_payment = models.BooleanField(
        default=True, 
        help_text="Event requires payment from participants"
    )
    payment_deadline = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="Deadline for participant payments"
    )
    
    # Event status
    status = models.CharField(
        max_length=20,
        choices=[
            ('DRAFT', 'Draft - not yet published'),
            ('OPEN', 'Open for registration'),
            ('FULL', 'Full - no more participants'),
            ('CONFIRMED', 'Confirmed - event will proceed'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Event completed')
        ],
        default='DRAFT',
        help_text="Current event status"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_datetime']
        verbose_name = "Group Event"
        verbose_name_plural = "Group Events"
    
    def __str__(self):
        return f"{self.title} - {self.group.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Auto-calculate cost per person when saving"""
        if self.total_cost and self.participants.count() > 0:
            self.cost_per_person = self.total_cost / self.participants.count()
        super().save(*args, **kwargs)
    
    @property
    def participant_count(self):
        """Get current number of participants"""
        return self.participants.count()
    
    @property
    def can_join(self):
        """Check if event can accept new participants"""
        return (self.status == 'OPEN' and 
                self.participant_count < self.max_participants)
    
    @property
    def is_full(self):
        """Check if event has reached maximum participants"""
        return self.participant_count >= self.max_participants


class EventParticipation(models.Model):
    """
    Through model for Event-User participation with payment tracking
    Manages participant status, payments, and cost allocation
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    # Participation details
    joined_at = models.DateTimeField(auto_now_add=True)
    custom_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Custom amount if not splitting equally"
    )
    
    # Payment status
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Payment pending'),
            ('PAID', 'Payment completed'),
            ('PARTIAL', 'Partial payment made'),
            ('REFUNDED', 'Payment refunded'),
            ('WAIVED', 'Payment waived')
        ],
        default='PENDING',
        help_text="Current payment status"
    )
    amount_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Amount already paid by participant"
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Participation status
    attendance_status = models.CharField(
        max_length=20,
        choices=[
            ('CONFIRMED', 'Will attend'),
            ('MAYBE', 'Maybe attending'),
            ('DECLINED', 'Will not attend'),
            ('NO_RESPONSE', 'No response yet')
        ],
        default='CONFIRMED',
        help_text="Participant's attendance confirmation"
    )
    
    class Meta:
        unique_together = ['user', 'event']
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.user.username} → {self.event.title} ({self.payment_status})"
    
    @property
    def amount_owed(self):
        """Calculate amount still owed by participant"""
        if self.custom_amount:
            return max(self.custom_amount - self.amount_paid, Decimal('0.00'))
        return max(self.event.cost_per_person - self.amount_paid, Decimal('0.00'))


class Comment(models.Model):
    """
    Comments system for groups and events
    Enables communication and discussion within the platform
    """
    # Comment content
    content = models.TextField(help_text="Comment text content")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="User who wrote this comment"
    )
    
    # Comment targets (polymorphic relationship)
    # Comments can be on groups or events
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='comments',
        help_text="Group this comment belongs to (if applicable)"
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='comments',
        help_text="Event this comment belongs to (if applicable)"
    )
    
    # Comment threading
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='replies',
        help_text="Parent comment (for threaded discussions)"
    )
    
    # Comment status
    is_edited = models.BooleanField(default=False, help_text="Comment has been edited")
    is_deleted = models.BooleanField(default=False, help_text="Comment has been deleted")
    is_pinned = models.BooleanField(default=False, help_text="Important comment pinned by moderator")
    
    # Moderation
    is_flagged = models.BooleanField(default=False, help_text="Comment flagged for review")
    flagged_reason = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Reason for flagging"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        target = self.group.name if self.group else self.event.title
        return f"{self.author.username} on {target}: {self.content[:50]}..."
    
    def clean(self):
        """Validate that comment belongs to either group or event, not both"""
        from django.core.exceptions import ValidationError
        if self.group and self.event:
            raise ValidationError("Comment cannot belong to both group and event")
        if not self.group and not self.event:
            raise ValidationError("Comment must belong to either group or event")
    
    @property
    def target(self):
        """Get the target object (group or event) this comment belongs to"""
        return self.group or self.event
    
    @property
    def reply_count(self):
        """Get number of replies to this comment"""
        return self.replies.filter(is_deleted=False).count()


class Transaction(models.Model):
    """
    Financial transaction logging for ChipIn platform
    Tracks all monetary movements for security and audit purposes
    """
    # Transaction identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Transaction parties
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_transactions',
        help_text="User who sent the funds"
    )
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_transactions',
        help_text="User who received the funds"
    )
    
    # Transaction details
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Transaction amount"
    )
    
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('DEPOSIT', 'Trusted adult deposit'),
            ('TRANSFER', 'User-to-user transfer'),
            ('EVENT_PAYMENT', 'Event participation payment'),
            ('REFUND', 'Event refund'),
            ('WITHDRAWAL', 'Account withdrawal'),
            ('ADJUSTMENT', 'Balance adjustment')
        ],
        help_text="Type of financial transaction"
    )
    
    # Associated records
    event = models.ForeignKey(
        Event, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='transactions',
        help_text="Related event if applicable"
    )
    
    # Transaction status
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Transaction pending'),
            ('COMPLETED', 'Transaction completed'),
            ('FAILED', 'Transaction failed'),
            ('CANCELLED', 'Transaction cancelled'),
            ('REFUNDED', 'Transaction refunded')
        ],
        default='PENDING',
        help_text="Current transaction status"
    )
    
    # Additional information
    description = models.TextField(blank=True, help_text="Transaction description or notes")
    reference_code = models.CharField(max_length=50, blank=True, help_text="External reference code")
    
    # Trusted adult oversight
    requires_adult_approval = models.BooleanField(default=False, help_text="Requires trusted adult approval")
    approved_by_adult = models.BooleanField(default=False, help_text="Approved by trusted adult")
    adult_approval_date = models.DateTimeField(null=True, blank=True)
    
    # Security and audit
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="IP address of transaction")
    user_agent = models.TextField(blank=True, help_text="Browser user agent")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Financial Transaction"
        verbose_name_plural = "Financial Transactions"
        indexes = [
            models.Index(fields=['sender', 'created_at']),
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['transaction_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type}: ${self.amount} from {self.sender.username} to {self.recipient.username}"
    
    @property
    def is_large_transaction(self):
        """Check if transaction requires special oversight"""
        return self.amount > Decimal('100.00')
    
    def process_transaction(self):
        """Process the transaction by updating balances"""
        if self.status != 'PENDING':
            return False
        
        try:
            sender_profile = Profile.objects.get(user=self.sender)
            recipient_profile = Profile.objects.get(user=self.recipient)
            
            # Validation checks
            if self.transaction_type != 'DEPOSIT' and sender_profile.balance < self.amount:
                self.status = 'FAILED'
                self.description += " - Insufficient balance"
                self.save()
                return False
            
            if not sender_profile.is_verified and self.transaction_type != 'DEPOSIT':
                self.status = 'FAILED'
                self.description += " - Sender not verified"
                self.save()
                return False
            
            # Process balance changes
            if self.transaction_type == 'DEPOSIT':
                recipient_profile.balance += self.amount
            else:
                sender_profile.balance -= self.amount
                recipient_profile.balance += self.amount
            
            sender_profile.save()
            recipient_profile.save()
            
            self.status = 'COMPLETED'
            self.processed_at = timezone.now()
            self.save()
            
            return True
            
        except Profile.DoesNotExist:
            self.status = 'FAILED'
            self.description += " - Profile not found"
            self.save()
            return False