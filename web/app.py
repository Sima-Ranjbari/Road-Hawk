import os
import base64
import json
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, g
from werkzeug.utils import secure_filename
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'reports.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key-change-in-production')

for d in (UPLOAD_FOLDER, os.path.join(BASE_DIR, 'static'), os.path.join(BASE_DIR, 'templates')):
    os.makedirs(d, exist_ok=True)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        area TEXT NOT NULL,
        city TEXT,
        address TEXT,
        crack_type TEXT,
        repair_level TEXT,
        created_at TEXT
    )
    ''')
    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


MICHIGAN_CITIES = [
    'Detroit', 'Grand Rapids', 'Warren', 'Sterling Heights', 'Lansing', 'Ann Arbor',
    'Flint', 'Kalamazoo', 'Traverse City', 'Saginaw', 'Muskegon', 'Dearborn',
    'Pontiac', 'Royal Oak', 'Battle Creek', 'Midland', 'Holland', 'Bay City'
]


def analyze_image_with_watsonx(image_bytes):
    """
    Calls WatsonX generative vision model 'llama-3-2-90b-vision-instruct'.
    
    Environment variables expected:
    - WATSONX_API_KEY: API key or Bearer token
    - WATSONX_URL: Base URL for the watsonx generative inference endpoint
    
    If these are not configured, returns a mock result for testing.
    """
    api_key = os.environ.get('WATSONX_API_KEY')
    api_url = os.environ.get('WATSONX_URL')

    # Mock result for testing when API is not configured
    def mock_result():
        n = len(image_bytes)
        types = ['longitudinal crack', 'transverse crack', 'alligator crack', 'pothole']
        severity = ['immediate', 'moderate', 'low', 'none']
        return {
            'crack_type': types[n % len(types)],
            'repair_level': severity[(n // 3) % len(severity)],
            'raw': 'Mock result - WATSONX_API_KEY and WATSONX_URL not configured'
        }

    if not api_key or not api_url:
        return mock_result()

    b64 = base64.b64encode(image_bytes).decode('utf-8')

    # Construct payload for WatsonX vision model
    payload = {
        'model': 'llama-3-2-90b-vision-instruct',
        'input': [
            {
                'role': 'user',
                'content': (
                    'Analyze this road image and identify any cracks or damage. '
                    'Classify the crack type as one of: longitudinal crack, transverse crack, alligator crack, or pothole. '
                    'Also determine the repair priority level as: immediate, moderate, low, or none. '
                    'Respond in JSON format with keys: crack_type and repair_level.'
                )
            },
            {
                'type': 'image',
                'image_base64': b64,
                'mimetype': 'image/jpeg'
            }
        ]
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        resp = requests.post(api_url.rstrip('/') + '/v1/generation', headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        # Try to extract structured response
        if isinstance(data, dict):
            for key in ('output', 'results', 'generations', 'choices'):
                if key in data:
                    content = json.dumps(data[key])
                    break
            else:
                content = json.dumps(data)

            # Try to parse JSON response
            try:
                parsed = json.loads(content)
                if isinstance(parsed, dict) and 'crack_type' in parsed and 'repair_level' in parsed:
                    return parsed
            except Exception:
                pass

        # Fallback: parse text response for keywords
        text = resp.text.lower()
        
        crack_type = 'unknown'
        for t in ['longitudinal crack', 'transverse crack', 'alligator crack', 'pothole']:
            if t in text:
                crack_type = t
                break

        repair_level = 'low'
        for r in ['immediate', 'moderate', 'low', 'none']:
            if r in text:
                repair_level = r
                break

        return {'crack_type': crack_type, 'repair_level': repair_level, 'raw': resp.text}
    
    except Exception as e:
        print(f"WatsonX API error: {e}")
        return mock_result()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        
        file = request.files['image']
        area = request.form.get('area', '').strip()
        city = request.form.get('city', '').strip()
        address = request.form.get('address', '').strip()

        if not file or file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if not area:
            flash('Please select a Michigan area')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(datetime.utcnow().strftime('%Y%m%d%H%M%S_') + file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            # Read image and analyze with WatsonX
            with open(path, 'rb') as f:
                image_bytes = f.read()

            result = analyze_image_with_watsonx(image_bytes)

            # Save to database
            db = get_db()
            db.execute(
                'INSERT INTO reports (filename, area, city, address, crack_type, repair_level, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (filename, area, city or None, address or None, result.get('crack_type'), result.get('repair_level'), datetime.utcnow().isoformat())
            )
            db.commit()

            flash('Image uploaded and analyzed successfully!')
            return render_template('upload_result.html', filename=filename, result=result, area=area)
        else:
            flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
            return redirect(request.url)

    return render_template('upload.html', cities=MICHIGAN_CITIES)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def check_admin_password(pw):
    return pw == os.environ.get('ADMIN_PASSWORD', 'adminpass')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        pw = request.form.get('password', '')
        if not check_admin_password(pw):
            flash('Invalid password')
            return redirect(url_for('admin'))
        return redirect(url_for('admin_panel'))
    return render_template('admin_login.html')


@app.route('/admin/panel')
def admin_panel():
    area = request.args.get('area')
    sort = request.args.get('sort', 'date')

    db = get_db()
    q = 'SELECT * FROM reports'
    params = []
    
    if area:
        q += ' WHERE area = ?'
        params.append(area)
    
    if sort == 'area':
        q += ' ORDER BY area, created_at DESC'
    elif sort == 'repair':
        q += ' ORDER BY CASE repair_level WHEN "immediate" THEN 1 WHEN "moderate" THEN 2 WHEN "low" THEN 3 ELSE 4 END, created_at DESC'
    else:
        q += ' ORDER BY created_at DESC'

    cur = db.execute(q, params)
    rows = cur.fetchall()
    
    return render_template('admin_panel.html', reports=rows, areas=MICHIGAN_CITIES, selected_area=area, selected_sort=sort)


@app.route('/admin/report/<int:report_id>')
def admin_report_detail(report_id):
    db = get_db()
    cur = db.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
    report = cur.fetchone()
    
    if not report:
        flash('Report not found')
        return redirect(url_for('admin_panel'))
    
    return render_template('admin_report_detail.html', report=report)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    print("Starting Road Hawk application...")
    print("Access at: http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
