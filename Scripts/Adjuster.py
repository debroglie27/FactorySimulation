##################################################################################################################
import os
import smtplib
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from dotenv import load_dotenv

from main import database_file_path, env_file_path
import Home
##################################################################################################################


# Window for Adjuster Database
class WinAdjuster:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Adjuster Window")
        self.root.geometry("377x380+450+110")
        self.root['bg'] = "#90EE90"
        self.root.resizable(width=False, height=False)

        self.head_label = Label(self.root, text="Adjuster Database", fg="purple", bg='#add8e6', bd=4, relief=GROOVE,
                                font=('Monotype Corsiva', 32, "bold"))
        self.head_label.pack(pady=(0, 10), ipadx=32, ipady=5)

        # Insert Search Update Delete Buttons
        self.but_insert = Button(self.root, text="Insert", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinAdjusterInsert, self.user_oid))
        self.but_insert.pack(pady=(15, 0), ipadx=35)
        self.but_search = Button(self.root, text="Search", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinAdjusterSearch, self.user_oid))
        self.but_search.pack(pady=(20, 0), ipadx=29)
        self.but_update = Button(self.root, text="Update", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinAdjusterUpdate, self.user_oid))
        self.but_update.pack(pady=(20, 0), ipadx=29)
        self.but_delete = Button(self.root, text="Delete", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinAdjusterDelete, self.user_oid))
        self.but_delete.pack(pady=(20, 0), ipadx=32)

        # Back Button
        self.but_back = Button(self.root, text="Back", font=('Helvetica', 10), bg="#add8e6",
                               command=lambda: self.new_window(Home.WinHome, self.user_oid))
        self.but_back.pack(pady=(10, 0), padx=(5, 0), ipadx=5, anchor=W)

        # Add Right Click Pop Up Menu
        self.my_popup_menu = Menu(self.root, tearoff=False)
        # Insert, Search, Update and Delete
        self.my_popup_menu.add_command(label="Insert", command=lambda: self.new_window(WinAdjusterInsert, self.user_oid))
        self.my_popup_menu.add_command(label="Search", command=lambda: self.new_window(WinAdjusterSearch, self.user_oid))
        self.my_popup_menu.add_command(label="Update", command=lambda: self.new_window(WinAdjusterUpdate, self.user_oid))
        self.my_popup_menu.add_command(label="Delete", command=lambda: self.new_window(WinAdjusterDelete, self.user_oid))
        self.my_popup_menu.add_separator()

        # Back and Exit
        self.my_popup_menu.add_command(label="Back", command=lambda: self.new_window(Home.WinHome, self.user_oid))

        # Binding the Right click Pop Up Menu
        self.root.bind("<Button-3>", self.my_popup)

        try:
            # Finding Username for our Status Bar
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

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

    def new_window(self, _class, oid):
        level = Tk()
        _class(level, oid)
        self.root.destroy()

##################################################################################################################


