"""
ChipIn App URLs
===============

URL patterns for the ChipIn student collaborative platform.
Handles routing for groups, events, payments, and social features.
"""

from django.urls import path
from . import views

app_name = 'chipin'

urlpatterns = [
    # Home and dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Group management URLs
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('groups/<int:group_id>/leave/', views.leave_group, name='leave_group'),
    
    # Group membership management
    path('groups/<int:group_id>/invite/', views.invite_users, name='invite_users'),
    path('groups/<int:group_id>/join/', views.request_to_join_group, name='request_to_join_group'),
    path('join-requests/<int:request_id>/vote/', views.vote_on_join_request, name='vote_on_join_request'),
    path('join-requests/<int:request_id>/delete/', views.delete_join_request, name='delete_join_request'),
    path('invites/<int:invite_id>/accept/', views.accept_invite, name='accept_invite'),
    
    # Event management URLs
    path('events/', views.event_list, name='event_list'),
    path('groups/<int:group_id>/events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('events/<int:event_id>/join/', views.join_event, name='join_event'),
    path('events/<int:event_id>/leave/', views.leave_event, name='leave_event'),
    path('events/<int:event_id>/update-status/', views.update_event_status, name='update_event_status'),
    
    # Comment management
    path('comments/add/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # Payment and balance management (Part B features)
    path('payments/', views.payment_dashboard, name='payment_dashboard'),
    path('payments/add-funds/', views.add_funds, name='add_funds'),
    path('payments/transfer/', views.transfer_funds, name='transfer_funds'),
    path('balance/', views.balance_management, name='balance_management'),
    
    # User profile and settings
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('settings/', views.user_settings, name='user_settings'),
    
    # API endpoints for AJAX functionality
    path('api/groups/<int:group_id>/members/', views.api_group_members, name='api_group_members'),
    path('api/events/<int:event_id>/participants/', views.api_event_participants, name='api_event_participants'),
    path('api/balance/check/', views.api_check_balance, name='api_check_balance'),
]