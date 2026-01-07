# foodapp
# 🥦 Food Rescue App

A web application connecting food companies with volunteers to reduce food waste and support communities.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## 🌟 Overview

Food Rescue is a platform designed to combat food waste by connecting businesses that have surplus food with volunteers who can distribute it to those in need. The application helps reduce environmental impact while addressing food insecurity in local communities.

## ✨ Features

### For Companies
- ✅ Register and manage company profile
- ✅ Add food donations with expiry dates and quantities
- ✅ Set location for volunteers to find
- ✅ Track donation status (available, claimed, completed)
- ✅ View statistics on donations
- ✅ Delete unclaimed donations

### For Volunteers
- ✅ Browse available food donations
- ✅ View donations on interactive map
- ✅ See donations sorted by distance
- ✅ Claim donations for pickup
- ✅ Track claimed donations
- ✅ Mark donations as completed

### General Features
- 🔐 Secure authentication with password hashing
- 🗺️ Interactive Leaflet maps showing donation locations
- 📱 Responsive design for mobile and desktop
- 🎨 Clean, modern UI with Bootstrap 5
- ⚡ Real-time distance calculations
- 🔔 Flash messages for user feedback
- 📊 Statistics dashboard

## 🛠️ Tech Stack

**Backend:**
- Python 3.x
- Flask (Web framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-WTF (Forms)
- SQLite (Database)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5.3
- Bootstrap Icons
- Leaflet.js (Maps)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or download the project**
```bash
cd food-rescue-app
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables (optional)**
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
Open your browser and navigate to `http://localhost:5000`

## 🚀 Usage

### First Time Setup

1. **Register an account**
   - Choose "Company" if you're a food business/store
   - Choose "Volunteer" if you want to help distribute food

2. **For Companies:**
   - Enable location services or manually set your location
   - Add food donations with details (name, category, expiry date, quantity)
   - Monitor when volunteers claim your donations

3. **For Volunteers:**
   - Enable location services to see donations sorted by distance
   - Browse available donations on the map or list view
   - Claim donations you can pick up
   - Mark donations as completed after pickup

### User Roles

**Company Account:**
- Company name and registration number required
- Can add, view, and manage donations
- Cannot claim donations from other companies

**Volunteer Account:**
- Individual registration with name and contact
- Can browse and claim available donations
- Can view claimed donations and mark as completed

## 📁 Project Structure

```
food-rescue-app/
│
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── database/             # SQLite database directory
│   └── foodapp.db
│
├── static/               # Static files
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── scripts.js   # JavaScript utilities
│
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── about.html        # About page
    ├── register.html     # Registration form
    ├── login.html        # Login form
    ├── dashboard_company.html    # Company dashboard
    ├── dashboard_volunteer.html  # Volunteer dashboard
    ├── add_donation.html         # Add donation form
    ├── 404.html          # Not found error page
    └── 500.html          # Server error page
```

## 🔮 Future Enhancements

### High Priority
- [ ] Email notifications for claimed donations
- [ ] User profile management and settings
- [ ] Search and filter functionality
- [ ] Donation categories with icons
- [ ] Image upload for food items
- [ ] Rating system for companies and volunteers

### Medium Priority
- [ ] Chat/messaging between companies and volunteers
- [ ] Donation history and analytics
- [ ] Export data to CSV/PDF
- [ ] Mobile app (React Native/Flutter)
- [ ] Multi-language support

### Nice to Have
- [ ] Social media integration
- [ ] Automated expiry reminders
- [ ] Integration with food banks
- [ ] Gamification (badges, leaderboards)
- [ ] Carbon footprint calculator

## 🤝 Contributing

This is an educational project created for a general interest course. Contributions and suggestions are welcome!

## 📄 License

This project is created for educational purposes.

## 👥 Contact

For questions or feedback about this project, please contact the development team.

---

**Made with 💚 to reduce food waste and support communities**