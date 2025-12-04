# Celery tasks for background processing
from celery import Celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from weasyprint import HTML, CSS
from jinja2 import Template

# Initialize Celery
celery_app = Celery(
    "cab_booking",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def generate_receipt_pdf(ride_id: int, ride_data: dict):
    """Generate PDF receipt for completed ride"""
    
    # HTML template for receipt
    receipt_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Ride Receipt</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .details { margin: 20px 0; }
            .total { font-weight: bold; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Cab Booking Receipt</h1>
            <p>Receipt #{{ receipt_number }}</p>
        </div>
        
        <div class="details">
            <p><strong>Ride ID:</strong> {{ ride_id }}</p>
            <p><strong>Date:</strong> {{ date }}</p>
            <p><strong>From:</strong> {{ pickup_address }}</p>
            <p><strong>To:</strong> {{ drop_address }}</p>
            <p><strong>Driver:</strong> {{ driver_name }}</p>
            <p><strong>Distance:</strong> {{ distance }} km</p>
            <p><strong>Duration:</strong> {{ duration }} minutes</p>
        </div>
        
        <div class="total">
            <p>Total Fare: ₹{{ fare_amount }}</p>
        </div>
    </body>
    </html>
    """
    
    try:
        # Render template
        template = Template(receipt_template)
        html_content = template.render(**ride_data)
        
        # Generate PDF
        pdf_path = f"receipts/receipt_{ride_id}.pdf"
        os.makedirs("receipts", exist_ok=True)
        
        HTML(string=html_content).write_pdf(pdf_path)
        
        return {"status": "success", "pdf_path": pdf_path}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@celery_app.task
def send_receipt_email(user_email: str, pdf_path: str, ride_data: dict):
    """Send receipt via email"""
    
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("SMTP_EMAIL")
        sender_password = os.getenv("SMTP_PASSWORD")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = f"Ride Receipt - #{ride_data['receipt_number']}"
        
        # Email body
        body = f"""
        Dear Customer,
        
        Thank you for using our cab service. Please find your ride receipt attached.
        
        Ride Details:
        - From: {ride_data['pickup_address']}
        - To: {ride_data['drop_address']}
        - Fare: ₹{ride_data['fare_amount']}
        
        Best regards,
        Cab Booking Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        with open(pdf_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= receipt_{ride_data["ride_id"]}.pdf'
            )
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return {"status": "success", "message": "Email sent successfully"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@celery_app.task
def update_driver_ratings(driver_id: int):
    """Update driver average rating after new review"""
    # This would calculate and update driver's average rating
    # Implementation would query all reviews for driver and calculate average
    pass

@celery_app.task
def process_wallet_topup(user_id: int, amount: float, payment_intent_id: str):
    """Process wallet top-up after successful Stripe payment"""
    # This would add money to user's wallet after payment confirmation
    pass