from flask import Flask, Response, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>RS Automation</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="RS Automation builds audit-ready automation tools for banks and financial institutions—no core access required.">
        <meta name="keywords" content="risk automation, bank compliance, reporting tools, excel automation, audit support">
        <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link rel="icon" type="image/png" href="/static/favicon.png">
        <style>
            body {
                font-family: 'Aptos Serif', Georgia, serif;
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
                font-family: "Aptos Serif", Georgia, serif;
                font-size: 0.9rem;
                padding: 8px 30px;
                box-sizing: border-box;
                z-index: 999;
            }
            .contact-bar a {
                color: #00A1DA;
                text-decoration: none;
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
            h2 {
                color: #00A1DA;
                margin-bottom: 10px;
                text-align: center;
            }
            .centered-section {
                text-align: center;
                max-width: 700px;
                margin: 0 auto;
            }
            .centered-section p {
                line-height: 1.6;
            }
            .icon-service-grid, .icon-service-row {
                display: flex;
                flex-wrap: wrap;
                gap: 30px;
                justify-content: center;
                margin-top: 30px;
                width: 100%;
                box-sizing: border-box;
            }
            .icon-service-item {
                text-align: center;
                flex: 1 1 250px;
                max-width: 250px;
                flex-shrink: 0;
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
            .cta {
                background-color: rgba(255, 255, 255, 0.1);
                padding: 25px;
                border-radius: 10px;
                text-align: center;
            }
            .cta h2 {
                margin-bottom: 10px;
            }
            .testimonial {
                font-style: italic;
                font-size: 1rem;
                color: #ddd;
                margin: 10px 0;
                text-align: center;
            }
            .calendly-section {
                margin-top: 30px;
                text-align: center;
            }
            footer {
                text-align: center;
                font-size: 0.9em;
                color: #bbb;
                margin-top: 60px;
            }
        </style>
    </head>
    <body>
        <div class="contact-bar">
            <p>
                <i class="fas fa-envelope"></i> <a href="mailto:ramirez.ricardo55@yahoo.com">ramirez.ricardo55@yahoo.com</a> | 
                <i class="fas fa-phone"></i> <a href="tel:+19154785436">(915) 478-5436</a>
            </p>
        </div>
        <div class="main-wrapper">
            <div class="container-box">
                <header class="header">
                    <img src="/static/logo.png" alt="RS Automation Logo">
                    <h1>RS Automation</h1>
                    <p class="tagline">Risk Reporting Automation</p>
                </header>
                <section class="centered-section">
                    <h2>What We Do</h2>
                    <p>RS Automation delivers precise, scalable solutions for banks and financial institutions by automating reporting, integrating risk insights, flagging exceptions, and simplifying audit workflows. Our tools reduce manual effort and increase reliability—so your team can focus on action, not repetition.</p>
                </section>
            </div>
            <div class="container-box">
                <section>
                    <h2>Core Services</h2>
                    <div class="icon-service-grid">
                        <div class="icon-service-item">
                            <i class="fas fa-file-excel"></i>
                            <p><strong>Excel Report Automation - 100% Compliance</strong><br>
                            <span class="service-subtext">Automate repetitive reporting tasks with fully audit-ready outputs. No more user-error.</span></p>
                        </div>
                        <div class="icon-service-item">
                            <i class="fas fa-microchip"></i>
                            <p><strong>Risk Model Integration, Insights & Alerts</strong><br>
                            <span class="service-subtext">Turn historical and live data into early-warning risk indicators.</span></p>
                        </div>
                        <div class="icon-service-item">
                            <i class="fas fa-clipboard-check"></i>
                            <p><strong>Audit Support Workflows</strong><br>
                            <span class="service-subtext">Structured logic, exception flagging, and tracking to simplify audits.</span></p>
                        </div>
                        <div class="icon-service-item">
                            <i class="fas fa-bolt"></i>
                            <p><strong>Exception-Driven Issue Detection</strong><br>
                            <span class="service-subtext">Automatically detect anomalies and route key issues for review.</span></p>
                        </div>
                    </div>
                </section>
            </div>
            <div class="container-box">
                <section>
                    <h2>How It Works</h2>
                    <div class="icon-service-row">
                        <div class="icon-service-item">
                            <i class="fas fa-file-export"></i>
                            <p><strong>1. Export Your Data</strong><br>
                            <span class="service-subtext">Export your Excel or report file and remove any sensitive info—we only need structure.</span></p>
                        </div>
                        <div class="icon-service-item">
                            <i class="fas fa-cogs"></i>
                            <p><strong>2. We Automate It</strong><br>
                            <span class="service-subtext">We convert your reporting logic into a reusable, audit-ready tool.</span></p>
                        </div>
                        <div class="icon-service-item">
                            <i class="fas fa-file-alt"></i>
                            <p><strong>3. Receive Final Report</strong><br>
                            <span class="service-subtext">You get a clean, consistent output you can use instantly—no installs, no complexity.</span></p>
                        </div>
                    </div>
                </section>
            </div>
            <div class="container-box">
                <section>
                    <h2>What Our Partners Say</h2>
                    <p class="testimonial">"We went from 8 hours of manual reporting every week to 20 minutes. It's fast and 100% accurate."</p>
                    <p class="testimonial">"We didn’t have to change our process—we just sent them the file and got a tool back that works."</p>
                </section>
            </div>
            <div class="container-box">
                <section class="calendly-section">
                    <h2>Book a 15-Minute Demo</h2>
                    <iframe src="https://calendly.com/ramirez-ricardo55/30min" width="100%" height="400" frameborder="0" scrolling="no"></iframe>
                </section>
            </div>
            <div class="container-box">
                <section class="cta">
                    <h2>Ready to streamline your reporting?</h2>
                    <p>Email us at <a href="mailto:ramirez.ricardo55@yahoo.com">ramirez.ricardo55@yahoo.com</a></p>
                </section>
                <footer>
                    © 2025 RS Automation. All rights reserved.
                </footer>
            </div>
        </div>
    </body>
    </html>
    '''
    return Response(html, mimetype='text/html')

@app.route('/download')
def download_pdf():
    return send_from_directory('static', 'RS_Automation_Overview.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
