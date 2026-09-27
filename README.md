# 📚 StudyFlow AI

> **AI-powered study planner that helps students organize subjects, manage tasks, build personalized study plans, and track academic progress.**

StudyFlow AI is a web-based productivity platform designed to make academic planning simpler and more personalized. Students can organize their subjects and topics, manage deadlines and tasks, generate AI-assisted study plans, and monitor their progress from a centralized dashboard.

---

## ✨ Features

### 🤖 AI Study Planner

* Generate personalized study plans using the Gemini API.
* Plan study sessions based on subjects, topics, deadlines, available study time, and priorities.
* Save generated plans for later reference.
* Includes a fallback planning system when the AI service is unavailable.

### 📊 Interactive Dashboard

* View an overview of your academic workload.
* Track subjects, tasks, deadlines, and completed work.
* Monitor study progress through visual statistics.
* Quick access to important study-planning features.

### 📚 Subject & Topic Management

* Create and manage subjects.
* Add individual topics under each subject.
* Organize academic content in a structured way.

### ✅ Task Management

* Create tasks with deadlines and priorities.
* Mark tasks as completed.
* Track pending and completed work.

### 📅 Study Planning

* Organize study activities around academic deadlines.
* Break larger academic goals into manageable tasks and study sessions.

### ⏱️ Productivity Tools

* Built-in Pomodoro-style study timer.
* Progress tracking to encourage consistent study habits.

### 👤 User Accounts

* Secure user registration and login using Django authentication.
* User-specific subjects, topics, tasks, and study plans.
* Personalized dashboard for each student.

### 📱 Responsive Design

* Student-focused interface.
* Responsive layouts for desktop, tablet, and mobile screens.
* Clean and intuitive navigation.

---

## 🛠️ Tech Stack

| Technology      | Purpose                       |
| --------------- | ----------------------------- |
| 🐍 Python       | Backend programming           |
| 🌐 Django       | Web framework                 |
| 🗃️ SQLite      | Database                      |
| 🤖 Gemini API   | AI-powered study planning     |
| 🎨 HTML5        | Page structure                |
| 🎨 CSS3         | Styling and responsive design |
| ⚡ JavaScript    | Frontend interactions         |
| 📊 Chart.js     | Data visualization            |
| 🔤 Font Awesome | Icons                         |

---

## 🏗️ Project Structure

```text
StudyFlow/
│
├── planner/
│   ├── migrations/
│   ├── templates/
│   │   └── planner/
│   ├── static/
│   │   └── planner/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── studyflow/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mahathideshapathi-cpu/StudyFlow.git
```

### 2. Open the project

```bash
cd StudyFlow
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Gemini API Configuration

StudyFlow AI uses the Gemini API for AI-powered study-plan generation.

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_django_secret_key_here
```

You can use `.env.example` as a template.

> **Security:** Never commit your `.env` file or expose your Gemini API key publicly.

---

## 🗄️ Database Setup

Run Django migrations:

```bash
python manage.py migrate
```

Optional: create a Django admin account:

```bash
python manage.py createsuperuser
```

---

## ▶️ Run the Application

Start the Django development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 🤖 How the AI Planner Works

The AI planning workflow is designed around the student's academic requirements:

```text
Student Input
     │
     ▼
Subjects + Topics + Deadlines
     │
     ▼
Available Study Time
     │
     ▼
AI Study Planner
     │
     ▼
Personalized Study Plan
     │
     ▼
Saved Plan + Progress Tracking
```

The planner uses the Gemini API to generate study recommendations based on the information provided by the student.

A local fallback planner is also included so that the application can continue providing basic planning functionality when the AI service is unavailable.

---

## 🎯 Main Modules

### 1. Authentication

* Signup
* Login
* Logout
* User-specific data

### 2. Dashboard

* Academic overview
* Task progress
* Subject statistics
* Quick actions

### 3. Subjects

* Add subjects
* View subjects
* Manage academic topics

### 4. Tasks

* Create tasks
* Set deadlines
* Set priorities
* Mark tasks complete

### 5. AI Planner

* Enter study requirements
* Generate personalized plans
* Save plans
* View previously generated plans

### 6. Progress Tracking

* Monitor completed tasks
* View study statistics
* Track academic workload

### 7. Productivity

* Pomodoro-style timer
* Structured study sessions
* Focus-oriented workflow

---

## 🔐 Security

The project follows basic security practices for local development:

* API keys are stored using environment variables.
* `.env` is excluded from Git tracking.
* Virtual environments are excluded from Git tracking.
* Python cache files are excluded.
* SQLite database files are excluded from Git tracking.

For production deployment, additional security configuration should be applied, including:

* `DEBUG=False`
* Secure production `SECRET_KEY`
* Production `ALLOWED_HOSTS`
* HTTPS
* Secure cookies
* Production database configuration
* Proper secret management

---

## 🚀 Future Enhancements

Planned improvements include:

* 📈 Advanced study analytics
* 📆 Calendar-based scheduling
* 🔔 Deadline reminders
* 📱 Progressive Web App support
* 🎯 Goal tracking
* 🧠 Smarter adaptive study plans
* 📊 More detailed progress visualizations
* ☁️ Cloud database integration
* 🌐 Production deployment
* 🔄 Automatic plan adjustment based on completed tasks

---

## 💡 Why StudyFlow AI?

Students often manage academic schedules across notebooks, calendars, reminders, and different productivity apps.

**StudyFlow AI brings these workflows together in one platform.**

Instead of simply listing tasks, the application focuses on helping students turn their academic requirements into an organized and actionable study plan.

---

## 📸 Screenshots

Screenshots of the application will be added here.

### Landing Page

*Add screenshot here*

### Dashboard

*Add screenshot here*

### AI Planner

*Add screenshot here*

### Task Management

*Add screenshot here*

---

## 👩‍💻 Author

**Mahathi Deshapathi**

B.Tech — Computer Science / Artificial Intelligence & Machine Learning

Interested in:

* Artificial Intelligence
* Machine Learning
* Web Development
* Software Engineering

---

## 📄 License

This project is currently intended for educational and portfolio purposes.

---

⭐ If you found this project interesting, feel free to explore the code and follow the project as it develops.
