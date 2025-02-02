import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template_string

# File to store appointments
file_path = "appointments.csv"

# Create the file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Email"])
    df.to_csv(file_path, index=False)


# Send email function
def send_email(name, date, time, email):
    """Sends an appointment confirmation email."""
    sender_email = "your-email@example.com"
    sender_password = "your-email-password"

    msg = MIMEText(f"Hello {name}, your appointment is booked for {date} at {time}.")
    msg["Subject"] = "Appointment Confirmation"
    msg["From"] = sender_email
    msg["To"] = email

    try:
        with smtplib.SMTP("smtp.your-email-provider.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        print(f"📩 Confirmation email sent to {email}.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# Flask app
app = Flask(__name__)


# Home route
@app.route('/')
def home():
    return "Welcome to the Appointment Bot!"


# Book Appointment route (Displays the form)
@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        # Getting form data
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        email = request.form['email']

        # Save to CSV
        df = pd.read_csv(file_path)
        new_appointment = pd.DataFrame({"Name": [name], "Date": [date], "Time": [time], "Email": [email]})
        df = pd.concat([df, new_appointment], ignore_index=True)
        df.to_csv(file_path, index=False)

        # Send confirmation email
        send_email(name, date, time, email)

        return f"✅ Appointment booked for {name} on {date} at {time}. Confirmation email sent to {email}."

    return '''
        <form method="POST">
            Name: <input type="text" name="name"><br>
            Date: <input type="text" name="date" placeholder="YYYY-MM-DD"><br>
            Time: <input type="text" name="time" placeholder="HH:MM AM/PM"><br>
            Email: <input type="email" name="email"><br>
            <input type="submit" value="Book Appointment">
        </form>
    '''


# View appointments route
@app.route('/view_appointments')
def view_appointments():
    df = pd.read_csv(file_path)
    if df.empty:
        return "No appointments found."
    else:
        return df.to_html()


if __name__ == '__main__':
    app.run(debug=True)
