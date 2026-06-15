# 🛍️ AHM Store - Integrated E-Commerce & RESTful API Platform

Welcome to **AHM Store**, a robust, scalable, and secure E-Commerce platform built with **Django** and **Django REST Framework (DRF)**. This project implements a hybrid architecture: a modern monolithic web application alongside a fully-featured REST API secured with **JWT Authentication**, role-based permissions, and automated **OpenAPI 3 documentation**.

---

## ✨ Key Features

### 💻 Hybrid Architecture
* **Monolithic Web App:** Complete user journey from browsing to checkout using Django Templates, Bootstrap 5, and vanilla JavaScript. Includes built-in template pagination.
* **RESTful API Engine:** Secure, decoupled API endpoints for product management, filtering, and user authentication.

### 👤 Advanced User Management & RBAC (Role-Based Access Control)
* Fully functional Custom User management (`api_register`, `api_login`, `api_logout`, `api_refresh_token`).
* Strict **RBAC System** embedded directly into the system with 3 distinct user roles:
  * 👑 **Admin:** Full access to management dashboards and logs.
  * 🏢 **Company:** Authorized to add, modify, and manage product catalogs.
  * 🛒 **Customer:** Can browse, filter, manage carts, and place orders.

### 🔐 Enterprise-Grade API Security
* Handcrafted **JWT Token Customization** without complex serializers. 
* User roles are dynamically injected into both `Access` and `Refresh` token payloads manually on login and token refresh cycles for maximum performance.
* Secure token revocation via JWT Blacklisting mechanism upon logout.
* Enhanced error handling that obscures backend user existence checking to prevent User Enumeration attacks.

### 📦 Order & Cart Subsystems
* Session-based cart storage allowing smooth guest-to-user transitions.
* Advanced order tracking with dynamic toggles for detailed views and order cancellation safety windows.

### 📜 Automated API Documentation
* Powered by `drf-spectacular` compliant with **OpenAPI 3.0** specifications.
* Interactive **Swagger UI** with global **Bearer JWT Authentication (Authorize Lock Button)** allowing real-time endpoint testing directly from the browser.

---

## 🛠️ Tech Stack & Architecture

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Engine** | Django 5.x | Core Web Framework & Business Logic |
| **API Architecture** | Django REST Framework | RESTful Endpoints & Serializers |
| **Security / Auth** | SimpleJWT | JSON Web Token Generation & Blacklisting |
| **API Docs** | drf-spectacular / Swagger | Interactive OpenAPI 3 Specification Layout |
| **Database** | SQLite3 / PostgreSQL Ready | Relational DB (Production-ready abstraction) |
| **Frontend UI** | Bootstrap 5.3 & CSS3 | Responsive Design & Gold Accent Theme |

---

## 📁 API Endpoints Architecture

| Endpoint URL | HTTP Method | Allowed Roles / Permissions | Description |
| :--- | :--- | :--- | :--- |
| `/api/accounts/register/` | `POST` | `AllowAny` | Registers a new user & auto-creates a Role profile. |
| `/api/accounts/login/` | `POST` | `AllowAny` | Issues Access & Refresh tokens injected with User Roles. |
| `/api/accounts/refresh-token/` | `POST` | `AllowAny` | Validates Refresh token, extracts `user_id`, and re-issues tokens. |
| `/api/accounts/profile/` | `GET`, `PUT`, `PATCH` | `IsAuthenticated` | Retrieves or performs full/partial updates on user profiles. |
| `/api/accounts/logout/` | `POST` | `IsAuthenticated` | Blacklists the current Refresh token securely. |
| `/api/schema/` | `GET` | `AllowAny` | Generates the raw OpenAPI 3 YAML/JSON schema. |
| `/api/docs/` | `GET` | `AllowAny` | Renders the beautiful, interactive Swagger UI portal. |

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/AHMahmedAHM/store.git](https://github.com/AHMahmedAHM/store.git)
cd store
