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
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
            html, body {
            max-width: 100%;
            overflow-x: hidden;
            position: relative;
            overscroll-behavior-x: none;
            touch-action: pan-y;
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
            @media (max-width: 480px) {
            /* 1. Shrink contact bar */
            .contact-bar {
                font-size: 0.75rem;
                padding: 6px 15px;
                justify-content: center;
                text-align: center;
            }
            .contact-bar i,
            .contact-bar a {
                font-size: inherit;
            }

            /* 2. Set full-page background with ribbon image at top */
            body {
                background:
                url('/static/background.jpg') no-repeat top center,
                #002147;
                background-size: 100% auto, cover;
                background-repeat: no-repeat;
                background-attachment: scroll;
                overflow-x: hidden;
            }

            /* 3. Push entire page content down to reveal ribbon behind first box */
            .main-wrapper {
                padding-top: 180px; /* matches the ribbon height */
            }
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

                text-align-last: center;

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
                text-align: center;
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
            /* Banner stretches full‑width */
            #banner {
            width: 100%;
            height: auto;
            display: block;
            }

            /* Container for the content that will fade in */
            .delayed-content {
            opacity: 0;
            visibility: hidden;
            transition: opacity 1s ease-in;
            }

            /* When .visible is added, it fades in */
            .delayed-content.visible {
            opacity: 1;
            visibility: visible;
            }
            /* Start every container hidden & shifted down */
            .container-box {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 2s ease, transform 2s ease;
            }

            /* When we add .visible, it comes into place */
            .container-box.visible {
            opacity: 1;
            transform: translateY(0);
            }
            .ribbon-banner {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 160px;  /* match your ribbon height */
            background: url('/static/ribbon-mobile.png') no-repeat center top;
            background-size: cover;
            z-index: 0;
            transition: transform 0.4s ease;
            }

            /* Hidden state: slide ribbon out of view */
            .ribbon-banner.hide {
            transform: translateY(-100%);
            }
            /* Fix image block alignment */
            .deployment-img {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                margin: 40px auto;
                box-sizing: border-box;
            }

            /* Desktop styling */
            .deployment-img-inner {
                width: 90%;
                max-width: 1000px;
                border-radius: 16px;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
                transition: transform 0.3s ease;
                display: block;
            }

            /* Hover effect (optional) */
            .deployment-img-inner:hover {
                transform: translateY(-4px);
            }

            /* Mobile view override */
            @media (max-width: 480px) {
                .deployment-img-inner {
                transform: scale(1.1);
                width: 110%;
                transform-origin: center center;
            }
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
    <div id="ribbon-banner" class="ribbon-banner"></div>
        <div id="delayed-content" class="delayed-content">
        <div class="main-wrapper">
            <div class="container-box">
                <header class="header">
                    <img src="/static/logo.png" alt="RS Automation Logo">
                    <h1>Manual Excel Work Wastes Hours—and Exposes You to Risk</h1>
                    <p><strong>We streamline operations across industries—no more Excel chaos, late reports, or compliance risks.</strong></p>
                    <p style="font-size:0.9rem; color:#ccc;"><em>“Cut our reporting time by 90%.” – VP, Regional Lender</em></p>
                    <p style="font-size:0.8rem; color:#aaa;"><em>Also trusted by clinics, warehouse operators, and field teams managing complex data workflows.</em></p>
                    <div style="margin-top: 20px;">
                        <a href="#get-started" class="cta-btn">📄 Download Overview</a>
                        <a href="https://calendly.com/ramirez-ricardo55/30min" target="_blank" class="cta-btn">📅 Book Free Consult</a>
                    </div>
                </header>
            </div>

           <div class="container-box" id="how-it-works">
                <section class="icon-service-grid">
                <div class="icon-service-item">
                    <i class="fas fa-clock"></i>
                    <p><strong>Save Hours</strong><br><span class="service-subtext">No more manual Excel updates</span></p>
                </div>
                <div class="icon-service-item">
                    <i class="fas fa-bolt"></i>
                    <p><strong>Flag Exceptions</strong><br><span class="service-subtext">Automatically catch risk issues</span></p>
                </div>
                <div class="icon-service-item">
                    <i class="fas fa-shield-alt"></i>
                    <p><strong>Pass Audits</strong><br><span class="service-subtext">Clean, audit-ready outputs</span></p>
                </div>
            </section>
            </div>

 


            <section class="deployment-img">
                <img 
                    src="/static/Deployment_Options.jpg" 
                    alt="Deployment Options"
                    class="deployment-img-inner">
            </section>
            
            
            <div class="container-box" id="get-started">
                <section class="centered-section">
                    <h2>Get Started</h2>
                    <p>Select your preferred way to engage:</p>
                    <p><a href="https://calendly.com/ramirez-ricardo55/30min" target="_blank">📅 Schedule a Strategy Call</a></p>
                    <a href="/get-pdf">📄 See How Automation Fits Your Industry</a>
                    <p><a href="/static/rs_template.xlsx" download>📂 Download Redacted Template</a></p>
                    <p>Email us directly: <a href="mailto:info@rsautomationep.com">info@rsautomationep.com</a></p>
                </section>
            </div>

            <!-- Testimonial Carousel Section -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.css" />
            <script src="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.js"></script>

            <div class="container-box" style="text-align: center;">
            <h2 style="color: #00A1DA; margin-bottom: 20px;">What Our Clients Say</h2>
            <div class="swiper-container">
                <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <p style="font-size: 1.1rem; color: #eee;"><em>"RS Automation cut our reporting time by 90%. We now spend time analyzing, not formatting."</em><br>– VP of Risk, Regional Bank</p>
                </div>
                <div class="swiper-slide">
                    <p style="font-size: 1.1rem; color: #eee;"><em>"We trusted them with a redacted file, and they returned a full working solution within days."</em><br>– Director, Lending Ops</p>
                </div>
                <div class="swiper-slide">
                    <p style="font-size: 1.1rem; color: #eee;"><em>"Their automation scripts work right inside our secure environment. No compliance issues."</em><br>– Compliance Manager</p>
                </div>
                </div>
                <div class="swiper-pagination" style="margin-top: 20px;"></div>
            </div>
            </div>

            <script>
            const swiper = new Swiper('.swiper-container', {
                loop: true,
                effect: 'fade',
                fadeEffect: {
                crossFade: true
                },
                autoplay: {
                delay: 6000,
                disableOnInteraction: false,
                },
                pagination: {
                el: '.swiper-pagination',
                clickable: true,
                },
            });
            </script>


            <div class="container-box">
                <section>
                    <h3 style="color:#00A1DA; text-align: center;">Our Mission</h3>
                    <p class="about-text">To eliminate manual reporting and reduce compliance risk by delivering secure, audit-ready automation for clinics, warehouses, job sites, and financial institutions alike.</p>
                    <h3 style="color:#00A1DA; text-align: center;">Our Vision</h3>
                    <p class="about-text">TTo become the most trusted automation partner across essential industries—making reporting effortless, accurate, and future-ready for any audit or executive review.</p>
                </section>
            </div>

            <footer>
                © 2025 RS Automation. All rights reserved.
            </footer>
        </div>
        <div>
        <script>
        document.addEventListener('DOMContentLoaded', () => {
            // After 1.5s, show the wrapper…
            setTimeout(() => {
            const wrapper = document.getElementById('delayed-content');
            wrapper.classList.add('visible');

            // …then stagger each .container-box
            const boxes = wrapper.querySelectorAll('.container-box');
            boxes.forEach((el, i) => {
                setTimeout(() => {
                el.classList.add('visible');
                }, i * 1500 + 1500);  // 0.5s apart, starting half‑second in
            });
            }, 0);
        });
        </script>
        <script>
        let lastScrollTop = 0;
        const ribbon = document.getElementById('ribbon-banner');

        window.addEventListener('scroll', () => {
            const st = window.pageYOffset || document.documentElement.scrollTop;

            if (st > lastScrollTop) {
            // Scrolling down
            ribbon.classList.add('hide');
            } else {
            // Scrolling up
            ribbon.classList.remove('hide');
            }

            lastScrollTop = st <= 0 ? 0 : st;
        });
        </script>
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
  // Fetch the PDF as a blob, then trigger a download
  fetch('/download')
    .then(resp => {
      if (!resp.ok) throw new Error('Network response was not ok');
      return resp.blob();
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'RS_Automation_Overview.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch(err => console.error('Download failed:', err));
  // After 5 seconds, redirect back home
  setTimeout(() => window.location.href = '/', 5000);
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
