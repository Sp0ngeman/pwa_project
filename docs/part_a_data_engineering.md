# Part A - Data Engineering (10 marks)
## ChipIn Platform - Data Dictionary and Class Diagrams

### Overview
This document provides comprehensive data modeling for the ChipIn secure social media platform, including detailed data dictionary and class diagrams for all required models with appropriate relationships.

---

## 1. Data Dictionary

### 1.1 ChipIn App - class Group

| Field Name | Data Type | Size/Constraints | Description | Validation Rules |
|------------|-----------|------------------|-------------|------------------|
| **Primary Key** |
| id | Integer | Auto-increment | Unique group identifier | System generated |
| **Basic Information** |
| name | CharField | max_length=100, not null | Group display name | 3-100 characters, unique per creator |
| description | TextField | not null | Group purpose and activities | Max 1000 characters |
| **Management** |
| creator | ForeignKey(User) | on_delete=CASCADE, not null | User who created the group | Must be verified user |
| **Settings** |
| is_public | BooleanField | default=False | Group visibility to other users | Boolean |
| requires_approval | BooleanField | default=True | New members need approval | Boolean |
| max_members | PositiveIntegerField | default=50 | Maximum group size | Range: 2-100 |
| default_split_method | CharField | max_length=20, default='EQUAL' | Cost splitting preference | EQUAL/CUSTOM/PERCENTAGE |
| **Status** |
| is_active | BooleanField | default=True | Group operational status | Boolean |
| **Timestamps** |
| created_at | DateTimeField | auto_now_add=True | Group creation timestamp | System generated |
| updated_at | DateTimeField | auto_now=True | Last modification timestamp | System generated |

**Business Rules:**
- Creator automatically becomes admin
- Only verified users can create groups
- Public groups discoverable in search
- Max members cannot exceed 100 for safety

### 1.2 ChipIn App - class GroupJoinRequest

| Field Name | Data Type | Size/Constraints | Description | Validation Rules |
|------------|-----------|------------------|-------------|------------------|
| **Primary Key** |
| id | Integer | Auto-increment | Unique request identifier | System generated |
| **Request Details** |
| user | ForeignKey(User) | on_delete=CASCADE, not null | Requesting user | Must be verified |
| group | ForeignKey(Group) | on_delete=CASCADE, not null | Target group | Must be active |
| message | TextField | blank=True | Optional join reason | Max 500 characters |
| **Status Tracking** |
| status | CharField | max_length=20, default='PENDING' | Current request status | PENDING/APPROVED/REJECTED/WITHDRAWN |
| **Review Information** |
| reviewed_by | ForeignKey(User) | on_delete=SET_NULL, null=True | Admin who reviewed | Must have admin/moderator role |
| review_message | TextField | blank=True | Reviewer's response | Max 500 characters |
| reviewed_at | DateTimeField | null=True, blank=True | Review completion time | Set when status changes |
| **Timestamps** |
| created_at | DateTimeField | auto_now_add=True | Request creation time | System generated |
| updated_at | DateTimeField | auto_now=True | Last status change | System generated |

**Business Rules:**
- One pending request per user per group
- Only group admins/moderators can review
- Auto-expire after 30 days if not reviewed
- Cannot request to join if already member

### 1.3 ChipIn App - class Comment

| Field Name | Data Type | Size/Constraints | Description | Validation Rules |
|------------|-----------|------------------|-------------|------------------|
| **Primary Key** |
| id | Integer | Auto-increment | Unique comment identifier | System generated |
| **Content** |
| content | TextField | not null | Comment text content | 1-1000 characters |
| author | ForeignKey(User) | on_delete=CASCADE, not null | Comment author | Must be authenticated |
| **Target (Polymorphic)** |
| group | ForeignKey(Group) | on_delete=CASCADE, null=True | Parent group if group comment | Exactly one of group/event required |
| event | ForeignKey(Event) | on_delete=CASCADE, null=True | Parent event if event comment | Exactly one of group/event required |
| **Threading** |
| parent | ForeignKey(Comment) | on_delete=CASCADE, null=True | Parent comment for replies | Max 3 levels deep |
| **Status** |
| is_edited | BooleanField | default=False | Comment has been modified | Boolean |
| is_deleted | BooleanField | default=False | Soft delete flag | Boolean |
| is_pinned | BooleanField | default=False | Important comment flag | Admin/moderator only |
| **Moderation** |
| is_flagged | BooleanField | default=False | Flagged for review | Boolean |
| flagged_reason | CharField | max_length=100, blank=True | Reason for flagging | Predefined reasons |
| **Timestamps** |
| created_at | DateTimeField | auto_now_add=True | Comment creation time | System generated |
| updated_at | DateTimeField | auto_now=True | Last modification time | System generated |