# Window for Inserting into Adjuster Table
class WinAdjusterInsert:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Adjuster Insert Window")
        self.root.geometry("390x320+440+150")
        self.root.resizable(width=False, height=False)

        # All Entry Boxes
        self.adjuster_id = Entry(self.root, width=20, font=('Helvetica', 15))
        self.adjuster_id.grid(row=0, column=1, pady=(20, 8), padx=(20, 0))
        self.first_name = Entry(self.root, width=20, font=('Helvetica', 15))
        self.first_name.grid(row=1, column=1, pady=8, padx=(20, 0))
        self.last_name = Entry(self.root, width=20, font=('Helvetica', 15))
        self.last_name.grid(row=2, column=1, pady=8, padx=(20, 0))
        self.expertise = Entry(self.root, width=20, font=('Helvetica', 15))
        self.expertise.grid(row=3, column=1, pady=8, padx=(20, 0))
        self.email_id = Entry(self.root, width=20, font=('Helvetica', 15))
        self.email_id.grid(row=4, column=1, pady=8, padx=(20, 0))

        # All Labels
        self.adjuster_id_label = Label(self.root, text="Adjuster ID:", font=('Helvetica', 15))
        self.adjuster_id_label.grid(row=0, column=0, padx=(16, 0), pady=(20, 8), sticky=E)
        self.first_name_label = Label(self.root, text="First Name:", font=('Helvetica', 15))
        self.first_name_label.grid(row=1, column=0, padx=(16, 0), pady=8, sticky=E)
        self.last_name_label = Label(self.root, text="Last Name:", font=('Helvetica', 15))
        self.last_name_label.grid(row=2, column=0, padx=(16, 0), pady=8, sticky=E)
        self.expertise_label = Label(self.root, text="Expertise:", font=('Helvetica', 15))
        self.expertise_label.grid(row=3, column=0, padx=(16, 0), pady=8, sticky=E)
        self.email_id_label = Label(self.root, text="Email:", font=('Helvetica', 15))
        self.email_id_label.grid(row=4, column=0, padx=(16, 0), pady=8, sticky=E)

        # Back and Submit Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=5, column=0, pady=10, columnspan=2)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11),
                                  command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 40), ipadx=5)

        # Submit Button
        self.submit_button = Button(self.button_frame, text="Submit", bg="#90EE90", font=('Helvetica', 11),
                                    command=self.submit)
        self.submit_button.grid(row=0, column=1, pady=20, padx=(30, 0), ipadx=5)

    def submit(self):
        # if any entry not filled then warning message displayed
        if self.adjuster_id.get() == '' or self.first_name.get() == '' or self.last_name.get() == '' or \
                self.expertise.get() == '' or self.email_id.get() == '':
            messagebox.showwarning(
                "Warning", "Please Fill The Details!", parent=self.root)
        else:
            # Check whether valid email was provided
            if '@' not in self.email_id.get() or '.' not in self.email_id.get():
                messagebox.showwarning("Warning", "Please provide a valid email!", parent=self.root)
                return

            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Default values when inserting
                status = "Idle"
                nfixes = 0

                query = '''Insert Into Adjusters(Adjuster_ID, First_Name, Last_Name, Expertise, Email_id, Status, nFixes) 
                           values(?, ?, ?, ?, ?, ?, ?)'''

                c.execute(query, (self.adjuster_id.get(), self.first_name.get(), self.last_name.get(),
                                  self.expertise.get(), self.email_id.get(), status, nfixes))

                # Clearing the originally filled values
                self.adjuster_id.delete(0, END)
                self.first_name.delete(0, END)
                self.last_name.delete(0, END)
                self.expertise.delete(0, END)
                self.email_id.delete(0, END)

                # Displaying info for successfully insertion
                messagebox.showinfo("Information", "Successfully Inserted", parent=self.root)

                conn.commit()
                conn.close()

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Adjuster_ID Already Taken!\nPlease Enter Other ID", parent=self.root)
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinAdjuster(level, self.user_oid)
        self.root.destroy()

##################################################################################################################


