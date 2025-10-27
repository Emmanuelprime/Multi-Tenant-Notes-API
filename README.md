# 📝 Multi-Tenant Notes API with Role-Based Access Control

A **FastAPI-based** multi-tenant notes application with **JWT authentication** and **role-based access control**.
This API allows multiple organizations to manage their users and notes independently with strict tenant isolation.

---

## 🚀 Features

* **Multi-Tenant Architecture:** Complete isolation between organizations
* **JWT Authentication:** Secure token-based authentication
* **Role-Based Access Control:** Three user roles with different permissions
* **Async MongoDB:** High-performance async database operations
* **Comprehensive Testing:** Full test coverage with pytest
* **Docker Support:** Easy deployment with Docker and Docker Compose
* **RESTful API:** Clean, well-documented REST endpoints
* **Automatic Admin Creation:** Organization creators automatically become admins

---

## 🛠️ Tech Stack

| Component            | Technology                      |
| -------------------- | ------------------------------- |
| **Framework**        | FastAPI                         |
| **Database**         | MongoDB with Motor async driver |
| **ODM**              | Beanie (MongoDB ODM)            |
| **Authentication**   | JWT tokens                      |
| **Password Hashing** | Bcrypt                          |
| **Testing**          | Pytest (async support)          |
| **Containerization** | Docker & Docker Compose         |

---

## 📋 Prerequisites

* Python **3.8+**
* MongoDB **4.4+**
* *(Optional)* Docker & Docker Compose

---

## ⚡ Quick Start

#### 1. Clone the repository

```bash
git clone https://github.com/Emmanuelprime/Multi-Tenant-Notes-API.git
cd notes-api
```

#### 2. Run with Docker Compose

```bash
docker-compose up --build
```

#### 3. Access the application

* **API:** [http://localhost:8000](http://localhost:8000)
* **Interactive Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Alternative Docs:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Alternative Docs (Scalar):** [http://localhost:8000/scalar](http://localhost:8000/scalar)

---

### 💻 Local Development

#### 1. Clone and setup

```bash
git https://github.com/Emmanuelprime/Multi-Tenant-Notes-API.git
python -m venv venv
source venv/bin/activate 
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Set environment variables

```bash
export MONGO_URL="mongodb://localhost:27017"
export MONGO_DB="notes_api"
export JWT_SECRET="************************"
```

#### 4. Start MongoDB

```bash
# Using Docker
docker run -d -p 27017:27017 --name mongo mongo:7.0

```

#### 5. Run the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔑 API Usage

### 1. 🏢 Create Organization

When you create an organization, you automatically become the **admin user**.

```bash
curl -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "description": "A sample organization",
    "admin_email": "admin@acme.com",
    "admin_password": "admin123",
    "admin_name": "John Admin"
  }'
```

**Response:**

```json
{
  "id": "org_id_here",
  "name": "Acme Corp",
  "description": "A sample organization",
  "admin_user": {
    "id": "user_id_here",
    "email": "admin@acme.com",
    "name": "John Admin",
    "role": "admin"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

💡 *Save the `id` from the response — this is your **organization ID**.*

---

### 2. 🔐 Login

Authenticate a user within a specific organization.

```bash
curl -X POST "http://localhost:8000/auth/login/ORG_ID_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@acme.com",
    "password": "admin123"
  }'
```

**Response:**

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": "user_id_here",
    "email": "admin@acme.com",
    "name": "John Admin",
    "role": "admin",
    "organization_id": "org_id_here",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

💡 *Save the `access_token` for authenticated requests.*

---

### 3. 👥 Create Users (Admin Only)

Admins can create new users within their organization.

```bash
curl -X POST "http://localhost:8000/organizations/ORG_ID_HERE/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -d '{
    "email": "writer@acme.com",
    "password": "writer123",
    "name": "Jane Writer",
    "role": "writer"
  }'
```

---

### 4. 🗒️ Manage Notes

#### ➕ Create a Note (Writer/Admin)

```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -d '{
    "title": "My First Note",
    "content": "This is the content of my note"
  }'
```

#### 📄 List All Notes (All Roles)

```bash
curl -X GET "http://localhost:8000/notes/" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

#### 🔍 Get Specific Note (All Roles)

```bash
curl -X GET "http://localhost:8000/notes/NOTE_ID_HERE" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

#### ✏️ Update Note

*(Writers can update their own notes, Admins can update any.)*

```bash
curl -X PUT "http://localhost:8000/notes/NOTE_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content"
  }'
```

#### 🗑️ Delete Note (Admin Only)

```bash
curl -X DELETE "http://localhost:8000/notes/NOTE_ID_HERE" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```


### 5. 👥 User Management (Admin Only)

#### 📋 List All Users in Organization

```bash
curl -X GET "http://localhost:8000/organizations/ORG_ID_HERE/users/" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

#### ✏️ Update User Role

```bash
curl -X PUT "http://localhost:8000/organizations/ORG_ID_HERE/users/USER_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -d '{"role": "admin"}'
```

#### 🗑️ Delete User

```bash
curl -X DELETE "http://localhost:8000/organizations/ORG_ID_HERE/users/USER_ID_HERE" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

---

## 👥 User Roles & Permissions

| **Permission**       | **Reader** | **Writer** | **Admin** |
| -------------------- | ---------- | ---------- | --------- |
| View notes           | ✅          | ✅          | ✅         |
| Create notes         | ❌          | ✅          | ✅         |
| Update own notes     | ❌          | ✅          | ✅         |
| Update others' notes | ❌          | ❌          | ✅         |
| Delete notes         | ❌          | ❌          | ✅         |
| List users           | ❌          | ❌          | ✅         |
| Create users         | ❌          | ❌          | ✅         |
| Update user roles    | ❌          | ❌          | ✅         |
| Delete users         | ❌          | ❌          | ✅         |

---

## 🗄️ Database Models

### 🏢 Organization

* **id:** Unique identifier
* **name:** Organization name
* **description:** Organization description
* **created_at**, **updated_at:** Timestamps

### 👤 User

* **id:** Unique identifier
* **email:** User email (unique within organization)
* **password:** Hashed password
* **name:** User’s full name
* **role:** One of `"reader"`, `"writer"`, `"admin"`
* **organization_id:** Reference to organization
* **is_active:** Account status
* **created_at**, **updated_at:** Timestamps

### 🗒️ Note

* **id:** Unique identifier
* **title:** Note title
* **content:** Note content
* **organization_id:** Reference to organization
* **created_by:** Reference to user who created the note
* **created_at**, **updated_at:** Timestamps


## 🧪 Testing

### ▶️ Run All Tests

```bash
pytest
```

### 📊 Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### 🎯 Run Specific Test Categories

#### 🔐 Authentication Tests

```bash
pytest tests/test_auth.py -v
```

#### 🏢 Organization Tests

```bash
pytest tests/test_organizations.py -v
```

#### 👥 User Management Tests

```bash
pytest tests/test_users.py -v
```

#### 🗒️ Notes Tests

```bash
pytest tests/test_notes.py -v
```

#### 🧩 Permission Tests

```bash
pytest tests/test_permissions.py -v
```
