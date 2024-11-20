import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the data from CSV file
df = pd.read_csv("student_details_test.csv")

# Email server setup (example using Gmail)
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "parkpoom.wisedsri@gmail.com"
sender_password = "gfyu jhkn pmqt tdyg"

# Connect to the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # Secure the connection
server.login(sender_email, sender_password)

# Generate and send an email for each student
for index, row in df.iterrows():
    receiver_email = row['Email']  # student's email
    password = row['Password']  # student's assigned password
    first_name = row['First Name']  # student's first name
    
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
