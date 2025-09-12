📋 Features

User authentication (login/register) for admin users.

Admin dashboard to view total assets, building‐wise or department‐wise breakdown.

Asset registration, modification and assignment to locations or users.

Asset history / record tracking (who used asset, when, status changes).

Interface for multiple buildings / locations.

Responsive frontend (HTML + CSS) for viewing and managing assets.

Simple, lightweight backend in Python.

🧰 Tech Stack
Component	Technology
Backend	Python (Flask / plain web server)
Frontend	HTML, CSS, JavaScript (static pages)
Database	SQLite (local file database.db)
Styling / UX	Custom CSS, basic styling, static assets
Dependencies	Listed in requirements.txt
🚀 Getting Started
Prerequisites

Python 3.x installed

Pip package manager

Basic familiarity with command‐line operations

Installation & Setup

Clone the repository

git clone https://github.com/naveen2k05-2k05/Asset_Management-In-House-.git
cd Asset_Management-In-House-


Create virtual environment (optional but recommended)

python3 -m venv venv
source venv/bin/activate   # on Mac/Linux
venv\Scripts\activate      # on Windows


Install dependencies

pip install -r requirements.txt


Configure (if needed)

Ensure database.db file exists and is in correct place.

If you have config for environment variables (e.g., secret keys), set them up.

Adjust port / host in app.py if needed.

Run the application

python app.py


Then open your browser at http://localhost:5000 (or whatever port you configured).

🗂 Repository Structure
Asset_Management-In-House-/
├── admin_dashboard.html
├── admin_login.html
├── app.py
├── asset_management.html
├── asset_total.html
├── choose_building.html
├── dashboard.html
├── database.db
├── login.html
├── record_history.html
├── register.html
├── requirements.txt
├── styles.css
├── web_bg.jpg
└── README.md


app.py – Main backend application logic (routes, handling requests).

database.db – SQLite database storing asset, user, record tables.

HTML files – Frontend views for different pages (login, dashboard, asset management, etc.)

styles.css and web_bg.jpg – Static assets for styling.# Asset_Management-In-House-
