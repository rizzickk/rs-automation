from flask import Flask, Response, send_from_directory, request, redirect, url_for, flash
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
import sqlite3
import os
# import pandas as pd
# from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'emails.db')


def store_email(email):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(''' 
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute("INSERT INTO emails (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        print("✅ Email stored in SQLite")
    except Exception as e:
        print(f"❌ SQLite Error: {e}")

# def append_email_to_excel(email):
#     excel_path = os.path.join(os.path.dirname(__file__), 'emails.xlsx')
#     data = {'email': [email], 'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]}
#     df_new = pd.DataFrame(data)

#     if os.path.exists(excel_path):
#         df_existing = pd.read_excel(excel_path)
#         df_combined = pd.concat([df_existing, df_new], ignore_index=True)
#     else:
#         df_combined = df_new

    # df_combined.to_excel(excel_path, index=False)
    # print("✅ Email appended to Excel")


# SMTP config for Microsoft 365
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USER = 'info@rsautomationep.com'
SMTP_PASS = os.getenv('SMTP_PASS')

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret")


@app.route('/')
def home():
    html = ''' 
    <!DOCTYPE html>
    <html>
    <head>
        <title>RS Automation</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                color: #ffffff;
                background: linear-gradient(rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.3)),
                    url('/static/background.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }
            .contact-bar {
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                background-color: rgba(0, 0, 0, 0.75);
                color: white;
                font-size: 0.9rem;
                padding: 8px 30px;
                box-sizing: border-box;
                z-index: 999;
            }
            .main-wrapper {
                padding-top: 80px;
            }
            .container-box {
                max-width: 1000px;
                margin: 30px auto;
                background-color: rgba(0, 0, 0, 0.6);
                padding: 40px 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
                color: white;
                box-sizing: border-box;
                overflow: hidden;
                width: 90%;
            }
            .centered-section p {
                margin: 12px auto;
                text-align: justify;
                text-align-last: center;
                text-justify: inter-word;
                max-width: 600px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .header img {
                max-width: 180px;
                margin-bottom: 20px;
                border-radius: 8px;
            }
            .header h1 {
                margin: 0;
                font-size: 2.4em;
                color: #00A1DA;
            }
            .tagline {
                font-size: 1.1em;
                color: #ccc;
                margin-top: 8px;
            }
            section {
                margin-bottom: 30px;
            }
            .profile-pic {
                width: 140px;
                height: 140px;
                object-fit: cover;
                border-radius: 50%;
                border: 3px solid #00A1DA;
                margin: 20px auto 10px auto;
                display: block;
                box-shadow: 0 0 8px rgba(0,0,0,0.4);
            }
            .about-text {
                text-align: justify;
                text-align-last: center;
                max-width: 600px;
                margin: 0 auto;
                color: #ddd;
            }
            .centered-section {
                text-align: center;
                max-width: 700px;
                margin: 0 auto;
            }
            .icon-service-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 30px;
                justify-content: center;
                margin-top: 30px;
            }
            .icon-service-item {
                text-align: center;
                width: 250px;
            }
            .icon-service-item i {
                font-size: 2.5em;
                color: #00bfff;
                margin-bottom: 10px;
            }
            .icon-service-item p {
                margin: 0;
                font-size: 1rem;
                color: #fff;
                line-height: 1.4;
            }
            .service-subtext {
                font-size: 0.85rem;
                color: #ccc;
            }
            a {
                color: #00A1DA;
                text-decoration: underline;
                transition: color 0.2s ease-in-out;
            }
            a:hover {
                color: #66d5f4;
                text-decoration: underline;
            }
            h2 {
                color: #00A1DA;
                margin-bottom: 10px;
            }
            .cta {
                background-color: rgba(255, 255, 255, 0.1);
                padding: 25px;
                border-radius: 10px;
                text-align: center;
            }
            footer {
                text-align: center;
                font-size: 0.9em;
                color: #bbb;
                margin-top: 60px;
            }
            input[type="file"] {
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="contact-bar">
            <p>
                <i class="fas fa-envelope"></i> <a href="mailto:info@rsautomationep.com">info@rsautomationep.com</a> |
                <i class="fas fa-phone"></i> <a href="tel:+19154785436">(915) 478-5436</a>
            </p>
        </div>

        <div class="main-wrapper">
            <div class="container-box">
                <header class="header">
                    <img src="/static/logo.png" alt="RS Automation Logo">
                    <h1>RS Automation</h1>
                    <p class="tagline">Risk Reporting Automation</p>
                    <p><strong>We help financial institutions eliminate manual reporting, flag risks faster, and pass audits with confidence.</strong></p>
                    <a href="#how-it-works">How It Works</a> | <a href="#get-started">Request a Demo</a>
                </header>
            </div>

            <div class="container-box">
                <section class="centered-section">
                    <h2>What We Help You Achieve</h2>
                    <p>📉 <strong>Reduce manual hours</strong> spent on monthly reporting</p>
                    <p>🚨 <strong>Automatically flag exceptions</strong> & risks</p>
                    <p>📁 <strong>Prepare clean, audit-ready outputs</strong> on demand</p>
                    <p>🔐 <strong>Keep all data</strong> securely within your infrastructure</p>
                </section>
            </div>

            <div class="container-box" id="how-it-works">
                <section>
                    <h2 style="text-align: center;">How We Work With You</h2>
                    <div class="icon-service-grid">
                        <div class="icon-service-item">
                            <i class="fas fa-user-shield"></i>
                            <p><strong>Start Safe</strong><br>
                            <span class="service-subtext">You choose: redacted Excel file, secure remote session, or in-network install.</span></p>
                        </div>
                        <div class="icon-service-item">
                            <i class="fas fa-cogs"></i>
                            <p><strong>Automate</strong><br>
                            <span class="service-subtext">We convert your reporting logic into an executable, reliable process.</span></p>
                        </div>
                        <div class="icon-service-item">
                            <i class="fas fa-file-alt"></i>
                            <p><strong>Deliver Confidence</strong><br>
                            <span class="service-subtext">You get audit-ready, repeatable reports that reduce stress and increase visibility.</span></p>
                        </div>
                    </div>
                </section>
            </div>

            <div class="container-box">
                <section class="centered-section">
                    <h2>Deployment Options</h2>
                    <p>📁 <strong>Redacted Sample Upload</strong> – Send redacted files for initial assessment.</p>
                    <p>🛰️ <strong>Secure Remote Access</strong> – We work via Citrix, VPN, or remote desktop within your network.</p>
                    <p>🏢 <strong>In-Environment Setup</strong> – We install scripts directly inside your environment, no data ever leaves your infrastructure.</p>
                    <p>📄 <strong>IT Documentation Available</strong> – We provide NDAs and technical specs for InfoSec review.</p>
                </section>
            </div>
            <div class="container-box" id="get-started">
                <section class="centered-section">
                    <h2>Get Started</h2>
                    <p>Select your preferred way to engage:</p>
                    <p><a href="https://calendly.com/ramirez-ricardo55/30min" target="_blank">📅 Schedule a Strategy Call</a></p>
                    <a href="/get-pdf">📄 Download Our Overview PDF</a>
                    <p><a href="/static/rs_template.xlsx" download>📂 Download Redacted Template</a></p>
                    <p>Email us directly: <a href="mailto:info@rsautomationep.com">info@rsautomationep.com</a></p>
                </section>
            </div>



            <div class="container-box">
                <section>
                    <h3 style="color:#00A1DA; text-align: center;">Our Mission</h3>
                    <p class="about-text">To eliminate manual reporting and reduce compliance risk by delivering secure, audit-ready automation tailored for financial institutions.</p>
                    <h3 style="color:#00A1DA; text-align: center;">Our Vision</h3>
                    <p class="about-text">To become the most trusted automation partner for regulated institutions by making reporting effortless, accurate, and built for tomorrow’s audit.</p>
                </section>
            </div>

            <footer>
                © 2025 RS Automation. All rights reserved.
            </footer>
        </div>
    </body>
    </html>
    '''


    return Response(html, mimetype='text/html')

# def send_notification_email(submitted_email):
#     msg = MIMEMultipart()
#     msg['From'] = SMTP_USER
#     msg['To'] = SMTP_USER
#     msg['Subject'] = "New PDF Download Request"

#     body = f"A new user submitted their email: {submitted_email}"
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()  # Required for Office 365
#             server.login(SMTP_USER, SMTP_PASS)
#             server.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
#         print("✅ Notification email sent.")
#     except Exception as e:
#         print(f"❌ Failed to send email: {e}")


@app.route('/get-pdf', methods=['GET', 'POST'])
def get_pdf():
    if request.method == 'POST':
        app.logger.debug("Reached /get-pdf POST")
        email = request.form.get('email')
        app.logger.debug(f"Email received: {email}")
        try:
            store_email(email)
        except Exception as e:
            app.logger.error(f"Error storing email: {e}")

        thank_you_html = '''
<html>
<head>
    <meta charset="UTF-8">
    <title>Thank You</title>
    <script>
        window.open("/download", "_blank");
        setTimeout(function() { window.location.href = "/"; }, 5000);
    </script>
    <style>
        body { font-family: Inter, sans-serif; background-color: #f4f4f4; display: flex; align-items: center; justify-content: center; height: 100vh; }
        .message-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
        @media (max-width: 480px) {
            body { padding: 10px; }
            .message-box p { text-align: left !important; }
        }
    </style>
</head>
<body>
    <div class="message-box">
        <h2>Thanks for your submission!</h2>
        <p>Your download will begin in a moment...</p>
    </div>
</body>
</html>
'''
        return Response(thank_you_html, mimetype='text/html')

    # GET: display the email capture form
    form_html = '''
<html>
<head>
    <title>Download PDF</title>
    <style>
        body { font-family: Inter, sans-serif; background-color: #f4f4f4; display: flex; align-items: center; justify-content: center; height: 100vh; }
        .form-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
        input[type="email"] { padding: 10px; width: 250px; border: 1px solid #ccc; border-radius: 4px; }
        input[type="submit"] { padding: 10px 20px; margin-top: 10px; background-color: #00A1DA; border: none; color: white; cursor: pointer; border-radius: 4px; }
        @media (max-width: 480px) {
            body { padding: 10px; }
            .form-box { width: 90%; padding: 20px; }
            input { width: 100%; }
            .form-box p { text-align: left !important; }
        }
    </style>
</head>
<body>
    <div class="form-box">
        <h2>Get Your PDF Overview</h2>
        <p>Enter your email to download the RS Automation overview:</p>
        <form method="POST">
            <input type="email" name="email" placeholder="you@company.com" required><br>
            <input type="submit" value="Download PDF">
        </form>
        <p style="margin-top:20px;"><a href="/" style="color:#00A1DA;">← Back to RS Automation</a></p>
    </div>
</body>
</html>
'''
    return Response(form_html, mimetype='text/html')
@app.route('/download')
def download_pdf():
    try:
        return send_from_directory('static', 'RS_Automation_Overview.pdf', as_attachment=True)
    except Exception as e:
        return Response(f"<h3>Error: {e}</h3>", mimetype='text/html')

@app.route('/admin/download-db')
def download_db():
    db_path = os.path.dirname(__file__)
    return send_from_directory(db_path, 'emails.db', as_attachment=True)

@app.route('/admin/emails')
def view_emails():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT email, timestamp FROM emails ORDER BY timestamp DESC")
        rows = c.fetchall()
        conn.close()

        html = "<h2>Stored Emails</h2><ul>"
        for email, timestamp in rows:
            html += f"<li>{email} — {timestamp}</li>"
        html += "</ul>"
        return Response(html, mimetype='text/html')
    except Exception as e:
        return Response(f"<p>Error: {e}</p>", mimetype='text/html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
