##################################################################################################################
import os
import smtplib
import sqlite3
from tkinter import *
from tkinter import messagebox
from pathlib import Path
from dotenv import load_dotenv
from tkhtmlview import HTMLLabel
from cryptography.fernet import Fernet

from main import database_file_path, env_file_path
import Home
##################################################################################################################


# Window for Login
class WinLogin:

    def __init__(self, master):
        self.root = master
        self.root.title("Login Window")
        self.root.geometry("380x230+450+150")
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Register the username_placeholder_vanish function
        username_placeholder_vanish_func = self.root.register(self.username_placeholder_vanish)
        # Register the password_placeholder_vanish function
        password_placeholder_vanish_func = self.root.register(self.password_placeholder_vanish)

        # Username Label and Entry
        self.username_label = Label(self.root, text="Username:", font=('Helvetica', 15))
        self.username_label.grid(row=0, column=0, padx=(15, 10), pady=(30, 0), sticky=E)
        self.username_entry = Entry(self.root, fg="#BFBFBF", font=('Helvetica', 15),
                                    validate="focusin", validatecommand=username_placeholder_vanish_func)
        self.username_entry.grid(row=0, column=1, padx=10, pady=(30, 0), columnspan=3)

        # Password Label and Entry
        self.password_label = Label(self.root, text="Password:", font=('Helvetica', 15))
        self.password_label.grid(row=1, column=0, padx=(15, 10), pady=10, sticky=E)
        self.password_entry = Entry(self.root, fg="#BFBFBF", font=('Helvetica', 15),
                                    validate="focusin", validatecommand=password_placeholder_vanish_func)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        # Login Button
        self.login_button = Button(self.root, text="Login", bg="#90EE90", font=('Helvetica', 11),
                                   command=self.login_check)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20, padx=(25, 0), ipadx=6)

        # SignUp Button
        self.signup_button = Button(self.root, text="SignUp", bg="#add8e6", font=('Helvetica', 11),
                                    command=lambda: self.forgot_signup_window(WinSignup))
        self.signup_button.grid(row=2, column=2, columnspan=2, pady=20, padx=(0, 50), ipadx=6)

        # Forgot Password Button
        self.forgot_pass_button = Button(self.root, text="Forgot Password?", fg="blue", relief=FLAT,
                                         command=lambda: self.forgot_signup_window(WinForgotPass))
        self.forgot_pass_button.grid(row=3, column=1, padx=(0, 30), columnspan=2)

        # Placeholder for our Entry Boxes and also giving a message to distinguish
        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")

        # Loading our .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

    def username_placeholder_vanish(self):
        if self.username_entry.get() == "Username":
            # Deleting the Placeholder and making foreground "black"
            self.username_entry.delete(0, END)
            self.username_entry.config(fg="black")

    def password_placeholder_vanish(self):
        if self.password_entry.get() == "Password":
            # Deleting the Placeholder, making foreground "black" and also the "show"
            self.password_entry.delete(0, END)
            self.password_entry.config(fg="black", show=self.bullet_symbol)

    def login_check(self):
        # Storing the Entry Boxes value in variables
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Password and OID for the given Username
            query = 'Select Password, oid from Users where Username=?'
            c.execute(query, (username,))

            encrypted_user_password, oid = c.fetchone()
            # Decrypting user password
            original_user_password = self.cipher_suite.decrypt(encrypted_user_password).decode()

            conn.commit()
            conn.close()

            # Checking whether password provided matched
            if password == original_user_password:
                self.new_window(Home.WinHome, oid)
            else:
                messagebox.showerror("Error", "Incorrect Username or Password!", parent=self.root)

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!", parent=self.root)

    def forgot_signup_window(self, _class):
        level = Tk()
        _class(level)
        self.root.destroy()

    def new_window(self, _class, oid):
        level = Tk()
        _class(level, oid)
        self.root.destroy()

##################################################################################################################


