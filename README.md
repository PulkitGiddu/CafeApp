# ☕ ArthCafe

A full-stack modern cafe ordering application built with **Flutter** (Mobile) and **FastAPI + PostgreSQL** (Backend). ArthCafe offers a seamless food and beverage ordering experience with real-time order tracking, address management, OTP-based authentication, and payment integration.

---

## 📱 Features

- **🔐 Mobile OTP Authentication**: Fast, passwordless login with secure token storage.
- **🍰 Interactive Menu & Categories**: Browse items with rich imagery, pricing, descriptions, and dietary indicators.
- **🛒 Dynamic Cart Management**: Add, customize quantities, and view real-time price calculations with taxes and delivery fees.
- **📍 Multi-Address Management**: Save multiple delivery addresses (Home, Work, Other) and set default addresses.
- **💳 Seamless Checkout & Payments**: Supports Razorpay and Cash on Delivery (COD) workflows.
- **🚚 Live Order Tracking & History**: Track order lifecycle states (`Placed`, `Preparing`, `Out for Delivery`, `Delivered`, `Cancelled`).
- **💬 Notifications & WhatsApp Updates**: Integration with WhatsApp notifications for order status changes.
- **🛠 Admin Management APIs**: Endpoints to manage menus, products, categories, orders, and delivery analytics.

---

## 🛠 Tech Stack

### Frontend (Mobile App)
- **Framework**: [Flutter](https://flutter.dev/) (Dart SDK `^3.10.8`)
- **State Management**: [Riverpod (`flutter_riverpod`)](https://pub.dev/packages/flutter_riverpod)
- **Navigation**: [GoRouter](https://pub.dev/packages/go_router)
- **Networking**: [Dio](https://pub.dev/packages/dio) with interceptors and auth token injection
- **Local Storage**: [flutter_secure_storage](https://pub.dev/packages/flutter_secure_storage)
- **Typography & UI**: [Google Fonts](https://pub.dev/packages/google_fonts), [Shimmer](https://pub.dev/packages/shimmer), [CachedNetworkImage](https://pub.dev/packages/cached_network_image)

### Backend (API Service)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with async driver ([asyncpg](https://github.com/MagicStack/asyncpg))
- **Data Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/) & [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Security & Auth**: JWT Tokens, PyJWT, Passlib (Bcrypt)
- **External Integrations**: Twilio / WhatsApp Cloud API, Razorpay

---

## 📂 Project Structure

```
arthcafe_app/
├── lib/                             # Flutter Application Source
│   ├── app.dart                     # App entry root & theme config
│   ├── main.dart                    # App bootstrap & ProviderScope
│   ├── core/                        # Shared app utilities & core modules
│   │   ├── constants/               # API endpoints, colors, configs
│   │   ├── network/                 # Dio client, interceptors
│   │   ├── router/                  # GoRouter configuration
│   │   ├── theme/                   # Material 3 light/dark themes
│   │   └── mock/                    # Mock data for testing
│   ├── features/                    # Feature modules
│   │   ├── address/                 # Address management & selection
│   │   ├── auth/                    # OTP authentication & sessions
│   │   ├── cart/                    # Cart provider, models & screen
│   │   ├── menu/                    # Categories, products, details
│   │   └── orders/                  # Checkout, history, live tracking
│   └── shared/                      # Reusable UI widgets
├── backend/                         # FastAPI Backend Application
│   ├── app/
│   │   ├── api/                     # REST API routes and dependencies
│   │   │   └── routes/              # auth, menu, addresses, orders, payments, admin
│   │   ├── core/                    # App configuration and security
│   │   ├── db/                      # Connection pool & database session
│   │   ├── models/                  # Database entity models
│   │   ├── repositories/            # Data access layer
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/                # Business logic & external services
│   │   └── main.py                  # FastAPI application entrypoint
│   ├── Dockerfile                   # Production Docker container definition
│   ├── render.yaml                  # Render deployment configuration
│   ├── requirements.txt             # Python backend dependencies
│   ├── schema.sql                   # PostgreSQL schema definition
│   └── seed.py                      # Database seeding script
├── android/                         # Native Android project files
├── ios/                             # Native iOS project files
├── pubspec.yaml                     # Flutter dependencies & metadata
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Flutter SDK**: `^3.10.8` ([Install Flutter](https://docs.flutter.dev/get-started/install))
- **Python**: `3.11+`
- **PostgreSQL**: `14+`
- **Android Studio / Xcode** for mobile simulators

---

### 1. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your PostgreSQL database credentials and keys:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/arthcafe
   SECRET_KEY=your-super-secret-jwt-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=43200
   ```

5. **Initialize Database Schema**:
   ```bash
   psql -U postgres -d arthcafe -f schema.sql
   ```

6. **Seed Initial Menu & Categories**:
   ```bash
   python -m seed
   ```

7. **Start the FastAPI Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   - **Interactive API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 2. Flutter App Setup

1. **Return to the root directory**:
   ```bash
   cd ..
   ```

2. **Install Flutter packages**:
   ```bash
   flutter pub get
   ```

3. **Configure API Base URL**:
   Ensure `lib/core/constants/api_constants.dart` matches your test environment:
   - **Android Emulator**: `http://10.0.2.2:8000/api/v1`
   - **iOS Simulator**: `http://localhost:8000/api/v1`
   - **Physical Device**: `http://<YOUR_LOCAL_IP>:8000/api/v1`

4. **Run the App**:
   ```bash
   flutter run
   ```

---

## 📡 API Endpoints Overview

| Module | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Auth** | `POST` | `/api/v1/auth/send-otp` | Trigger mobile OTP |
| **Auth** | `POST` | `/api/v1/auth/verify-otp` | Verify OTP & return JWT token |
| **Menu** | `GET` | `/api/v1/menu/categories` | List active categories |
| **Menu** | `GET` | `/api/v1/menu/products` | List menu products with filtering |
| **Addresses** | `GET` / `POST` | `/api/v1/addresses` | Fetch or add user delivery addresses |
| **Orders** | `POST` | `/api/v1/orders` | Create a new order |
| **Orders** | `GET` | `/api/v1/orders` | Get user order history |
| **Orders** | `GET` | `/api/v1/orders/{id}` | Get real-time status of an order |
| **Payments** | `POST` | `/api/v1/payments/verify` | Verify Razorpay transaction signature |
| **Admin** | `GET` / `POST` | `/api/v1/admin/*` | Manage items, categories & status updates |

---

## 🚢 Deployment

### Backend on Render
1. Push repository to GitHub.
2. Link repository to [Render](https://render.com/).
3. Use the provided `render.yaml` configuration for automatic blueprint deployment.
4. Set production environment variables (`DATABASE_URL`, `SECRET_KEY`, `RAZORPAY_KEY`, etc.).

---

## Demo

https://github.com/user-attachments/assets/04dae874-d848-4f39-bdb0-decddc8f83ca


---

## 📄 License

This project is licensed under the MIT License.
