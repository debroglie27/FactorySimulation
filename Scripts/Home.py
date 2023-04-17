##################################################################################################################
import os
import smtplib
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from dotenv import load_dotenv, set_key
from tkhtmlview import HTMLLabel
from cryptography.fernet import Fernet

from main import database_file_path, env_file_path
import LoginSystem
import Machine
import Adjuster
import Maintenance
##################################################################################################################


# Window for Home
class WinHome:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Home Window")
        self.root.geometry("377x350+450+110")
        self.root['bg'] = "#90EE90"
        self.root.resizable(width=False, height=False)

        # Heading Label
        self.head_label = Label(self.root, text="Factory Simulation", fg="purple",
                                bg='#add8e6', bd=4, relief=GROOVE, font=('Monotype Corsiva', 32, "bold"))
        self.head_label.pack(pady=(0, 10), ipadx=28, ipady=5)

        # Machine, Adjuster and Maintenance Window Button
        self.but_machine = Button(self.root, text="Machine", font=('Helvetica', 15), bg='#fdebd0',
                                  command=lambda: self.new_window(Machine.WinMachine, self.user_oid))
        self.but_machine.pack(pady=(32, 0), ipadx=32)
        self.but_adjuster = Button(self.root, text="Adjuster", font=('Helvetica', 15), bg='#fdebd0',
                                   command=lambda: self.new_window(Adjuster.WinAdjuster, self.user_oid))
        self.but_adjuster.pack(pady=(26, 0), ipadx=32)
        self.but_maintenance = Button(self.root, text="Maintenance", font=('Helvetica', 15), bg='#fdebd0',
                                      command=lambda: self.new_window(Maintenance.WinMaintenance, self.user_oid))
        self.but_maintenance.pack(pady=(26, 0), ipadx=12)

        # Create Menu
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        # Add File Menu
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        # Add File Menu Items
        self.file_menu.add_command(label="Machine",
                                   command=lambda: self.new_window(Machine.WinMachine, self.user_oid))
        self.file_menu.add_command(label="Adjuster",
                                   command=lambda: self.new_window(Adjuster.WinAdjuster, self.user_oid))
        self.file_menu.add_command(label="Maintenance",
                                   command=lambda: self.new_window(Maintenance.WinMaintenance, self.user_oid))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Logout", command=lambda: self.logout(LoginSystem.WinLogin))
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Add Settings Menu
        self.settings_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Settings", menu=self.settings_menu)
        # Add Settings Menu Items
        self.settings_menu.add_command(label="User Details",
                                       command=lambda: self.new_window(WinUserDetails, self.user_oid))
        self.settings_menu.add_command(label="Change Password",
                                       command=lambda: self.new_window(WinChangePassword, self.user_oid))

        # Only for Admin
        if self.user_oid == 1:
            # Add Admin Settings Menu
            self.admin_settings_menu = Menu(self.my_menu, tearoff=False)
            self.my_menu.add_cascade(label="Admin Settings", menu=self.admin_settings_menu)
            # Add Settings Menu Items
            self.admin_settings_menu.add_command(label="All User Details",
                                                 command=lambda: self.new_window(WinAllUserDetails, self.user_oid))
            self.admin_settings_menu.add_command(label="Change Secret Key",
                                                 command=lambda: self.new_window(WinChangeSecretKey, self.user_oid))

        # Add Right Click Pop Up Menu
        self.my_popup_menu = Menu(self.root, tearoff=False)
        # Insert, Search, Update and Delete
        self.my_popup_menu.add_command(label="Machine",
                                       command=lambda: self.new_window(Machine.WinMachine, self.user_oid))
        self.my_popup_menu.add_command(label="Adjuster",
                                       command=lambda: self.new_window(Adjuster.WinAdjuster, self.user_oid))
        self.my_popup_menu.add_command(label="Maintenance",
                                       command=lambda: self.new_window(Maintenance.WinMaintenance, self.user_oid))
        self.my_popup_menu.add_separator()
        # User Details and Change Password
        self.my_popup_menu.add_command(label="User Details",
                                       command=lambda: self.new_window(WinUserDetails, self.user_oid))
        self.my_popup_menu.add_command(label="Change Password",
                                       command=lambda: self.new_window(WinChangePassword, self.user_oid))
        self.my_popup_menu.add_separator()

        # Only for Admin
        if self.user_oid == 1:
            # All User Details and Change Secret Key
            self.my_popup_menu.add_command(label="All User Details",
                                           command=lambda: self.new_window(WinAllUserDetails, self.user_oid))
            self.my_popup_menu.add_command(label="Change Secret Key",
                                           command=lambda: self.new_window(WinChangeSecretKey, self.user_oid))
            self.my_popup_menu.add_separator()

        # Logout and Exit
        self.my_popup_menu.add_command(label="Logout", command=lambda: self.logout(LoginSystem.WinLogin))
        self.my_popup_menu.add_command(label="Exit", command=self.root.quit)

        # Binding the Right click Pop Up Menu
        self.root.bind("<Button-3>", self.my_popup)

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Username for our Status Bar
            query = 'Select Username from Users where OID=?'
            c.execute(query, (self.user_oid,))

            username = c.fetchone()[0]

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            username = ''
            messagebox.showerror("Error", "Status Bar Not Working\nPlease Try Again!!!", parent=self.root)

        # Finding whether our user is an ADMIN or not
        if self.user_oid == 1:
            text = f'User: {username} (ADMIN) '
        else:
            text = f'User: {username} '

        # Add Status Bar
        self.status_bar = Label(self.root, text=text, anchor=E, bg="#dfdfdf")
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=1)

    def my_popup(self, event):
        self.my_popup_menu.tk_popup(event.x_root, event.y_root)

    def logout(self, _class):
        level = Tk()
        _class(level)
        self.root.destroy()

    def new_window(self, _class, oid):
        level = Tk()
        _class(level, oid)
        self.root.destroy()