**Business Rules:**
- Comments must belong to either group OR event (not both)
- Only author or moderators can edit/delete
- Deleted comments preserve thread structure
- Flagged comments require moderator review

### 1.4 ChipIn App - class Event

| Field Name | Data Type | Size/Constraints | Description | Validation Rules |
|------------|-----------|------------------|-------------|------------------|
| **Primary Key** |
| id | Integer | Auto-increment | Unique event identifier | System generated |
| **Basic Information** |
| title | CharField | max_length=200, not null | Event name/title | 3-200 characters |
| description | TextField | not null | Event details | Max 2000 characters |
| **Organization** |
| group | ForeignKey(Group) | on_delete=CASCADE, not null | Organizing group | Must be active group |
| creator | ForeignKey(User) | on_delete=CASCADE, not null | Event creator | Must be group member |
| **Schedule & Location** |
| start_datetime | DateTimeField | not null | Event start time | Must be future date |
| end_datetime | DateTimeField | not null | Event end time | Must be after start |
| location | CharField | max_length=255, not null | Event venue/location | 1-255 characters |
| **Financial Details** |
| total_cost | DecimalField | max_digits=10, decimal_places=2, not null | Total event cost | Positive value, max $99,999.99 |
| cost_per_person | DecimalField | max_digits=10, decimal_places=2, default=0 | Calculated individual cost | Auto-calculated |
| requires_payment | BooleanField | default=True | Payment required flag | Boolean |
| payment_deadline | DateTimeField | null=True, blank=True | Payment due date | Before start_datetime |
| **Participation** |
| max_participants | PositiveIntegerField | default=20 | Maximum attendees | Range: 2-50 |
| min_participants | PositiveIntegerField | default=2 | Minimum for event to proceed | Range: 2-max_participants |
| **Status** |
| status | CharField | max_length=20, default='DRAFT' | Event status | DRAFT/OPEN/FULL/CONFIRMED/CANCELLED/COMPLETED |
| **Timestamps** |
| created_at | DateTimeField | auto_now_add=True | Event creation time | System generated |
| updated_at | DateTimeField | auto_now=True | Last modification time | System generated |

**Business Rules:**
- Only group members can create events
- Cost per person auto-calculated when participants change
- Events auto-cancel if min participants not met by deadline
- Financial limits enforced based on user age/trusted adult settings

### 1.5 Users App - class Profile

| Field Name | Data Type | Size/Constraints | Description | Validation Rules |
|------------|-----------|------------------|-------------|------------------|
| **Primary Key** |
| id | Integer | Auto-increment | Unique profile identifier | System generated |
| **User Link** |
| user | OneToOneField(User) | on_delete=CASCADE, not null | Linked Django user account | One-to-one relationship |
| **Student Information** |
| student_id | CharField | max_length=20, unique=True | School student identifier | Format: STU######, unique |
| date_of_birth | DateField | not null | Student birth date | Age 13-18 required |
| **Trusted Adult Oversight** |
| trusted_adult_email | EmailField | not null | Parent/guardian email | Valid email format |
| trusted_adult_phone | CharField | max_length=20, not null | Emergency contact number | Valid phone format |
| **Financial Management** |
| balance | DecimalField | max_digits=10, decimal_places=2, default=0 | Account balance | Non-negative, max $9,999.99 |
| spending_limit | DecimalField | max_digits=10, decimal_places=2, default=50 | Per-transaction limit | $1.00-$500.00 |
| **Account Settings** |
| is_verified | BooleanField | default=False | Trusted adult verification | Verified by trusted adult |
| can_create_groups | BooleanField | default=True | Group creation permission | Boolean |
| can_join_events | BooleanField | default=True | Event participation permission | Boolean |
| **Privacy & Safety** |
| privacy_level | CharField | max_length=20, default='FRIENDS' | Profile visibility | PUBLIC/FRIENDS/PRIVATE |
| **Timestamps** |
| created_at | DateTimeField | auto_now_add=True | Profile creation time | System generated |
| updated_at | DateTimeField | auto_now=True | Last modification time | System generated |

**Business Rules:**
- Profile automatically created when user registers
- All financial operations require is_verified = True
- Trusted adult can modify balance and spending limits
- Privacy controls limit group/event visibility

### 1.6 SSA Project - class Users (Django Built-in User)

