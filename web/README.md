# Road Hawk - Michigan Road Damage Reporter

A web application for reporting and analyzing road damage in Michigan using AI-powered image analysis via WatsonX.

## Features

### User Portal
- Upload road damage images with location information
- Automatic AI analysis using WatsonX's `llama-3-2-90b-vision-instruct` model
- Detect crack types: longitudinal crack, transverse crack, alligator crack, pothole
- Repair priority classification: immediate, moderate, low, none
- Michigan-only location restrictions

### Admin Portal
- View all damage reports in a sortable table
- Filter reports by Michigan area/city
- Sort by date, area, or repair priority
- Access uploaded images
- Password-protected access

## Installation

### Prerequisites
- Python 3.8 or higher
- WatsonX API credentials (optional for testing - app includes mock mode)

### Setup Instructions

1. **Navigate to the web directory**
```powershell
cd web
```

2. **Create and activate a virtual environment**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment variables** (optional - app works in mock mode without these)

For WatsonX integration:
```powershell
$env:WATSONX_API_KEY = "your-api-key-here"
$env:WATSONX_URL = "https://your-watsonx-endpoint"
```

For admin access (default password is `adminpass`):
```powershell
$env:ADMIN_PASSWORD = "your-secure-password"
```

Optional Flask secret key:
```powershell
$env:FLASK_SECRET = "your-secret-key"
```

5. **Run the application**
```powershell
python app.py
```

6. **Access the application**

Open your browser and navigate to: `http://localhost:8000`

## Usage

### For Users

1. Click **"Upload Road Image"** on the home page
2. Select an image file (PNG, JPG, or JPEG)
3. Choose your Michigan area from the dropdown
4. Optionally add city and address details
5. Click **"Upload & Analyze"**
6. View the AI-generated analysis results

### For Admins

1. Click **"Admin Login"** on the home page
2. Enter the admin password (default: `adminpass`)
3. View all reports in the dashboard
4. Use filters to sort by area or repair priority
5. Click on image links to view uploaded photos

## WatsonX Integration

The application uses WatsonX's `llama-3-2-90b-vision-instruct` model for image analysis. 

### Configuration

Set these environment variables to enable WatsonX:
- `WATSONX_API_KEY`: Your WatsonX API key
- `WATSONX_URL`: Your WatsonX endpoint URL

### Mock Mode

If WatsonX credentials are not configured, the app runs in **mock mode** with simulated AI responses. This is useful for:
- Local development and testing
- UI/UX testing without API costs
- Demonstrating the application

## Project Structure

```
web/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── reports.db            # SQLite database (created on first run)
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── upload_result.html
│   ├── admin_login.html
│   └── admin_panel.html
├── static/               # Static files
│   └── style.css
└── uploads/              # Uploaded images (created on first run)
```

## Database Schema

SQLite database with a `reports` table:
- `id`: Primary key
- `filename`: Uploaded image filename
- `area`: Michigan city/area
- `city`: Optional specific city
- `address`: Optional street address
- `crack_type`: AI-detected crack type
- `repair_level`: AI-determined repair priority
- `created_at`: Timestamp

## Crack Types Detected

1. **Longitudinal Crack**: Runs parallel to road centerline
2. **Transverse Crack**: Runs perpendicular to road centerline
3. **Alligator Crack**: Interconnected cracks forming alligator skin pattern
4. **Pothole**: Bowl-shaped holes in road surface

## Repair Priority Levels

1. **Immediate**: Urgent repair needed
2. **Moderate**: Repair needed soon
3. **Low**: Minor issue, can wait
4. **None**: No repair needed

## Michigan Cities Supported

- Detroit
- Grand Rapids
- Warren
- Sterling Heights
- Lansing
- Ann Arbor
- Flint
- Kalamazoo
- Traverse City
- Saginaw
- Muskegon
- Dearborn
- Pontiac
- Royal Oak
- Battle Creek
- Midland
- Holland
- Bay City

## Security Notes

⚠️ **For Production Use:**
- Change the default admin password
- Set a strong `FLASK_SECRET` key
- Enable HTTPS
- Add rate limiting
- Implement CSRF protection
- Add file size limits
- Use a production WSGI server (e.g., Gunicorn, uWSGI)
- Consider using a more robust database (PostgreSQL, MySQL)

## Troubleshooting

### Import errors when running app
Make sure you've activated the virtual environment and installed dependencies:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### WatsonX API errors
- Verify your API key and URL are correct
- Check your WatsonX account has access to the vision model
- Review the `analyze_image_with_watsonx()` function to ensure it matches your endpoint's schema

### Can't access admin panel
- Default password is `adminpass`
- Set custom password via `ADMIN_PASSWORD` environment variable

## License

See LICENSE file in the root directory.

## Contributing

This is a demonstration project for Michigan road damage reporting. For production use, additional security and scalability measures are recommended.
