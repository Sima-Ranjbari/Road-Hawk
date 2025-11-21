# Road Hawk - Michigan Road Damage Reporter

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1+-green.svg)
![WatsonX](https://img.shields.io/badge/WatsonX-AI-orange.svg)

**Project for IBM AI Hackathon 2025 using WatsonX**

A web application for reporting and analyzing road damage in Michigan using AI-powered image analysis via IBM WatsonX.ai

## 🎯 Overview

Road Hawk is an intelligent road damage reporting system that enables Michigan residents to upload images of road damage and receive instant AI-powered analysis. The system automatically classifies crack types and determines repair priority levels, helping municipalities manage road maintenance more efficiently.

## ✨ Features

### 👤 User Portal
- **Image Upload**: Upload road damage images with location information
- **AI Analysis**: Automatic crack detection using WatsonX vision AI
- **Crack Classification**: Detects 4 types of cracks:
  - Longitudinal crack
  - Transverse crack
  - Alligator crack
  - Pothole
- **Repair Priority**: Classifies urgency levels:
  - Immediate
  - Moderate
  - Low
  - None
- **Michigan-Only**: Location restricted to Michigan cities

### 🔐 Admin Portal
- **Dashboard**: View all damage reports in sortable tables
- **Filtering**: Filter reports by Michigan area/city
- **Sorting**: Sort by date, area, or repair priority
- **Image Access**: View all uploaded road damage photos
- **Password Protection**: Secure admin access

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- WatsonX API credentials (optional - app includes mock mode for testing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SheliaRT/Road-Hawk.git
cd Road-Hawk/web
```

2. **Create virtual environment**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment (optional)**
```powershell
# For WatsonX AI integration
$env:WATSONX_API_KEY = "your-api-key"
$env:WATSONX_URL = "your-watsonx-endpoint"

# Admin password (default: adminpass)
$env:ADMIN_PASSWORD = "your-secure-password"

# Flask secret key
$env:FLASK_SECRET = "your-secret-key"
```

5. **Run the application**
```powershell
python app.py
```

6. **Access the app**
Open browser: http://localhost:8000

## 📁 Project Structure

```
Road-Hawk/
├── web/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── README.md             # Detailed web app documentation
│   ├── reports.db            # SQLite database (auto-created)
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── upload_result.html
│   │   ├── admin_login.html
│   │   └── admin_panel.html
│   ├── static/               # CSS and static files
│   │   └── style.css
│   └── uploads/              # Uploaded images (auto-created)
├── README.md                  # This file
└── LICENSE
```

## 🔧 Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite
- **AI/ML**: IBM WatsonX (`llama-3-2-90b-vision-instruct`)
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **HTTP Client**: Requests library

## 🧪 Testing

The application includes a **mock mode** for testing without WatsonX credentials:
- Simulated AI responses for development
- No API costs during testing
- Full UI/UX functionality

To test:
1. Run the app without setting WatsonX environment variables
2. Upload any image - you'll get mock analysis results
3. Test all features including admin panel

## 🎨 Screenshots

- **Home Page**: Choose between User and Admin portals
- **Upload Page**: Select image, Michigan location, and submit
- **Results Page**: View AI analysis with crack type and repair priority
- **Admin Dashboard**: Filter, sort, and manage all reports

## 🌍 Michigan Coverage

Supported Michigan cities include:
- Detroit, Grand Rapids, Warren, Sterling Heights
- Lansing, Ann Arbor, Flint, Kalamazoo
- Traverse City, Saginaw, Muskegon, Dearborn
- And more...

## 🔒 Security Notes

⚠️ **For Production Deployment:**
- Change default admin password
- Set strong `FLASK_SECRET` key
- Enable HTTPS/SSL
- Add rate limiting
- Implement CSRF protection
- Add file size/type validation
- Use production WSGI server (Gunicorn, uWSGI)
- Consider PostgreSQL/MySQL for database

## 📊 Database Schema

**reports** table:
- `id`: Primary key
- `filename`: Uploaded image filename
- `area`: Michigan city/area
- `city`: Specific city (optional)
- `address`: Street address (optional)
- `crack_type`: AI-detected crack type
- `repair_level`: Repair priority
- `created_at`: Timestamp

## 🤝 Contributing

This project was created for the IBM AI Hackathon 2025. Contributions are welcome!

## 📄 License

See LICENSE file for details.

## 👥 Authors

- **SheliaRT** - Initial work - [GitHub](https://github.com/SheliaRT)
- **Sima Ranjbari** -Initial work - [GitHub](https://github.com/Sima-Ranjbari)

## 🙏 Acknowledgments

- IBM WatsonX for AI vision capabilities
- IBM AI Hackathon 2025
- Michigan Department of Transportation for inspiration


**Built with ❤️ for Michigan roads using IBM WatsonX AI**
