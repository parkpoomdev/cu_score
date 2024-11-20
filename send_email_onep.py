import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email server setup (example using Gmail)
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "parkpoom.wisedsri@gmail.com"
sender_password = "gfyu jhkn pmqt tdyg"  # Example App Password (Make sure to use your actual App Password)

# Connect to the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # Secure the connection
server.login(sender_email, sender_password)

# Define the details for the test email
receiver_email = "test@example.com"  # Replace with the actual email address for testing
password = "1234"  # Example password
first_name = "Test User"  # Example first name

# Create the email message
message = MIMEMultipart("alternative")
message["Subject"] = "Login Credentials"
message["From"] = sender_email
message["To"] = receiver_email

# Email body
text = f"""
Dear {first_name},

Here is your username and password to sign in and view your scores:

Username: {receiver_email}
Password: {password}

Please ensure you keep this information secure.

Best regards,
University Administration
"""

# Convert to MIMEText objects
part = MIMEText(text, "plain")
message.attach(part)

# Send the email
try:
    server.sendmail(sender_email, receiver_email, message.as_string())
    print(f"Email successfully sent to {receiver_email}")
except Exception as e:
    print(f"Failed to send email to {receiver_email}. Error: {str(e)}")

# Close the SMTP server
server.quit()