# Window for SignUp
class WinSignup:

    def __init__(self, master):
        self.root = master
        self.root.title("SignUp Window")
        self.root.geometry('380x280+450+150')
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Username Label and Entry
        self.username_label = Label(self.root, text="Username:", font=('Helvetica', 15))
        self.username_label.grid(row=0, column=0, padx=10, pady=(30, 0), sticky=E)
        self.username_entry = Entry(self.root, font=('Helvetica', 15))
        self.username_entry.grid(row=0, column=1, padx=10, pady=(30, 0), columnspan=3)

        # Password Label and Entry
        self.password_label = Label(self.root, text="Password:", font=('Helvetica', 15))
        self.password_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky=E)
        self.password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.password_entry.grid(row=1, column=1, padx=10, pady=(10, 0), columnspan=3)

        # Email Label and Entry
        self.email_label = Label(self.root, text="Email:", font=('Helvetica', 15))
        self.email_label.grid(row=2, column=0, padx=10, pady=10, sticky=E)
        self.email_entry = Entry(self.root, font=('Helvetica', 15))
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=3)

        # Admin Secret Key
        self.secret_label = Label(self.root, text="Secret Key:", font=('Helvetica', 15))
        self.secret_label.grid(row=3, column=0, padx=10, pady=(20, 10), sticky=E)
        self.secret_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.secret_entry.grid(row=3, column=1, padx=10, pady=(20, 10), columnspan=3)

        # Back Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11),
                                  command=self.close_window)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, padx=(30, 0), ipadx=4)

        # Submit Button
        self.submit_button = Button(self.root, text="Submit", bg="#90EE90", font=('Helvetica', 11),
                                    command=self.signup_check)
        self.submit_button.grid(row=4, column=2, columnspan=2, pady=20, padx=(0, 60), ipadx=4)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

        # Getting the Secret Key
        self.encrypted_secret_key = os.environ.get('SECRET_KEY')

    def signup_check(self):
        # if any entry not filled then warning message displayed
        if self.username_entry.get() == '' or self.password_entry.get() == '' or self.email_entry.get() == '' or \
                self.secret_entry.get() == '':
            messagebox.showwarning("Warning", "Please Fill The Details!", parent=self.root)
            return

        # Storing the values of Entry Boxes
        username = self.username_entry.get()
        password = self.password_entry.get()
        email_id = self.email_entry.get()
        secret_key = self.secret_entry.get()

        # Clearing the Entry Boxes
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.secret_entry.delete(0, END)

        # Check whether valid email was provided
        if '@' not in email_id or '.' not in email_id:
            messagebox.showwarning("Warning", "Please provide a valid email!", parent=self.root)
            return

        # Decrypting secret key
        original_secret_key = self.cipher_suite.decrypt(self.encrypted_secret_key).decode()

        if not secret_key == original_secret_key:
            messagebox.showerror("Error", "Incorrect Secret Key!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Encrypting user password
                password = self.cipher_suite.encrypt(password.encode())

                # Inserting Details of New User
                query = "Insert Into users(Username, Email_id, Password) values(?, ?, ?)"
                c.execute(query, (username, email_id, password))
                conn.commit()

                # Displaying message informing that account was added successfully
                messagebox.showinfo("Information", "Account Successfully Added!", parent=self.root)

                conn.commit()
                conn.close()

                self.close_window()

            except sqlite3.IntegrityError:
                messagebox.showwarning("Warning", "Username Already Taken!\nPlease Enter Other Username!",
                                       parent=self.root)
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinLogin(level)
        self.root.destroy()

##################################################################################################################


# Window for Forgot Password
class WinForgotPass:

    def __init__(self, master):
        self.root = master
        self.root.title("Forgot Password Window")
        self.root.geometry("360x245+450+150")
        self.root.resizable(width=False, height=False)

        # Instruction Label
        self.instruction_label = Label(self.root,
                                       text="Provide Your Email-id where the\npassword will be shared.",
                                       font=('Helvetica', 13), fg="green")
        self.instruction_label.pack(padx=25, pady=(20, 0))

        # Frame for email label and Entry
        self.email_frame = Frame(self.root)
        self.email_frame.pack(padx=(17, 0), pady=20)

        # Email Label and Entry
        self.email_label = Label(self.email_frame, text="Email:", font=('Helvetica', 15))
        self.email_label.grid(row=0, column=0, padx=10)
        self.email_entry = Entry(self.email_frame, font=('Helvetica', 15))
        self.email_entry.grid(row=0, column=1, padx=(0, 30))

        # Frame for Buttons
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=10)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=('Helvetica', 11),
                                  command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 20), ipadx=10)

        # Send Button
        self.send_button = Button(self.button_frame, text="Send", bg="#90EE90", font=('Helvetica', 11),
                                  command=self.email_check)
        self.send_button.grid(row=0, column=1, padx=(20, 20), ipadx=10)

        # Our Gmail and Yahoo Links
        self.link_label = HTMLLabel(self.root, html="<a href='https://www.gmail.com'>Gmail</a>"
                                                    "----"
                                                    "<a href='https://www.yahoo.com'>Yahoo</a>")
        self.link_label.pack(padx=(101, 0), pady=(15, 0), fill=BOTH, expand=True)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        self.EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

    def send_mail(self, email, user_password):
        # Sending Email Code
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)

            subject = 'Forgot Password: Factory Simulation Software'
            body = f'Dear User\n\nPlease find your Password of your Factory Simulation Account\n\nPassword: {user_password}'

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(self.EMAIL_ADDRESS, email, msg)

    def email_check(self):
        # Displaying Message Informing that it will take some time
        messagebox.showinfo("Information", "It may take some time\nPlease Wait!!!", parent=self.root)

        # Grabbing the Email provided
        email = self.email_entry.get()

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Password for the given Email_id
            query = 'Select Password from Users where Email_id=?'
            c.execute(query, (email,))

            user_password = c.fetchone()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

        # Whether password corresponding to given email exists
        if user_password is None:
            messagebox.showerror("Error", "Incorrect! Email-id!", parent=self.root)
        else:
            try:
                # Decrypting user password
                user_password = self.cipher_suite.decrypt(user_password[0]).decode()

                # Sending mail
                self.send_mail(email, user_password)

                # Message to inform that Email has been sent
                messagebox.showinfo("Information", "Mail has been sent Successfully:)", parent=self.root)
                self.close_window()

            except smtplib.SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error
                messagebox.showerror(f"Error Code: {error_code}",
                                     f"Error Message: {error_message}\nPlease Try Again!",
                                     parent=self.root)

    def close_window(self):
        level = Tk()
        WinLogin(level)
        self.root.destroy()
