# 📖 Timeless Tales

**Timeless Tales** is a Django-based blogging platform where users can create, publish, discover, and interact with blog posts.

## ✨ Features

* 🔐 User registration, login, and logout
* 📝 Create, edit, draft, and publish blog posts
* 🏷️ Categories and tags
* 🔍 Search blogs by title and content
* ❤️ Like posts using AJAX
* 💬 Comment on blog posts
* 👁️ Track post views and reading time
* 📊 Writer dashboard with post statistics
* 👤 User profiles and profile images
* 🖼️ Blog image uploads
* 🔥 Trending and most-viewed posts
* ⚙️ Django Admin for content management

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, Bootstrap, JavaScript
* **Database:** SQLite
* **Templates:** Django Templates
* **Storage:** Local media storage

## 📂 Project Structure

```text
Timeless_Tales/
├── blog/          # Project configuration
├── home/          # Blog application
├── templates/     # HTML templates
├── media/         # Uploaded images
├── db.sqlite3     # SQLite database
├── manage.py      # Django management script
└── README.md
```

## 🔄 How It Works

Users can browse published blogs, search for posts, and read their content.

Registered users can create and manage their own posts, upload images, add categories and tags, save drafts, publish content, like posts, and add comments.

The writer dashboard displays post statistics such as views, likes, and recent posts. Django Admin provides management of users, blogs, categories, tags, comments, and profiles.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/TanishaSharma19/Timeless_Tales.git
cd Timeless_Tales
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

### 6. Run the project

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

## 🔐 Admin Panel

Access the Django Admin panel at:

**http://127.0.0.1:8000/admin/**

## 📌 Notes

* Uses SQLite for development.
* Uploaded images are stored in `media/`.
* Keep secret keys and sensitive information out of GitHub.
* Add `__pycache__/`, `*.pyc`, `venv/`, and sensitive files to `.gitignore`.

## 🌐 Repository

[Timeless Tales on GitHub](https://github.com/TanishaSharma19/Timeless_Tales?utm_source=chatgpt.com)

## 👩‍💻 Author

**Tanisha Sharma**
