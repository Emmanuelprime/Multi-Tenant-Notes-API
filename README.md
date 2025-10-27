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
git clone <repository-url>
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

---

### 💻 Local Development

#### 1. Clone and setup

```bash
git clone <repository-url>
cd notes-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Set environment variables

```bash
export MONGO_URL="mongodb://localhost:27017"
export MONGO_DB="notes_api"
export JWT_SECRET="your-super-secret-jwt-key-change-in-production"
```

#### 4. Start MongoDB

```bash
# Using Docker
docker run -d -p 27017:27017 --name mongo mongo:7.0

# Or install MongoDB locally
# Follow instructions from: https://docs.mongodb.com/manual/installation/
```

#### 5. Run the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

🧩 **Now your API is live!**
You can access it locally or through Docker and explore the docs via FastAPI’s built-in Swagger UI or ReDoc.