##################################################################################################################


# Window for Displaying User Details
class WinUserDetails:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("User Details")
        self.root.geometry("435x220+440+150")
        self.root.resizable(width=False, height=False)

        # Username Label and Entry
        self.username_label = Label(self.root, text="Username:", font=('Helvetica', 15))
        self.username_label.grid(row=0, column=0, padx=10, pady=(30, 0), sticky=E)
        self.username_entry = Entry(self.root, font=('Helvetica', 15), fg="green", width=19)
        self.username_entry.grid(row=0, column=1, padx=10, pady=(30, 0), sticky=W)

        # Email Label and Entry
        self.email_label = Label(self.root, text="Email:", font=('Helvetica', 15))
        self.email_label.grid(row=1, column=0, padx=10, pady=20, sticky=E)
        self.email_entry = Entry(self.root, font=('Helvetica', 15), fg="green", width=19)
        self.email_entry.grid(row=1, column=1, padx=10, pady=20, sticky=W)

        # Change Buttons
        self.change_button1 = Button(self.root, text="Change", font=('Helvetica', 10), bg="orange",
                                     command=lambda: self.change_entry(0))
        self.change_button1.grid(row=0, column=2, padx=5, pady=(30, 0))
        self.change_button2 = Button(self.root, text="Change", font=('Helvetica', 10), bg="orange",
                                     command=lambda: self.change_entry(1))
        self.change_button2.grid(row=1, column=2, padx=5, pady=20)

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding Details of User
            query = 'Select Username, Email_id from Users where OID=?'
            c.execute(query, (self.user_oid,))

            username, email = c.fetchone()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            username = ''
            email = ''
            messagebox.showerror("Error", "Unable To Fetch User Details\nPlease Try Again!!!", parent=self.root)

        # Displaying Values in Username Entry and Email Entry
        self.username_entry.insert(0, username)
        self.email_entry.insert(0, email)

        # Making the Entry Boxes READ-ONLY
        self.username_entry.config(state="readonly")
        self.email_entry.config(state="readonly")

        # Back and Save Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=3)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11),
                                  command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 40), ipadx=5)

        # Save Button
        self.save_button = Button(self.button_frame, text="Save", bg="#90EE90", font=('Helvetica', 11),
                                  command=self.save_details)
        self.save_button.grid(row=0, column=1, pady=20, padx=(40, 0), ipadx=5)

    def close_window(self):
        level = Tk()
        WinHome(level, self.user_oid)
        self.root.destroy()

    def change_entry(self, val):
        if val == 0:
            self.username_entry.config(state=NORMAL)
        elif val == 1:
            self.email_entry.config(state=NORMAL)

    def save_details(self):
        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Updating the database with new values
            query = "update Users set Username = ?, Email_id = ? where OID = ?"
            e = (self.username_entry.get(), self.email_entry.get(), self.user_oid)
            c.execute(query, e)

            conn.commit()
            conn.close()

            # Message Informing Successful Saving
            messagebox.showinfo("Information", "Successfully Saved", parent=self.root)

            self.close_window()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username Already Taken!\nPlease Enter Other Username", parent=self.root)
        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