# Window for Searching the Adjuster Table
class WinAdjusterSearch:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Adjuster Search Window")
        self.root.geometry("584x430+365+100")
        self.root.resizable(width=False, height=False)

        # Our Search Label and Search Entry
        self.search_label = Label(self.root, text="Search:", anchor=E, font=('Helvetica', 15))
        self.search_label.grid(row=0, column=0, padx=(5, 0), pady=20)
        self.search_Entry = Entry(self.root, width=15, font=('Helvetica', 15))
        self.search_Entry.grid(row=0, column=1, padx=(0, 20), pady=20)

        # Drop Down Box for Search Type
        self.drop = ttk.Combobox(self.root,
                                 values=['Search by...', 'OID', 'Adjuster_ID', 'First_Name', 'Last_Name', 'Expertise',
                                         'Email_id', 'Status', 'nFixes'],
                                 font=('Helvetica', 11))
        self.drop.current(0)
        self.drop.grid(row=0, column=2, padx=(0, 27))

        # Buttons (Back, Show, Show_All)
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11),
                                  command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(55, 0), pady=15, ipadx=5)
        self.search_button = Button(self.root, text="Search", bg="#90EE90", font=('Helvetica', 11),
                                    command=lambda: self.show(1))
        self.search_button.grid(row=1, column=1, pady=15, ipadx=5)
        self.show_all_button = Button(self.root, text="Show All", bg="orange", font=('Helvetica', 11),
                                      command=lambda: self.show(0))
        self.show_all_button.grid(row=1, column=2, padx=(15, 20), pady=15, ipadx=5)

        # Add some style
        self.style = ttk.Style(self.root)
        # Pick a theme
        self.style.theme_use("vista")
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#E3E3E3")

        self.style.map('Treeview',
                       background=[('selected', 'yellow')],
                       foreground=[('selected', 'black')])

        # Create TreeView Frame
        self.tree_frame = Frame(self.root)
        self.tree_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=15)

        # TreeView ScrollBar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create TreeView
        self.my_tree = ttk.Treeview(
            self.tree_frame, height=7, yscrollcommand=self.tree_scroll.set)
        self.my_tree.pack()

        # Configure ScrollBar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our columns
        self.my_tree['columns'] = ("OID", "Adjuster_ID", "First_Name", "Last_Name",
                                   "Expertise", "Email_ID", "Status", "nFixes")

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("OID", anchor=CENTER, width=30)
        self.my_tree.column("Adjuster_ID", anchor=CENTER, width=70)
        self.my_tree.column("First_Name", anchor=CENTER, width=75)
        self.my_tree.column("Last_Name", anchor=CENTER, width=75)
        self.my_tree.column("Expertise", anchor=CENTER, width=65)
        self.my_tree.column("Email_ID", anchor=CENTER, width=120)
        self.my_tree.column("Status", anchor=CENTER, width=50)
        self.my_tree.column("nFixes", anchor=CENTER, width=50)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("OID", text="OID", anchor=CENTER)
        self.my_tree.heading("Adjuster_ID", text="Adjuster_ID", anchor=CENTER)
        self.my_tree.heading("First_Name", text="First Name", anchor=CENTER)
        self.my_tree.heading("Last_Name", text="Last Name", anchor=CENTER)
        self.my_tree.heading("Expertise", text="Expertise", anchor=CENTER)
        self.my_tree.heading("Email_ID", text="Email_ID", anchor=CENTER)
        self.my_tree.heading("Status", text="Status", anchor=CENTER)
        self.my_tree.heading("nFixes", text="nFixes", anchor=CENTER)

        # Count Variable for number of records
        self.count = 0

        # Create Stripped row Tags
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

        # Change_Status Button
        self.change_status_button = Button(self.root, text="Change Status", bg="#f2f547", font=('Helvetica', 11),
                                           command=self.change_status)
        self.change_status_button.grid(row=3, column=0, columnspan=3, pady=(5, 0), ipadx=5)

        self.machine_failure_list = self.find_machine_failures()

        # Loading the Environment Variables from .env file
        env_path = Path(env_file_path)
        load_dotenv(dotenv_path=env_path)

        self.EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # Function for finding Machines which have already failed
    def find_machine_failures(self):
        try:
            # This will put Failed machines inside a list
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # Query for selecting Machines that has failed
            # Info like: 'OID', 'Machine_ID' and 'Machine_Type' are collected
            q = "Select OID, Machine_ID, Machine_Type from Machines where Status=?"
            c.execute(q, ("Failure",))
            machine_failure_list = c.fetchall()

            conn.commit()
            conn.close()

            return machine_failure_list

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!", parent=self.root)
            return []

    def send_mail(self, email, machine_id):
        # code for sending mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)

            # Subject and Body
            subject = 'Machine Fixing Duty: Factory Simulation Software'
            body = f'Dear Adjuster\n\nPlease find the Machine_ID which you need to fix\n\nMachine ID: {machine_id}'

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(self.EMAIL_ADDRESS, email, msg)

    def change_status(self):
        if self.my_tree.selection():
            # Grab the Record number
            selected = self.my_tree.focus()
            # Grab the values of the record
            values = self.my_tree.item(selected, "values")

            # Finding the OID, nFixes and Adjuster_ID value for that record
            oid = values[0]
            adjuster_id = values[1]
            num_fixes = int(values[7])

            # Adjuster is Idle
            if values[6] == "Idle":
                # Asking for confirmation whether user wants to change status or not
                user_ans = messagebox.askyesno(
                    "Confirmation", "Do you want to Change Status?\nIt will take some time please be patient!",
                    parent=self.root)
                # If User pressed 'No' nothing will happen
                if not user_ans:
                    return

                for machine in self.machine_failure_list:
                    # Machine Type == Adjuster Expertise
                    if machine[2] == values[4]:
                        # Finding Machine_ID for which Adjuster Expertise matched
                        machine_id = self.machine_failure_list.pop(
                            self.machine_failure_list.index(machine))[1]
                        status = "Busy"

                        try:
                            conn = sqlite3.connect(database_file_path)
                            c = conn.cursor()

                            # Adjuster status becomes busy
                            query = "Update Adjusters set Status=? where OID=?"
                            c.execute(query, (status, oid))

                            # Finding email of the Adjuster
                            query = "Select Email_id from Adjusters where OID=?"
                            c.execute(query, oid)
                            email = c.fetchone()[0]

                            # Machine status becomes U/M
                            query = "Update Machines set Status=? where Machine_ID=?"
                            c.execute(query, ("U/M", machine_id))

                            # Entry made to Maintenance table
                            query = "Insert Into Maintenance(Machine_ID, Adjuster_ID) values(?, ?)"
                            c.execute(query, (machine_id, adjuster_id))

                            # Sending Mail
                            self.send_mail(email, machine_id)

                            # Message to inform that Email has been sent
                            messagebox.showinfo(
                                "Information", "Mail has been sent Successfully:)", parent=self.root)

                            conn.commit()
                            conn.close()

                            # Update the Treeview
                            self.my_tree.item(selected, text="", values=(values[0], values[1], values[2], values[3],
                                                                         values[4], values[5], status, values[7]))

                        except sqlite3.OperationalError:
                            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

            # Adjuster is Busy
            else:
                # Asking for confirmation whether user wants to change status or not
                user_ans = messagebox.askyesno(
                    "Confirmation", "Do you want to Change Status?", parent=self.root)
                # If User pressed 'No' nothing will happen
                if not user_ans:
                    return

                status = "Idle"

                try:
                    conn = sqlite3.connect(database_file_path)
                    c = conn.cursor()

                    num_fixes += 1
                    # Making Status of the Adjuster "Idle" and also updating nFixes
                    query = "Update Adjusters set Status=?, nFixes=? where OID=?"
                    c.execute(query, (status, num_fixes, oid))

                    # Finding corresponding Machine_ID for Adjuster_ID
                    query = "Select Machine_ID from Maintenance where Adjuster_ID=?"
                    c.execute(query, (adjuster_id,))
                    machine_id = c.fetchone()[0]

                    # Deleting the record from Maintenance Table for given Adjuster_ID
                    query = "Delete from Maintenance where Adjuster_ID=?"
                    c.execute(query, (adjuster_id,))

                    # Updating the status of Machine
                    query = "Update Machines set Status=? where Machine_ID=?"
                    c.execute(query, ("Working", machine_id))

                    conn.commit()
                    conn.close()

                    # Update the Treeview
                    self.my_tree.item(selected, text="", values=(values[0], values[1], values[2], values[3],
                                                                 values[4], values[5], status, num_fixes))

                except sqlite3.OperationalError:
                    messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def show(self, a):
        # Whether user has provided value to search_entry box and
        # User clicked search button
        if self.search_Entry.get() == "" and a == 1:
            messagebox.showwarning(
                "Warning", "Please Provide the Value to be Searched", parent=self.root)
            return

        # Whether User has chosen some Search by value
        selection = self.drop.get()
        if selection == 'Search by...' and a == 1:
            messagebox.showwarning(
                "Warning", "Please Select an Option to be Searched!!!", parent=self.root)
            return

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            # a->0 then show_all button was clicked
            # a->1 then search button was clicked
            if a == 0:
                c.execute("Select OID, * from Adjusters")
            else:
                query = "select OID, * from Adjusters where " + selection + " LIKE ?"
                value = '%' + self.search_Entry.get() + '%'
                c.execute(query, (value,))

            records = c.fetchall()

            # Removing the Preexisting Records(if any)
            for rec in self.my_tree.get_children():
                self.my_tree.delete(rec)

            # Resetting the Count
            self.count = 0

            if records:
                for record in records:
                    if self.count % 2 == 0:
                        self.my_tree.insert(
                            parent='', index='end', iid=str(self.count), text="", values=record, tags=("evenrow",))
                    else:
                        self.my_tree.insert(
                            parent='', index='end', iid=str(self.count), text="", values=record, tags=("oddrow",))
                    self.count += 1
            else:
                messagebox.showinfo("Information", "No Record Found!!!", parent=self.root)

            # Clearing the Entry Box and Resetting the Drop-Down Box
            self.search_Entry.delete(0, END)
            self.drop.current(0)

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinAdjuster(level, self.user_oid)
        self.root.destroy()

