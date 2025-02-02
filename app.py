@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        email = request.form['email']

        # Save the data to a CSV file
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
            <inp