##################################################################################################################


# Window for Changing Password
class WinChangePassword:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Change Password")
        self.root.geometry("450x280+440+150")
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Current Password Label and Entry
        self.current_password_label = Label(self.root, text="Current Password:", font=('Helvetica', 15))
        self.current_password_label.grid(row=0, column=0, padx=10, pady=(30, 20), sticky=E)
        self.current_password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.current_password_entry.grid(row=0, column=1, padx=10, pady=(30, 20), sticky=W)

        # New Password Label and Entry
        self.new_password_label = Label(self.root, text="New Password:", font=('Helvetica', 15))
        self.new_password_label.grid(row=1, column=0, padx=10, pady=(20, 10), sticky=E)
        self.new_password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.new_password_entry.grid(row=1, column=1, padx=10, pady=(20, 10), sticky=W)

        # Confirm Password Label and Entry
        self.confirm_password_label = Label(self.root, text="Confirm Password:", font=('Helvetica', 15))
        self.confirm_password_label.grid(row=2, column=0, padx=10, pady=(5, 0), sticky=E)
        self.confirm_password_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=(5, 0), sticky=W)

        # Back and Save Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=3, column=0, pady=20, columnspan=2)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11),
                                  command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 40), ipadx=5)

        # Save Button
        self.save_button = Button(self.button_frame, text="Save", bg="#90EE90", font=('Helvetica', 11),
                                  command=self.change_password)
        self.save_button.grid(row=0, column=1, pady=20, padx=(30, 0), ipadx=5)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

    def close_window(self):
        level = Tk()
        WinHome(level, self.user_oid)
        self.root.destroy()

    def change_password(self):
        # Storing the values of Entry Boxes
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Clearing the Entry Boxes
        self.current_password_entry.delete(0, END)
        self.new_password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Finding password for the given user
            query = "Select Password from Users where oid=?"
            c.execute(query, (self.user_oid,))

            encrypted_password = c.fetchone()[0]

            # Decrypting password
            decrypted_password = self.cipher_suite.decrypt(encrypted_password).decode()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

        if decrypted_password != current_password:
            messagebox.showerror("Error", "Wrong Current Password!!!", parent=self.root)
        else:
            if new_password != confirm_password:
                messagebox.showerror(
                    "Error", "Confirm Password is not same\nas New Password!!!", parent=self.root)
            else:
                # Encrypting user password
                confirm_password = self.cipher_suite.encrypt(confirm_password.encode())

                try:
                    conn = sqlite3.connect(database_file_path)
                    c = conn.cursor()

                    # Updating the password for the given user oid
                    query = "update Users set Password = ? where OID = ?"
                    c.execute(query, (confirm_password, self.user_oid))

                    conn.commit()
                    conn.close()

                    messagebox.showinfo(
                        "Information", "Password Changed Successfully!!!", parent=self.root)

                    self.close_window()

                except sqlite3.OperationalError:
                    messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

##################################################################################################################


