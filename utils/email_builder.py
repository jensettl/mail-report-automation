# Functions for building and sending emails

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from pathlib import Path

logger = logging.getLogger(__name__)

SMTP_PORT = config.SMTP_PORT  # Standard port for email submission
SMTP_SERVER = config.SMTP_SERVER  # Google SMTP server
PWD = config.EMAIL_PWD  # Password for email account

def sendEmail(email_from, email_to, subject, body):
    msg = MIMEMultipart("alternative")  # Create a multipart message
    msg["From"] = email_from  # Add sender email to message
    msg["To"] = email_to  # Add receiver email to message
    msg["Subject"] = subject  # Add subject to message

    # Add body to email
    msg.attach(MIMEText(body, "html"))

    text = msg.as_string()

    try:
        logger.info("Connecting to SMTP server...")
        TIE_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        TIE_server.starttls()
        TIE_server.login(email_from, PWD)
        logger.info("Connected to SMTP server successfully")

        logger.info(f"Sending email to {email_to}")
        TIE_server.sendmail(email_from, email_to, text)
        logger.info(f"Email successfully sent to {email_to}")

    except Exception as e:
        logger.error(f"An error occurred while sending email: {e}", exc_info=True)

    finally:
        TIE_server.quit()
        logger.debug("SMTP connection closed")
        

def build_email_body(weather_data, astronomy_data, stock_data, cleaned_headlines):
    """ Building the HTML Body of the email"""
    
    # Load CSS from assets/css/styles.css (relative to project root)
    try:
        project_root = Path(__file__).resolve().parents[1]  # mail-report-automation/
        css_path = project_root / "assets" / "css" / "styles.css"
        styles = css_path.read_text(encoding="utf-8")
    except Exception:
        # Fallback minimal styles if file can't be read
        styles = """
        body { background-color: #f4f4f4; font-family: Arial, sans-serif; margin:0; padding:0; }
        .email-container { background-color:#fff; padding:20px; border-radius:8px; max-width:800px; margin:20px auto; }
        .header { font-size:24px; font-weight:bold; margin-bottom:20px; }
        .index-row { display:flex; flex-wrap:wrap; gap:10px; }
        .index-box { background:#cfdee9; padding:10px; border-radius:5px; flex:1; min-width:150px; }
        .stock-info { background:#f9f9f9; padding:5px; border-radius:5px; margin-bottom:20px; text-align:left; position:relative; }
        .recommendation-bar { display:flex; height:20px; border-radius:5px; overflow:hidden; }
        .strong-buy { background:#28a745; } .buy { background:#007bff; } .hold { background:#ffc107; } .sell { background:#fd7e14; } .strong-sell { background:#dc3545; }
        .footer { font-size:12px; color:#999; margin-top:20px; }
        """
    
    # Stocks Section
    stock_html = ""
    for stock in stock_data:
        stock_html += f"""
            <div class="stock-info">
                <div class="stock-info-header">
                    <p><strong>{stock}</strong></p>
                </div>
                <p>Closing at {stock_data[stock]['closing_price']}€ <i>({stock_data[stock]['changeSymbol']}{stock_data[stock]['changePct']}%)</i></p>
                <div class="recommendation-bar">
                    <div class="strong-buy" style="width: {stock_data[stock]['strongBuy']}%">StrongBuy ({stock_data[stock]['strongBuy']}%)</div>
                    <div class="buy" style="width: {stock_data[stock]['buy']}%">Buy ({stock_data[stock]['buy']}%)</div>
                    <div class="hold" style="width: {stock_data[stock]['hold']}%">Hold ({stock_data[stock]['hold']}%)</div>
                    <div class="sell" style="width: {stock_data[stock]['sell']}%">Sell ({stock_data[stock]['sell']}%)</div>
                    <div class="strong-sell" style="width: {stock_data[stock]['strongSell']}%">StrongSell ({stock_data[stock]['strongSell']}%)</div>
                </div>
            </div>
        """
    
    # Headlines Section
    articles_html = ""
    for article in cleaned_headlines:
        articles_html += f"""
            <div class="index-box">
                <h3><a href="{article['url']}">{article['title']}</a></h3>
                <p style="color:grey; font-size:12px">{article['published_at']}</p>
                <p>{article['description']}</p>
            </div>
        """
            
    return f"""
        <html lang="de">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Stock Report</title>
                <style>
                    {styles}
                </style>
            </head>
                <body>
            <div class="email-container">
                <!-- Header Titel -->
                <div class="header">Daily Report</div>
                <!-- Weather Section -->
                <div class="section">
                    <h2>Weather for {weather_data["location"]}, {weather_data["country"]} </h2>
                    <p>Temperature: {weather_data["temperature"]}°C</p>
                    <p>Humidity: {weather_data["humidity"]}%</p>
                    <p>Wind: {weather_data["wind_speed"]} km/h</p>
                    <p>Condition: {weather_data["condition"]}</p>
                    <p>Sunrise: {astronomy_data["sunrise"]}</p>
                    <p>Sunset: {astronomy_data["sunset"]}</p>
                    <p class="footer">Last Updated: {weather_data["last_updated"]}</p>
                </div>
                
                <!-- Stock Section -->
                <div class="section">
                    <h2>Stocks</h2>
                    {stock_html}
                </div>
                
                <!-- Headlines Section -->
                <div class="section">
                    <h2>Headlines</h2>
                    <div class="index-row">
                        {articles_html}
                    </div>
                
                <!-- Footer -->
                <div class="footer">This is an automated email</div>
            </div>
            </body>
        </html>
    """