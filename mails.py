import smtplib
import time
from tkinter import *
from tkinter import filedialog
import re
from email.utils import formataddr

# List of recipients
recipients = []

def validate_email(email):
    """Validate email using regex."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    if not re.match(r"[^@]+@(gmail|yahoo|hotmail)\.com", email):
        return False
    return True

def send_emails(sender_email, sender_password, sender_name, subject, email_body, link):
    # Connect to SMTP server and login
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender_email, sender_password)
    
    # Delare a variable to handle the recipient name
    start = 0
    end = 4

    # Send email to each recipient
    for recipient in recipients:
        if validate_email(recipient):
            # Set email headers
            from_header = formataddr((sender_name, sender_email))
            message = f"From: {from_header}\n"
            message += f"To: {recipient}\n"
            message += f"Subject: {subject}\n\n"
            message += f"Hello {recipient[start:end]},\n"
            message += email_body
            message += f"\n\n {link}"

            # Send email
            smtp_server.sendmail(sender_email, recipient, message)
            status_text.insert(END, f"Email sent to {recipient} successfully!\n")
        else:
            status_text.insert(END, f"Invalid email address: {recipient}\n")

    # Disconnect from SMTP server
    smtp_server.quit()

    status_text.insert(END, "Emails sent successfully!\n")

def select_file():
    global recipients
    file_path = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("Word Files", "*.docx")))
    with open(file_path, 'r') as f:
        recipients = f.read().splitlines()
    status_text.insert(END, "Recipients loaded successfully!\n")

def send_emails_periodically(sender_name):
    while True:
        send_emails(sender_name)
        time.sleep(3600) # delay for one hour

# Create GUI
root = Tk()
root.title("Email Sender")
root.configure(bg="blue")

# Create entry and label for sender's email
sender_email_label = Label(root, text="Enter sender's email:", bg="blue", fg="white")
sender_email_label.pack()
sender_email_entry = Entry(root)
sender_email_entry.pack()

# Create entry and label for sender's password
sender_password_label = Label(root, text="Enter sender's password:", bg="blue", fg="white")
sender_password_label.pack()
sender_password_entry = Entry(root, show="*")  # Mask the password input
sender_password_entry.pack()


# Create label and button for selecting file
label = Label(root, text="Select file with email addresses:", bg="blue", fg="white")
label.pack()
select_file_button = Button(root, text="Select File", command=select_file, bg="red", fg="white")
select_file_button.pack()

# Create entry and label for sender name
sender_name_label = Label(root, text="Enter sender name:", bg="blue", fg="white")
sender_name_label.pack()
sender_name_entry = Entry(root)
sender_name_entry.pack()

# Create entry and label for subject
subject_label = Label(root, text="Enter subject:")
subject_label.pack()
subject_entry = Entry(root)
subject_entry.pack()

# Create entry and label for email body
email_body_label = Label(root, text="Enter email body:", bg="blue", fg="white")
email_body_label.pack()
email_body_entry = Text(root, height=10, width=50)
email_body_entry.pack()

# Create entry and label for link
link_label = Label(root, text="Enter link:", bg="blue", fg="white")
link_label.pack()
link_entry = Entry(root)
link_entry.pack()

send_button = Button(root, text="Send Emails", command=lambda: send_emails(sender_email_entry.get(), sender_password_entry.get(), sender_name_entry.get(), subject_entry.get(), email_body_entry.get("1.0", END), link_entry.get()), bg="red", fg="white")
send_button.pack()


# Create text widget for displaying status messages
status_text = Text(root, height=5, width=50,fg="black",bg="green")
status_text.pack()

root.mainloop()