# Window for Displaying All User Details
class WinAllUserDetails:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("All User Details")
        self.root.geometry("390x290+450+130")
        self.root.resizable(width=False, height=False)

        # Add some style
        style = ttk.Style(self.root)
        # Pick a theme
        style.theme_use("vista")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#E3E3E3")

        style.map('Treeview',
                  background=[('selected', 'yellow')],
                  foreground=[('selected', 'black')])

        # Create TreeView Frame
        self.tree_frame = Frame(self.root)
        self.tree_frame.pack(pady=(20, 0), padx=10)

        # TreeView ScrollBar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create TreeView
        self.my_tree = ttk.Treeview(self.tree_frame, height=6,
                                    yscrollcommand=self.tree_scroll.set)
        self.my_tree.pack()

        # Configure ScrollBar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our columns
        self.my_tree['columns'] = ("OID", "Username", "Email")

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("OID", anchor=CENTER, width=30)
        self.my_tree.column("Username", anchor=CENTER, width=100)
        self.my_tree.column("Email", anchor=CENTER, width=180)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("OID", text="OID", anchor=CENTER)
        self.my_tree.heading("Username", text="Username", anchor=CENTER)
        self.my_tree.heading("Email", text="Email", anchor=CENTER)

        # Count Variable for number of records
        self.count = 0

        # Create Stripped row Tags
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            c.execute("Select OID, Username, Email_id from Users where oid <> 1")
            records = c.fetchall()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            records = []
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

        # Resetting the Count
        self.count = 0

        for record in records:
            if self.count % 2 == 0:
                self.my_tree.insert(
                    parent='', index='end', iid=str(self.count), text="", values=record, tags=("evenrow",))
            else:
                self.my_tree.insert(
                    parent='', index='end', iid=str(self.count), text="", values=record, tags=("oddrow",))
            self.count += 1

        # Back and Remove Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=(20, 10))

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11),
                                  command=self.close_window)
        self.back_button.grid(row=0, column=0, pady=10, padx=(5, 45), ipadx=5)

        # Remove Button
        self.remove_button = Button(self.button_frame, text="Remove", bg="orange", font=('Helvetica', 11),
                                    command=self.remove_user)
        self.remove_button.grid(
            row=0, column=1, pady=10, padx=(25, 0), ipadx=5)

    def close_window(self):
        level = Tk()
        WinHome(level, self.user_oid)
        self.root.destroy()

    def remove_user(self):
        if self.my_tree.focus():
            for record in self.my_tree.selection():
                # Getting the OID from the record
                oid = self.my_tree.item(record)['values'][0]

                try:
                    conn = sqlite3.connect(database_file_path)
                    c = conn.cursor()

                    c.execute("Delete from Users where oid=?", (oid,))

                    conn.commit()
                    conn.close()

                    # removing the record from the treeview
                    self.my_tree.delete(record)

                    messagebox.showinfo("Information", "Successfully Removed!")

                except sqlite3.OperationalError:
                    messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

        else:
            messagebox.showwarning("Warning", "Please select a record to remove!")

##################################################################################################################