| Field Name | Data Type | Size/Constraints | Description | Validation Rules |
|------------|-----------|------------------|-------------|------------------|
| **Primary Key** |
| id | Integer | Auto-increment | Unique user identifier | System generated |
| **Authentication** |
| username | CharField | max_length=150, unique=True | Login username | 3-150 chars, alphanumeric+_.-@ |
| password | CharField | max_length=128 | Hashed password | Django password validation |
| email | EmailField | max_length=254, unique=True | User email address | Valid email format, unique |
| **Personal Information** |
| first_name | CharField | max_length=150, blank=True | User's first name | Optional, max 150 chars |
| last_name | CharField | max_length=150, blank=True | User's last name | Optional, max 150 chars |
| **Status Flags** |
| is_active | BooleanField | default=True | Account active status | Boolean |
| is_staff | BooleanField | default=False | Staff access flag | Boolean |
| is_superuser | BooleanField | default=False | Admin access flag | Boolean |
| **Timestamps** |
| date_joined | DateTimeField | auto_now_add=True | Account creation date | System generated |
| last_login | DateTimeField | null=True, blank=True | Last successful login | Updated on login |

**Business Rules:**
- Username must be unique across system
- Email must be unique and verified
- Only active users can login
- Password must meet security requirements

---

## 2. Class Diagrams

### 2.1 Complete System Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           ChipIn Platform Data Schema                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌──────────────────┐    1:1     ┌──────────────────┐                               │
│  │      User        │◄──────────►│     Profile      │                               │
│  │                  │            │                  │                               │
│  │ + id: Integer    │            │ + id: Integer    │                               │
│  │ + username: Str  │            │ + student_id: Str│                               │
│  │ + email: Email   │            │ + balance: Decimal│                               │
│  │ + password: Str  │            │ + spending_limit  │                               │
│  │ + first_name     │            │ + is_verified     │                               │
│  │ + last_name      │            │ + trusted_adult_* │                               │
│  │ + is_active      │            │ + privacy_level   │                               │
│  │ + date_joined    │            │ + created_at      │                               │
│  │ + last_login     │            │                  │                               │
│  └──────────────────┘            └──────────────────┘                               │
│           │                               │                                         │
│           │ 1:M                          │                                         │
│           ▼                              │                                         │
│  ┌──────────────────┐            ┌─────────────┐                                   │
│  │     Group        │            │GroupMember  │                                   │
│  │                  │            │ship         │                                   │
│  │ + id: Integer    │◄──────────►│(Through)    │                                   │
│  │ + name: String   │     M:M    │+ role       │                                   │
│  │ + description    │            │+ joined_at  │                                   │
│  │ + creator: FK    │            │+ is_active  │                                   │
│  │ + is_public      │            │+ permissions│                                   │
│  │ + max_members    │            └─────────────┘                                   │
│  │ + is_active      │                    ▲                                         │
│  │ + created_at     │                    │                                         │
│  └──────────────────┘                    │ M:M                                     │
│           │                              │                                         │
│           │ 1:M                          ▼                                         │
│           ▼                    ┌──────────────────┐                                │
│  ┌──────────────────┐          │      User        │                                │
│  │GroupJoinRequest  │          │                  │                                │
│  │                  │          └──────────────────┘                                │
│  │ + id: Integer    │                    │                                         │
│  │ + user: FK       │                    │ 1:M                                     │
│  │ + group: FK      │                    ▼                                         │
│  │ + message: Text  │          ┌──────────────────┐                                │
│  │ + status: Enum   │          │     Event        │                                │
│  │ + reviewed_by    │          │                  │                                │
│  │ + review_message │          │ + id: Integer    │                                │
│  │ + created_at     │          │ + title: String  │                                │
│  └──────────────────┘          │ + description    │                                │
│           │                    │ + group: FK      │                                │
│           │ 1:M                │ + creator: FK    │                                │
│           ▼                    │ + start_datetime │                                │
│  ┌──────────────────┐          │ + end_datetime   │                                │
│  │     Comment      │          │ + location       │                                │
│  │                  │          │ + total_cost     │                                │
│  │ + id: Integer    │          │ + cost_per_person│                                │
│  │ + content: Text  │          │ + max_participants│                               │
│  │ + author: FK     │          │ + status: Enum   │                                │
│  │ + group: FK?     │          │ + created_at     │                                │
│  │ + event: FK?     │◄────────►└──────────────────┘                                │
│  │ + parent: FK     │    1:M            │                                         │
│  │ + is_edited      │                   │ M:M                                     │
│  │ + is_deleted     │                   ▼                                         │
│  │ + is_flagged     │         ┌──────────────────┐                                │
│  │ + created_at     │         │EventParticipation│                                │
│  └──────────────────┘         │(Through)         │                                │
│                               │+ joined_at       │                                │
│                               │+ payment_status  │                                │
│                               │+ amount_paid     │                                │
│                               │+ custom_amount   │                                │
│                               │+ attendance_status│                               │
│                               └──────────────────┘                                │
│                                        ▲                                         │
│                                        │ M:M                                     │
│                                        ▼                                         │
│                               ┌──────────────────┐                                │
│                               │      User        │                                │
│                               │                  │                                │
│                               └──────────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Relationship Mapping

