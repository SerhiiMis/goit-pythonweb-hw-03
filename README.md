# Simple Python Web App

## 📚 Description

A simple web application built with Python's `http.server` and Jinja2 templates. It allows users to submit messages via a form, stores them in `data.json`, and displays them on a separate page.

---

## ✅ Features

- Two main HTML pages: `index.html` and `message.html`
- Static file handling: `styles.css` and `logo.png`
- Message submission form with `username` and `message` fields
- Data storage in `storage/data.json` with timestamp keys
- View all messages on `/read` page using Jinja2 templating
- Custom 404 error page

---

## 🛠 Project structure

```
├── app/
│   ├── handler.py
│   ├── server.py
│   └── storage.py
├── templates/
│   └── read.html
├── storage/
│   └── data.json
├── index.html
├── message.html
├── error.html
├── styles.css
├── Dockerfile
└── run.py
```

---

## 🚀 How to run

```
python run.py
```

Visit: [http://localhost:3000](http://localhost:3000)

---

## 🐳 Docker (optional)

Build and run in Docker:

```
docker build -t simple-python-webapp .
docker run -d -p 3000:3000 -v $(pwd)/storage:/app/storage simple-python-webapp
```

---

## 📄 Author

Serhii — GoIT Python Web course project.

---