# Window for Changing Secret Key
class WinChangeSecretKey:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Change Secret Key")
        self.root.geometry("456x290+430+130")
        self.root.resizable(width=False, height=False)

        # Bullet Symbol
        self.bullet_symbol = "\u2022"

        # Current Password Label and Entry
        self.current_secret_key_label = Label(
            self.root, text="Current Secret Key:", font=('Helvetica', 15))
        self.current_secret_key_label.grid(
            row=0, column=0, padx=10, pady=(30, 10), sticky=E)
        self.current_secret_key_entry = Entry(
            self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.current_secret_key_entry.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky=W)

        # Forgot Secret Key Button
        self.forgot_secret_key_button = Button(self.root, text="Forgot Secret Key?", fg="blue", relief=FLAT,
                                               command=lambda: self.new_window(WinForgotSecretKey, self.user_oid))
        self.forgot_secret_key_button.grid(row=1, column=0, columnspan=2)

        # New Password Label and Entry
        self.new_secret_key_label = Label(self.root, text="New Secret Key:", font=('Helvetica', 15))
        self.new_secret_key_label.grid(row=2, column=0, padx=10, pady=(15, 10), sticky=E)
        self.new_secret_key_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.new_secret_key_entry.grid(row=2, column=1, padx=10, pady=(15, 10), sticky=W)

        # Confirm Password Label and Entry
        self.confirm_secret_key_label = Label(self.root, text="Confirm Secret Key:", font=('Helvetica', 15))
        self.confirm_secret_key_label.grid(row=3, column=0, padx=10, pady=(5, 0), sticky=E)
        self.confirm_secret_key_entry = Entry(self.root, show=self.bullet_symbol, font=('Helvetica', 15))
        self.confirm_secret_key_entry.grid(row=3, column=1, padx=10, pady=(5, 0), sticky=W)

        # Back and Save Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=4, column=0, pady=20, columnspan=2)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11),
                                  command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(10, 40), ipadx=5)

        # Save Button
        self.save_button = Button(self.button_frame, text="Save", bg="#90EE90", font=('Helvetica', 11),
                                  command=self.change_secret_key)
        self.save_button.grid(row=0, column=1, pady=20, padx=(30, 0), ipadx=5)

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        # Getting the ENCRYPTION_KEY
        key = os.environ.get('ENCRYPTION_KEY')
        self.cipher_suite = Fernet(key)

        # Getting the Secret Key
        self.encrypted_secret_key = os.environ.get('SECRET_KEY')

    def new_window(self, _class, oid):
        level = Tk()
        _class(level, oid)
        self.root.destroy()

    def close_window(self):
        level = Tk()
        WinHome(level, self.user_oid)
        self.root.destroy()

    def change_secret_key(self):
        # Storing the values of Entry Boxes
        current_secret_key = self.current_secret_key_entry.get()
        new_secret_key = self.new_secret_key_entry.get()
        confirm_secret_key = self.confirm_secret_key_entry.get()

        # Clearing the Entry Boxes
        self.current_secret_key_entry.delete(0, END)
        self.new_secret_key_entry.delete(0, END)
        self.confirm_secret_key_entry.delete(0, END)

        # Decrypting secret key - self.encrypted_secret_key is from the __init__() method
        original_secret_key = self.cipher_suite.decrypt(self.encrypted_secret_key).decode()

        if current_secret_key != original_secret_key:
            messagebox.showerror("Error", "Wrong Current Secret Key!!!", parent=self.root)
            return
        else:
            if new_secret_key != confirm_secret_key:
                messagebox.showerror("Error", "Confirm Secret Key is not same\nas New Secret Key!!!", parent=self.root)
                return
            else:
                # Encrypting secret key
                encrypted_confirm_secret_key = self.cipher_suite.encrypt(confirm_secret_key.encode()).decode()

                # Writing the Secret Key onto the .env file
                os.environ['SECRET_KEY'] = encrypted_confirm_secret_key
                set_key(env_file_path, "SECRET_KEY", os.environ["SECRET_KEY"])

                messagebox.showinfo("Information", "Secret Key Changed Successfully!!!", parent=self.root)

                self.close_window()

##################################################################################################################


# Window for Forgetting Secret Key
class WinForgotSecretKey:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Forgot Secret Key")
        self.root.geometry("360x245+450+150")
        self.root.resizable(width=False, height=False)

        # Instruction Label
        self.instruction_label = Label(self.root,
                                       text="Provide Your Email-id where the\nSecret Key will be shared.",
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

        # Getting the Secret Key
        self.encrypted_secret_key = os.environ.get('SECRET_KEY')

    def send_mail(self, email, decrypted_secret_key):
        # Code for sending email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)

            subject = 'Forgot Secret Key: Factory Simulation Software'
            body = f'''Dear User\n\n
                       Please find the Secret Key of the Factory Simulation Account\n\n
                       Secret Key: {decrypted_secret_key}'''

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(self.EMAIL_ADDRESS, email, msg)

    def email_check(self):
        messagebox.showinfo("Information", "It may take some time\nPlease Wait!!!", parent=self.root)

        # Grabbing the email provided
        email = self.email_entry.get()

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Fetching Oid for the given email_id
            query = 'select oid from Users where email_id=?'
            c.execute(query, (email,))

            oid = c.fetchone()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

        # Whether the email provided is of Admin
        if oid is None or oid[0] != 1:
            messagebox.showerror("Error", "Incorrect!!! Email-id", parent=self.root)
        else:
            # Decrypting secret key
            original_secret_key = self.cipher_suite.decrypt(self.encrypted_secret_key).decode()
            try:
                # Sending mail
                self.send_mail(email, original_secret_key)

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
        WinChangeSecretKey(level, self.user_oid)
        self.root.destroy()