#### 2.2.1 Core Relationships

**User ↔ Profile (1:1)**
- Each User has exactly one Profile
- Profile contains ChipIn-specific student data
- Cascade delete: deleting User deletes Profile

**User ↔ Group (M:M through GroupMembership)**
- Users can be members of multiple Groups
- Groups have multiple Users as members
- GroupMembership tracks role, permissions, join date

**Group ↔ GroupJoinRequest (1:M)**
- Groups can have multiple pending join requests
- Each request belongs to one Group
- Tracks approval workflow

**Group ↔ Event (1:M)**
- Groups can organize multiple Events
- Each Event belongs to one Group
- Group deletion affects Events

**User ↔ Event (M:M through EventParticipation)**
- Users can participate in multiple Events
- Events have multiple User participants
- EventParticipation tracks payment and attendance

**Comment Polymorphic Relationships**
- Comments can belong to Groups OR Events (not both)
- Self-referential for threaded discussions
- Tracks content, moderation status

#### 2.2.2 Financial Security Relationships

**Profile Financial Controls:**
- `balance`: Current available funds
- `spending_limit`: Maximum per-transaction amount
- `trusted_adult_*`: Parent/guardian oversight
- `is_verified`: Required for financial operations

**Event Financial Flow:**
- `total_cost`: Event total expense
- `cost_per_person`: Auto-calculated split
- EventParticipation tracks individual payments
- Payment validation against Profile limits

### 2.3 Data Integrity Constraints

#### 2.3.1 Database Constraints

```sql
-- User Profile Constraints
ALTER TABLE chipin_profile ADD CONSTRAINT balance_non_negative 
CHECK (balance >= 0);

ALTER TABLE chipin_profile ADD CONSTRAINT spending_limit_positive 
CHECK (spending_limit > 0);

-- Event Constraints  
ALTER TABLE chipin_event ADD CONSTRAINT end_after_start 
CHECK (end_datetime > start_datetime);

ALTER TABLE chipin_event ADD CONSTRAINT positive_cost 
CHECK (total_cost > 0);

ALTER TABLE chipin_event ADD CONSTRAINT valid_participant_range 
CHECK (min_participants <= max_participants AND min_participants >= 2);

-- Comment Constraints
ALTER TABLE chipin_comment ADD CONSTRAINT comment_target_check 
CHECK ((group_id IS NULL) != (event_id IS NULL));

-- GroupJoinRequest Unique Constraint
ALTER TABLE chipin_groupjoinrequest ADD CONSTRAINT unique_pending_request 
UNIQUE (user_id, group_id, status) WHERE status = 'PENDING';
```

#### 2.3.2 Business Logic Constraints

**User Registration:**
- Age validation (13-18 years)
- Trusted adult email verification
- Unique student ID generation

**Group Management:**
- Creator automatically becomes admin
- Maximum member limits enforced
- Public/private visibility controls

**Event Financial Rules:**
- Cost per person ≤ user spending limit
- User balance ≥ required payment
- Trusted adult approval for large amounts

**Security Controls:**
- All financial operations require verified account
- Comment moderation for inappropriate content
- Activity logging for audit trails

---

## 3. Schema Validation Summary

### 3.1 Completeness Check

✅ **All Required Models Documented:**
- ChipIn App - class Group ✓
- ChipIn App - class GroupJoinRequest ✓  
- ChipIn App - class Comment ✓
- ChipIn App - class Event ✓
- Users App - class Profile ✓
- SSA Project - class Users ✓

✅ **All Relationship Types Defined:**
- One-to-One: User ↔ Profile
- One-to-Many: Group ↔ Event, Group ↔ Comment
- Many-to-Many: User ↔ Group, User ↔ Event
- Self-Referential: Comment ↔ Comment (threading)
- Polymorphic: Comment → Group/Event

✅ **Data Dictionary Comprehensive:**
- Field names, types, constraints
- Business rules and validation
- Relationship definitions
- Security considerations

### 3.2 Security & Safety Features

**Financial Protection:**
- Trusted adult oversight for all monetary operations
- Spending limits based on age and verification
- Transaction logging and audit trails
- Balance validation before payments

**Privacy Controls:**
- User profile visibility settings
- Group public/private status
- Comment moderation system
- Content filtering and flagging

**Data Integrity:**
- Referential integrity through foreign keys
- Check constraints for business rules
- Unique constraints for critical fields
- Cascade/restrict policies for deletions

This data engineering specification provides a robust foundation for the ChipIn platform, ensuring both functionality and security for the student-focused collaborative environment while maintaining proper data relationships and integrity constraints.