##################################################################################################################


# Window for Updating the Adjuster Table
class WinAdjusterUpdate:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Adjuster Update Window")
        self.root.geometry("390x410+440+100")
        self.root.resizable(width=False, height=False)

        # Select Label and Entry Box
        self.select_label = Label(self.root, text="Select OID:", anchor=E, font=('Helvetica', 15))
        self.select_label.grid(row=0, column=0, padx=(5, 25), pady=(20, 10), ipadx=18)
        self.select_Entry = Entry(self.root, width=15, font=('Helvetica', 15))
        self.select_Entry.grid(row=0, column=1, padx=(0, 40), pady=(20, 10))

        # Back and Show Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11),
                                  command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(90, 0), pady=(10, 30), ipadx=6)
        self.show_button = Button(self.root, text="Show", bg="orange", font=('Helvetica', 11), command=self.display)
        self.show_button.grid(row=1, column=1, padx=(0, 60), pady=(10, 30), ipadx=6)

        # Label and Entry Frame
        self.my_frame = Frame(self.root)
        self.my_frame.grid(row=2, column=0, columnspan=2)

        # All Entry Boxes
        self.adjuster_id = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.adjuster_id.grid(row=0, column=1, pady=5)
        self.first_name = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.first_name.grid(row=1, column=1, pady=5)
        self.last_name = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.last_name.grid(row=2, column=1, pady=5)
        self.expertise = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.expertise.grid(row=3, column=1, pady=5)
        self.email_id = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.email_id.grid(row=4, column=1, pady=5)

        # All Labels
        self.adjuster_id_label = Label(self.my_frame, text="Adjuster ID:", font=('Helvetica', 15))
        self.adjuster_id_label.grid(row=0, column=0, padx=(0, 20), pady=5, sticky=E)
        self.first_name_label = Label(self.my_frame, text="First Name:", font=('Helvetica', 15))
        self.first_name_label.grid(row=1, column=0, padx=(0, 20), pady=5, sticky=E)
        self.last_name_label = Label(self.my_frame, text="Last Name:", font=('Helvetica', 15))
        self.last_name_label.grid(row=2, column=0, padx=(0, 20), pady=5, sticky=E)
        self.expertise_label = Label(self.my_frame, text="Expertise:", font=('Helvetica', 15))
        self.expertise_label.grid(row=3, column=0, padx=(0, 20), pady=5, sticky=E)
        self.email_id_label = Label(self.my_frame, text="Email_ID:", font=('Helvetica', 15))
        self.email_id_label.grid(row=4, column=0, padx=(0, 20), pady=5, sticky=E)

        # Update Button
        self.update_button = Button(self.root, text="Update", bg="#90EE90", font=('Helvetica', 11), command=self.update)
        self.update_button.grid(row=3, column=0, pady=25, ipadx=10, columnspan=2)

    def display(self):
        # Clearing all the Entry Boxes
        self.adjuster_id.delete(0, END)
        self.first_name.delete(0, END)
        self.last_name.delete(0, END)
        self.expertise.delete(0, END)
        self.email_id.delete(0, END)

        # Whether User has provided value for oid
        if self.select_Entry.get() == '':
            messagebox.showwarning("Warning", "Please Select an ID!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Fetching info for a Particular Adjuster
                c.execute("Select * from Adjusters where OID=?", self.select_Entry.get())
                record = c.fetchone()

                # Checking whether record was found
                if not record:
                    messagebox.showwarning("Warning", "No Record Found!", parent=self.root)
                else:
                    # Displaying information
                    self.adjuster_id.insert(0, record[0])
                    self.first_name.insert(0, record[1])
                    self.last_name.insert(0, record[2])
                    self.expertise.insert(0, record[3])
                    self.email_id.insert(0, record[4])

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def update(self):
        # Check whether the User has provided any OID
        if self.select_Entry.get() == '':
            messagebox.showwarning(
                "Warning", "Please Select an OID!", parent=self.root)
        # Check whether all the Entry fields were filled or not
        elif self.adjuster_id.get() == '' or self.first_name.get() == '' or self.last_name.get() == '' or \
                self.expertise.get() == '' or self.email_id.get() == '':
            messagebox.showwarning("Warning", "Please Fill The Details!", parent=self.root)
        else:
            # Check whether valid email was provided
            if '@' not in self.email_id.get() or '.' not in self.email_id.get():
                messagebox.showwarning("Warning", "Please provide a valid email!", parent=self.root)
                return

            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Updating the Database with the newly provided values
                query = '''update Adjusters set Adjuster_ID = ?, First_Name = ?, Last_Name = ?, Expertise = ?, 
                           Email_id = ? where OID = ?'''
                e = (self.adjuster_id.get(), self.first_name.get(), self.last_name.get(),
                     self.expertise.get(), self.email_id.get(), self.select_Entry.get())
                c.execute(query, e)

                # Clearing our Entry Fields
                self.adjuster_id.delete(0, END)
                self.first_name.delete(0, END)
                self.last_name.delete(0, END)
                self.expertise.delete(0, END)
                self.email_id.delete(0, END)
                self.select_Entry.delete(0, END)

                # Displaying info for successfully update
                messagebox.showinfo("Information", "Successfully Updated", parent=self.root)

                conn.commit()
                conn.close()

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Adjuster_ID Already Taken!\nPlease Enter Other ID", parent=self.root)
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinAdjuster(level, self.user_oid)
        self.root.destroy()

##################################################################################################################


# Window for Deleting from Adjuster Table
class WinAdjusterDelete:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Adjuster Delete Window")
        self.root.geometry("400x160+450+150")
        self.root.resizable(width=False, height=False)

        # Select Label and Entry
        self.select_label = Label(self.root, text="Select AID:", font=('Helvetica', 15), anchor=E)
        self.select_label.grid(row=0, column=0, padx=(10, 38), pady=(20, 10), ipadx=10)
        self.select_Entry = Entry(self.root, width=17, font=('Helvetica', 15))
        self.select_Entry.grid(row=0, column=1, padx=(0, 40), pady=(20, 10))

        # Back and Delete Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11),
                                  command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(90, 0), pady=30, ipadx=10)
        self.del_button = Button(self.root, text="Delete", bg="orange", font=('Helvetica', 11),
                                 command=self.delete_record)
        self.del_button.grid(row=1, column=1, padx=(0, 50), pady=30, ipadx=10)

    def delete_record(self):
        # Checking if an OID was given
        if self.select_Entry.get() == '':
            messagebox.showwarning(
                "Warning", "Please Select an AID!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Selecting Adjuster whose OID was given
                query1 = "Select * from Adjusters where Adjuster_ID=?"
                c.execute(query1, (self.select_Entry.get(),))

                # Checking whether AID given has any Adjuster corresponding to it
                if c.fetchone() is None:
                    messagebox.showerror(
                        "Error", "No Record Found to Delete\nPlease Try Again!!!", parent=self.root)
                else:
                    # Deleting the Adjuster with corresponding AID
                    query2 = "Delete from Adjusters where Adjuster_ID=?"
                    c.execute(query2, (self.select_Entry.get(),))

                    # Clearing the Entry Box
                    self.select_Entry.delete(0, END)

                    # Displaying info for successfully deletion
                    messagebox.showinfo(
                        "Information", "Successfully Deleted", parent=self.root)

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinAdjuster(level, self.user_oid)
        self.root.destroy()
