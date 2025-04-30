# 📘 Learning Tracker

A fullstack web application to help users track their learning progress, manage study sessions, set goals, and gain insights through visual dashboards.

---

## 🚀 Features

### ✅ Core Features
- User authentication (Register/Login)
- Add, edit, and delete learning skills
- Track learning sessions (logs with time, duration, notes)
- View dashboard with total hours, skills, and sessions
- Pie and bar charts using Ant Design Charts

### 🔥 Advanced Features
- Goal tracking per skill or overall
- Study reminders and in-app notifications
- Skill status (in progress / completed / dropped)
- Notes for each learning log
- Responsive UI optimized for all devices

---

## 🛠️ Tech Stack

### Frontend
- React + Redux Toolkit + React Router DOM
- Ant Design UI + Ant Design Charts
- SCSS for custom styling

### Backend
- FastAPI (Python)
- PostgreSQL
- JWT Authentication (access/refresh tokens)

---

## 🗄️ Database Schema (PostgreSQL)

### Tables:
- **users**: id, username, email, password_hash, role, created_at
- **skills**: id, user_id, title, description, status, created_at
- **study_logs**: id, user_id, skill_id, start_time, end_time, duration, note, created_at
- **goals**: id, user_id, skill_id, target_hours, current_hours, start_date, end_date, status, created_at
- **notifications**: id, user_id, message, is_read, created_at

---

## ⚙️ Getting Started

### 1. Clone project

#### Frontend
```bash
git clone https://github.com/TanNguyen234/learning_tracker.git
```

#### Backend
```bash
git clone https://github.com/TanNguyen234/Learning_Tracking_BE.git
```

### 2. Frontend Setup
```bash
cd learning_tracker
npm install
npm run dev
```

### 3. Backend Setup (FastAPI)
```bash
cd Learning_Tracking_BE
pip install -r requirements.txt
uvicorn main:app --reload
```

### 4. Environment Variables
- `DATABASE_URL`: your PostgreSQL URI
- `JWT_SECRET`: secret key for JWT

---

## 📊 Demo Screenshot
_Include here a dashboard screenshot, mobile responsive image, or login/register UI._

---

## ✍️ Author
- **Nguyễn Thành Duy Tân**  
- GitHub: [TanNguyen234](https://github.com/TanNguyen234)  
- Email: tanntd.2005@gmail.com

---

## 📄 License
This project is licensed under the MIT License.

