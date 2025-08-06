# Part A - System Modeling (10 marks)
## ChipIn Secure Social Media Platform

### Overview
This document presents the system modeling for the ChipIn platform - a secure social media platform for students to collaboratively share event costs with trusted adult oversight.

---

## 1. Structure Chart - Hierarchical System Organization

### System Hierarchy and Module Organization

```
ChipIn System (ssa_project)
│
├── Authentication Module (users app)
│   ├── login_view()
│   ├── register()
│   ├── logout_view()
│   └── profile_management()
│
├── Group Management Module (chipin app)
│   ├── group_detail()
│   ├── create_group()
│   ├── delete_group()
│   ├── leave_group()
│   └── Group Membership Submodule
│       ├── invite_users()
│       ├── request_to_join_group()
│       ├── vote_on_join_request()
│       ├── delete_join_request()
│       └── accept_invite()
│
├── Event Management Module (chipin app)
│   ├── create_event()
│   ├── join_event()
│   ├── leave_event()
│   ├── delete_event()
│   └── update_event_status()
│
├── Communication Module (chipin app)
│   ├── edit_comment()
│   ├── delete_comment()
│   └── add_comment()
│
├── Financial Management Module (chipin app)
│   ├── Payment Processing Submodule
│   │   ├── payment_handling()
│   │   ├── process_transaction()
│   │   └── validate_payment()
│   └── Balance Management Submodule
│       ├── balance_management()
│       ├── check_spending_limits()
│       ├── trusted_adult_oversight()
│       └── update_balance()
│
└── Security & Oversight Module
    ├── trusted_adult_verification()
    ├── spending_limit_enforcement()
    ├── transaction_monitoring()
    └── safety_controls()
```

### Module Relationships and Data Flow

**Control Flow:**
1. **Main Controller** → Authentication Module → User Verification
2. **Authenticated User** → Group Management → Create/Join Groups
3. **Group Member** → Event Management → Create/Participate in Events
4. **Event Participant** → Financial Module → Handle Payments
5. **All Modules** → Security Module → Continuous Monitoring

**Data Exchange Points:**
- User authentication data flows to all modules for authorization
- Group membership data feeds into event participation controls
- Financial data requires trusted adult approval before processing
- All transactions monitored by security module

---

## 2. Data Flow Diagram - System Data Movement

### Level 0 DFD - Context Diagram

```
External Entities:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Student   │    │Trusted Adult│    │   School    │
│    User     │    │ (Guardian)  │    │  Authority  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       │ Login/Register    │ Approve Spending  │ Monitor Usage
       │ Join Groups       │ Set Limits        │ Safety Reports
       │ Create Events     │ View Transactions │ User Oversight
       │ Make Payments     │                   │
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌─────────────┐
                    │   ChipIn    │
                    │   System    │
                    │ (ssa_project│
                    └─────────────┘
                           │
                    ┌─────────────┐
                    │  External   │
                    │  Payment    │
                    │  Gateway    │
                    └─────────────┘
```

### Level 1 DFD - Main Processes

```
Data Stores:
[D1] User_Profiles
[D2] Groups
[D3] Events  
[D4] Financial_Records
[D5] Security_Logs

Processes:

1.0 User Management
    Input: Registration Data, Login Credentials
    Output: User Profile, Authentication Token
    Data Stores: [D1] User_Profiles, [D5] Security_Logs

2.0 Group Management  
    Input: Group Creation Data, Join Requests
    Output: Group Information, Membership Status
    Data Stores: [D1] User_Profiles, [D2] Groups

3.0 Event Management
    Input: Event Details, Participation Requests
    Output: Event Information, Participant Lists
    Data Stores: [D2] Groups, [D3] Events, [D1] User_Profiles

4.0 Financial Processing
    Input: Payment Requests, Balance Updates
    Output: Transaction Records, Balance Information
    Data Stores: [D1] User_Profiles, [D3] Events, [D4] Financial_Records

5.0 Security & Oversight
    Input: All System Activities
    Output: Security Reports, Alert Notifications
    Data Stores: [D5] Security_Logs, [D4] Financial_Records
```

### Level 2 DFD - Detailed Process Breakdown

#### 2.0 Group Management Process Detail

```
2.1 Create Group
    Input: Group Name, Description, Settings
    Process: Validate creator permissions, Create group record
    Output: New group entry
    Data Store: [D2] Groups

2.2 Join Group Process
    Input: User ID, Group ID, Join Request
    Process: Check group settings, Create join request
    Output: Join request record or immediate membership
    Data Store: [D2] Groups, [D1] User_Profiles

2.3 Approve/Reject Requests
    Input: Join Request ID, Admin Decision
    Process: Validate admin permissions, Update request status
    Output: Updated membership or rejection notice
    Data Store: [D2] Groups

2.4 Manage Members
    Input: Member ID, Action (promote, remove, etc.)
    Process: Check permissions, Update member status
    Output: Updated membership records
    Data Store: [D2] Groups
```

#### 4.0 Financial Processing Detail

```
4.1 Payment Request
    Input: Event ID, User ID, Amount
    Process: Validate user balance, Check spending limits
    Output: Payment authorization or denial
    Data Store: [D1] User_Profiles, [D4] Financial_Records

4.2 Process Payment
    Input: Authorized payment data
    Process: Transfer funds, Update balances, Log transaction
    Output: Transaction record, Updated balances
    Data Store: [D4] Financial_Records, [D1] User_Profiles

4.3 Trusted Adult Oversight
    Input: Transaction data, Spending requests
    Process: Notify trusted adult, Await approval for large amounts
    Output: Approval/denial, Updated spending limits
    Data Store: [D1] User_Profiles, [D4] Financial_Records

4.4 Balance Management
    Input: Deposit requests, Withdrawal requests
    Process: Validate trusted adult authorization
    Output: Updated account balances
    Data Store: [D1] User_Profiles, [D4] Financial_Records
```

### Data Dictionary Summary

**Key Data Elements:**
- **User_Profile**: student_id, balance, spending_limit, trusted_adult_info
- **Group**: group_id, name, creator, member_list, financial_settings
- **Event**: event_id, group_id, cost_details, participant_list, payment_status
- **Transaction**: transaction_id, amount, participants, approval_status
- **Security_Log**: timestamp, user_id, action, security_level

---

## System Architecture Summary

The ChipIn system follows a **modular, security-first architecture** with:

1. **Clear separation of concerns** between authentication, group management, events, and financial processing
2. **Hierarchical control flow** ensuring proper authorization at each level
3. **Comprehensive data tracking** for all financial and social interactions
4. **Trusted adult oversight** integrated into all financial processes
5. **Security monitoring** across all system components

This structure ensures both **functionality** and **safety** for the student-focused collaborative platform while maintaining **clear data flow** and **proper access controls**.