# Plan to Make Tests Pass

## Test Analysis

**Current failure:** `MemoryUsersRepo() takes no arguments` (tests/test_create_user.py:5)

**Test requirements** (tests/test_create_user.py:4-14):
- MemoryUsersRepo that accepts initial users list
- CreateUser command with execute(uuid, username, email, dni) method
- User entity with uuid, username, email, dni attributes
- MemoryUsersRepo.find_all() method returning list of users

## Implementation Plan

Following hexagonal architecture & TDD principles (minimal implementation only):

### 1. Domain Layer - Create User Entity
**File:** `domain/__init__.py`
- Define User class with:
  - uuid attribute
  - username attribute
  - email attribute
  - dni attribute

### 2. Infrastructure Layer - Implement MemoryUsersRepo
**File:** `infra/repos.py`
- Accept initial users list in `__init__(users)`
- Store users in internal list
- Implement `find_all()` method returning all users
- Implement method to add/save users to the list

### 3. Application Layer - Implement CreateUser Command
**File:** `app/create_user.py`
- Accept repository in `__init__(repo)`
- Implement `execute(uuid, username, email, dni)` method that:
  - Creates User entity with provided data
  - Saves user to repository

## Notes
- No extra features per project rules (red, green, refactor workflow)
- Minimal code to pass test only
