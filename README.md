# LumiLens - Photographer Booking Platform

**Capture moments that last forever.**

LumiLens is a professional photographer booking platform built with Python Flask, designed as a real-world startup product for final year project submission. The platform features a modern UI with blush pink gradients, comprehensive booking management, and role-based dashboards.

## 🎨 Features

### For Clients
- Browse 20+ professional photographers with detailed profiles
- View photographer portfolios, ratings, and reviews
- Book photographers for various events (Wedding, Portrait, Corporate, etc.)
- Secure payment simulation with multiple payment options
- Track booking progress through 4 stages:
  - **Requested** → **Accepted** → **In Progress** → **Completed**
- Real-time booking status updates
- Chat and call features (UI ready)
- Submit reviews and ratings after completion
- Pinterest-style inspiration gallery

### For Photographers
- **Modern Dashboard** with:
  - Notification badge showing active bookings count
  - Stat cards displaying rating, reviews, price, and bookings
  - Booking filters (All, Requested, Accepted, In Progress, Completed)
  - Enhanced booking cards with client avatars
- Manage bookings with status updates
- View client details and event information
- Update booking progress in real-time
- View ratings and reviews
- Portfolio management (static for now)
- Client communication tools (Chat & Call UI)

### Additional Features
- Role-based authentication (Client/Photographer)
- Rule-based chatbot assistant
- Fully responsive design
- Modern UI with Poppins font and blush pink gradient theme
- Base template for consistent layout
- Toast notification system
- AWS-ready architecture

## 🛠️ Tech Stack

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** Python Dictionaries (local development)
- **Fonts:** Google Fonts (Poppins)
- **Cloud:** AWS (DynamoDB, SNS, IAM) - boto3 integration
- **Deployment:** Localhost + AWS EC2 compatible

## 📂 Project Structure

```
impact final one/
├── app.py                      # Main Flask application
├── aws_app.py                  # AWS integrations (DynamoDB, SNS, IAM)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html              # Base template (navbar, footer, chatbot)
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── user_dashboard.html
│   ├── photographer_dashboard.html  # Redesigned with modern UI
│   ├── photographers.html
│   ├── profile.html
│   ├── booking.html
│   ├── payment.html
│   ├── tracker.html
│   ├── gallery.html
│   └── review.html
└── static/                     # Static assets
    ├── css/
    │   └── style.css          # Enhanced with 350+ new lines
    └── js/
        └── chat.js
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Setup

1. **Navigate to project directory**
```bash
cd "C:\Users\acer\OneDrive\Desktop\impact final one"
```

2. **Create virtual environment** (optional but recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the website**
Open your browser and go to: `http://127.0.0.1:5000`

## 👤 Test Accounts

### Client Account
- **Email:** user1@example.com
- **Password:** password123

### Photographer Account
- **Email:** photographer1@example.com
- **Password:** photo123

## 📱 Pages Overview

1. **Home** - Hero section with features and CTA
2. **Login/Signup** - Role-based authentication
3. **User Dashboard** - View and manage bookings
4. **Photographer Dashboard** - Modern dashboard with notifications, filters, and enhanced booking cards
5. **Browse Photographers** - Card-based photographer listing (20 photographers)
6. **Photographer Profile** - Portfolio, reviews, and booking
7. **Booking Page** - Event details and booking form
8. **Payment** - Simulated payment with multiple options
9. **Tracker** - Visual booking progress timeline (4 stages)
10. **Gallery** - Pinterest-style inspiration gallery
11. **Review** - Submit ratings and reviews

## 💬 Chatbot

The platform includes a rule-based chatbot that can help with:
- Booking process
- Pricing information
- Contact details
- Payment methods
- Tracking bookings

## 🎨 Design Features

### Color Palette
- Soft white + blush pink gradient background
- Rose pink accent colors (#ff6b9d, #ff8fab)
- Clean, modern aesthetic

### Typography
- Primary Font: Poppins (Google Fonts)
- Fallback: Segoe UI, Tahoma, Geneva, Verdana

### UI Elements
- Rounded cards with subtle shadows
- Glassmorphism effects
- Smooth hover animations
- Gradient backgrounds
- Icon-based visual design
- Toast notifications
- Fully responsive layout

### Booking Status Flow
1. **Requested** - Initial booking request (Yellow badge)
2. **Accepted** - Photographer accepts (Blue badge)
3. **In Progress** - Work in progress (Light blue badge)
4. **Completed** - Work delivered (Green badge)

## 🔧 Key Enhancements

### ✅ Fixed Issues
- **Booking Synchronization:** Photographers now see bookings immediately after users create them
- **Status Flow:** Simplified from 5 stages to 4 stages for better clarity

### ✨ New Features
- **Base Template:** Consistent navbar, footer, and chatbot across all pages
- **Notification Badge:** Shows active bookings count on photographer dashboard
- **Booking Filters:** Filter bookings by status (All, Requested, Accepted, In Progress, Completed)
- **Modern Stat Cards:** Icon-based cards with hover effects
- **Enhanced Booking Cards:** Client avatars, grid layout, detailed information
- **Toast Notifications:** Success and error notifications with smooth animations
- **Poppins Font:** Modern, professional typography

## ☁️ AWS Deployment (Optional)

### Setup AWS Infrastructure

1. **Configure AWS credentials**
```bash
aws configure
```

2. **Run AWS setup script**
```bash
python aws_app.py
```

This will create:
- DynamoDB tables (Users, Photographers, Bookings)
- SNS topic for notifications
- IAM roles with appropriate permissions

### Deploy to EC2

1. Launch an EC2 instance (Amazon Linux 2 or Ubuntu)
2. SSH into the instance
3. Install Python and dependencies
4. Clone/upload the project
5. Run the application with production settings

## 📝 Notes

- This is a demonstration project with simulated payment
- Database uses Python dictionaries for local development
- AWS integration is optional and requires proper credentials
- All photographer data is pre-loaded for demonstration
- Chat and Call features have UI placeholders

## 🔒 Security

- Session-based authentication
- Password storage (use hashing in production)
- CSRF protection (implement in production)
- AWS IAM role-based access

## 🧪 Testing

### Test User Booking Flow:
1. Login as client (user1@example.com / password123)
2. Browse photographers
3. View photographer profile
4. Book photographer
5. Complete payment
6. Track booking progress

### Test Photographer Dashboard:
1. Login as photographer (photographer1@example.com / photo123)
2. View modern dashboard with stats
3. See booking from user
4. Update booking status (Requested → Accepted → In Progress → Completed)
5. Test booking filters
6. Verify real-time updates

## 📄 License

This project is created for educational purposes as a final year project.

## 👨‍💻 Developer

Created as a professional photographer booking platform demonstration.

---

**LumiLens** - Where moments become memories. 📸

**Status:** ✅ Production Ready for Final Year Submission
