##################################################################################################################
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from main import database_file_path
import Home
##################################################################################################################


# Window for Machine Database
class WinMachine:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Machine Window")
        self.root.geometry("377x380+450+110")
        self.root['bg'] = "#90EE90"
        self.root.resizable(width=False, height=False)

        self.head_label = Label(self.root, text="Machine Database", fg="purple", bg='#add8e6', bd=4, relief=GROOVE,
                                font=('Monotype Corsiva', 32, "bold"))
        self.head_label.pack(pady=(0, 10), ipadx=32, ipady=5)

        # Insert Search Update Delete Buttons
        self.but_insert = Button(self.root, text="Insert", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinMachineInsert, self.user_oid))
        self.but_insert.pack(pady=(15, 0), ipadx=35)
        self.but_search = Button(self.root, text="Search", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinMachineSearch, self.user_oid))
        self.but_search.pack(pady=(20, 0), ipadx=29)
        self.but_update = Button(self.root, text="Update", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinMachineUpdate, self.user_oid))
        self.but_update.pack(pady=(20, 0), ipadx=29)
        self.but_delete = Button(self.root, text="Delete", font=('Helvetica', 15), bg='#fdebd0',
                                 command=lambda: self.new_window(WinMachineDelete, self.user_oid))
        self.but_delete.pack(pady=(20, 0), ipadx=32)

        # Back Button
        self.but_back = Button(self.root, text="Back", font=('Helvetica', 10), bg="#add8e6",
                               command=lambda: self.new_window(Home.WinHome, self.user_oid))
        self.but_back.pack(pady=(10, 0), padx=(5, 0), ipadx=5, anchor=W)

        # Add Right Click Pop Up Menu
        self.my_popup_menu = Menu(self.root, tearoff=False)
        # Insert, Search, Update and Delete
        self.my_popup_menu.add_command(label="Insert",
                                       command=lambda: self.new_window(WinMachineInsert, self.user_oid))
        self.my_popup_menu.add_command(label="Search",
                                       command=lambda: self.new_window(WinMachineSearch, self.user_oid))
        self.my_popup_menu.add_command(label="Update",
                                       command=lambda: self.new_window(WinMachineUpdate, self.user_oid))
        self.my_popup_menu.add_command(label="Delete",
                                       command=lambda: self.new_window(WinMachineDelete, self.user_oid))
        self.my_popup_menu.add_separator()

        # Back
        self.my_popup_menu.add_command(label="Back", command=lambda: self.new_window(
            Home.WinHome, self.user_oid))

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


# Window for Inserting into Machine Table
class WinMachineInsert:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Machine Insert Window")
        self.root.geometry("420x235+440+150")
        self.root.resizable(width=False, height=False)

        # All Entry Boxes
        self.machine_id = Entry(self.root, width=20, font=('Helvetica', 15))
        self.machine_id.grid(row=0, column=1, pady=(20, 8), padx=(20, 0))
        self.machine_type = Entry(self.root, width=20, font=('Helvetica', 15))
        self.machine_type.grid(row=1, column=1, pady=8, padx=(20, 0))
        self.mttf = Entry(self.root, width=20, font=('Helvetica', 15))
        self.mttf.grid(row=2, column=1, pady=8, padx=(20, 0))

        # All Labels
        self.machine_id_label = Label(self.root, text="Machine ID:", font=('Helvetica', 15))
        self.machine_id_label.grid(row=0, column=0, padx=(16, 0), pady=(20, 8), sticky=E)
        self.machine_type_label = Label(self.root, text="Machine Type:", font=('Helvetica', 15))
        self.machine_type_label.grid(row=1, column=0, padx=(16, 0), pady=8, sticky=E)
        self.mttf_label = Label(self.root, text="MTTF:", font=('Helvetica', 15))
        self.mttf_label.grid(row=2, column=0, padx=(16, 0), pady=8, sticky=E)

        # Back and Submit Button Frame
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=3, column=0, pady=10, columnspan=2)

        # Back Button
        self.back_button = Button(self.button_frame, text="Back", bg="#add8e6", font=("Helvetica", 11),
                                  command=self.close_window)
        self.back_button.grid(row=0, column=0, padx=(20, 40), ipadx=5)

        # Submit Button
        self.submit_button = Button(self.button_frame, text="Submit", bg="#90EE90", font=('Helvetica', 11),
                                    command=self.submit)
        self.submit_button.grid(row=0, column=1, pady=20, padx=(30, 0), ipadx=5)

    def submit(self):
        # If any of the entry boxes not filled then warning message shown
        if self.machine_id.get() == '' or self.machine_type.get() == '' or self.mttf.get() == '':
            messagebox.showwarning("Warning", "Please Fill ALL The Details!", parent=self.root)
        else:
            # Check whether mttf was provided as a Real Number
            try:
                float(self.mttf.get())
            except ValueError:
                messagebox.showwarning("Warning", "MTTF should be a Real Number!", parent=self.root)
                return

            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Default values when inserting
                status = "Working"
                nfails = 0

                query = "Insert Into Machines(Machine_ID, Machine_Type, MTTF, Status, nFails) values(?, ?, ?, ?, ?)"

                c.execute(query, (self.machine_id.get(), self.machine_type.get(), self.mttf.get(), status, nfails))

                # Clearing the originally filled values
                self.machine_id.delete(0, END)
                self.machine_type.delete(0, END)
                self.mttf.delete(0, END)

                # Displaying confirmation message informing Successful Insertion
                messagebox.showinfo("Information", "Successfully Inserted", parent=self.root)

                conn.commit()
                conn.close()

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Machine_ID Already Taken!\nPlease Enter Other ID", parent=self.root)
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinMachine(level, self.user_oid)
        self.root.destroy()

##################################################################################################################


# Window for Searching the Machine Table
class WinMachineSearch:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Machine Search Window")
        self.root.geometry("510x430+400+100")
        self.root.resizable(width=False, height=False)

        # Our Search Label and Search Entry
        self.search_label = Label(self.root, text="Search:", anchor=E, font=('Helvetica', 15))
        self.search_label.grid(row=0, column=0, padx=(5, 0), pady=20)
        self.search_Entry = Entry(self.root, width=15, font=('Helvetica', 15))
        self.search_Entry.grid(row=0, column=1, padx=(0, 20), pady=20)

        # Drop Down Box for Search Type
        self.drop = ttk.Combobox(self.root,
                                 values=['Search by...', 'OID', 'Machine_ID', 'Machine_Type', 'MTTF', 'Status', "nFails"],
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
        self.tree_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=10)

        # TreeView ScrollBar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create TreeView
        self.my_tree = ttk.Treeview(self.tree_frame, height=7, yscrollcommand=self.tree_scroll.set)
        self.my_tree.pack()

        # Configure ScrollBar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our columns
        self.my_tree['columns'] = ("OID", "Machine_ID", "Machine_Type", "MTTF", "Status", "nFails")

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("OID", anchor=CENTER, width=30)
        self.my_tree.column("Machine_ID", anchor=CENTER, width=80)
        self.my_tree.column("Machine_Type", anchor=CENTER, width=120)
        self.my_tree.column("MTTF", anchor=CENTER, width=70)
        self.my_tree.column("Status", anchor=CENTER, width=80)
        self.my_tree.column("nFails", anchor=CENTER, width=50)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("OID", text="OID", anchor=CENTER)
        self.my_tree.heading("Machine_ID", text="Machine_ID", anchor=CENTER)
        self.my_tree.heading("Machine_Type", text="Machine_Type", anchor=CENTER)
        self.my_tree.heading("MTTF", text="MTTF", anchor=CENTER)
        self.my_tree.heading("Status", text="Status", anchor=CENTER)
        self.my_tree.heading("nFails", text="nFails", anchor=CENTER)

        # Count Variable for number of records
        self.count = 0

        # Create Stripped row Tags
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

        # Change Status Button
        self.change_status_button = Button(self.root, text="Change Status", bg="#f2f547", font=('Helvetica', 11),
                                           command=self.change_status)
        self.change_status_button.grid(row=3, column=0, columnspan=3, pady=(5, 0), ipadx=5)

        self.machine_failure_list = self.find_machine_failures()

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

    def change_status(self):
        if self.my_tree.selection():
            # Grab the Record number
            selected = self.my_tree.focus()
            # Grab the values of the record
            values = self.my_tree.item(selected, "values")

            # Finding the OID and nFails value for that record
            oid = values[0]
            nfails = int(values[5])

            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                if values[4] == "U/M":
                    return
                else:
                    # Asking for confirmation whether user wants to change status or not
                    user_ans = messagebox.askyesno(
                                    "Confirmation", "Do you want to Change Status?", parent=self.root)
                    # If User pressed 'No' nothing will happen
                    if not user_ans:
                        return

                    if values[4] == "Working":
                        status = "Failure"
                        nfails += 1

                        query = "Select OID, Machine_ID, Machine_Type from Machines where OID = ?"
                        c.execute(query, (oid,))
                        self.machine_failure_list.append(c.fetchone())
                    else:
                        status = "Working"
                        nfails -= 1

                        query = "Select OID, Machine_ID, Machine_Type from Machines where OID = ?"
                        c.execute(query, (oid,))
                        self.machine_failure_list.pop(self.machine_failure_list.index(c.fetchone()))

                # Updating Machine status and nFails
                query = "Update Machines set Status=?, nFails=? where OID=?"
                c.execute(query, (status, nfails, oid))

                # Update the Treeview
                self.my_tree.item(selected, text="", values=(values[0], values[1], values[2], values[3], status, nfails))

                conn.commit()
                conn.close()

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
                c.execute("Select OID, * from Machines")
            else:
                query = "select OID, * from Machines where " + selection + " LIKE ?"
                value = '%' + self.search_Entry.get() + '%'
                c.execute(query, (value,))

            records = c.fetchall()

            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)
            return

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
            messagebox.showinfo(
                "Information", "No Record Found!!!", parent=self.root)

        # Clearing the Entry Box and Resetting the Drop-Down Box
        self.search_Entry.delete(0, END)
        self.drop.current(0)

    def close_window(self):
        level = Tk()
        WinMachine(level, self.user_oid)
        self.root.destroy()

##################################################################################################################


# Window for Updating the Machine Table
class WinMachineUpdate:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Machine Update Window")
        self.root.geometry("400x330+440+120")
        self.root.resizable(width=False, height=False)

        # Select Label and Entry Box
        self.select_label = Label(
            self.root, text="Select OID:", anchor=E, font=('Helvetica', 15))
        self.select_label.grid(row=0, column=0, padx=(
            5, 25), pady=(20, 10), ipadx=18)
        self.select_Entry = Entry(self.root, width=15, font=('Helvetica', 15))
        self.select_Entry.grid(row=0, column=1, padx=(0, 40), pady=(20, 10))

        # Back and Show Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(
            90, 0), pady=(10, 30), ipadx=6)
        self.show_button = Button(self.root, text="Show", bg="orange", font=('Helvetica', 11), command=self.display)
        self.show_button.grid(row=1, column=1, padx=(
            0, 60), pady=(10, 30), ipadx=6)

        # Label and Entry Frame
        self.my_frame = Frame(self.root)
        self.my_frame.grid(row=2, column=0, columnspan=2)

        # All Entry Boxes
        self.machine_id = Entry(self.my_frame, width=20,
                                font=('Helvetica', 15))
        self.machine_id.grid(row=0, column=1, pady=5)
        self.machine_type = Entry(
            self.my_frame, width=20, font=('Helvetica', 15))
        self.machine_type.grid(row=1, column=1, pady=5)
        self.mttf = Entry(self.my_frame, width=20, font=('Helvetica', 15))
        self.mttf.grid(row=2, column=1, pady=5)

        # All Labels
        self.machine_id_label = Label(self.my_frame, text="Machine ID:", font=('Helvetica', 15))
        self.machine_id_label.grid(row=0, column=0, padx=(7, 20), pady=5, sticky=E)
        self.machine_type_label = Label(self.my_frame, text="Machine Type:", font=('Helvetica', 15))
        self.machine_type_label.grid(row=1, column=0, padx=(7, 20), pady=5, sticky=E)
        self.mttf_label = Label(self.my_frame, text="MTTF:", font=('Helvetica', 15))
        self.mttf_label.grid(row=2, column=0, padx=(7, 20), pady=5, sticky=E)

        # Update Button
        self.update_button = Button(self.root, text="Update", bg="#90EE90", font=('Helvetica', 11), command=self.update)
        self.update_button.grid(row=3, column=0, pady=25, ipadx=10, columnspan=2)

    def display(self):
        # Clearing the Entry Boxes
        self.machine_id.delete(0, END)
        self.machine_type.delete(0, END)
        self.mttf.delete(0, END)

        # Whether select_entry was filled
        if self.select_Entry.get() == '':
            messagebox.showwarning(
                "Warning", "Please Select an ID!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Fetching Machine data for corresponding OID provided
                c.execute("Select * from Machines where OID=?", self.select_Entry.get())
                record = c.fetchone()

                # Whether no record was found
                if not record:
                    messagebox.showinfo("Information", "No Record Found!", parent=self.root)
                else:
                    # Inserting the fetched data into entry boxes
                    self.machine_id.insert(0, record[0])
                    self.machine_type.insert(0, record[1])
                    self.mttf.insert(0, record[2])

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def update(self):
        if self.select_Entry.get() == '':
            messagebox.showwarning(
                "Warning", "Please Select an OID!", parent=self.root)
        elif self.machine_id.get() == self.machine_type.get() == self.mttf.get() == '':
            messagebox.showwarning(
                "Warning", "Please Fill The Details!", parent=self.root)
        else:
            # Check whether mttf was provided as a Real Number
            try:
                float(self.mttf.get())
            except ValueError:
                messagebox.showwarning("Warning", "MTTF should be a Real Number!", parent=self.root)
                return

            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                query = "update Machines set Machine_ID = ?, Machine_Type = ?, mttf = ? where OID = ?"
                e = (self.machine_id.get(), self.machine_type.get(), self.mttf.get(), self.select_Entry.get())
                c.execute(query, e)

                self.machine_id.delete(0, END)
                self.machine_type.delete(0, END)
                self.mttf.delete(0, END)
                self.select_Entry.delete(0, END)

                messagebox.showinfo(
                    "Information", "Successfully Updated", parent=self.root)

                conn.commit()
                conn.close()

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Machine_ID Already Taken!\nPlease Enter Other ID", parent=self.root)
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinMachine(level, self.user_oid)
        self.root.destroy()

##################################################################################################################


# Window for Deleting from Machine Table
class WinMachineDelete:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Machine Delete Window")
        self.root.geometry("400x160+450+150")
        self.root.resizable(width=False, height=False)

        # Select Label and Select Entry
        self.select_label = Label(self.root, text="Select MID:", font=('Helvetica', 15), anchor=E)
        self.select_label.grid(row=0, column=0, padx=(10, 38), pady=(20, 10), ipadx=10)
        self.select_Entry = Entry(self.root, width=17, font=('Helvetica', 15))
        self.select_Entry.grid(row=0, column=1, padx=(0, 40), pady=(20, 10))

        # Back and Delete Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=('Helvetica', 11), command=self.close_window)
        self.back_button.grid(row=1, column=0, padx=(90, 0), pady=30, ipadx=10)
        self.del_button = Button(self.root, text="Delete", bg="orange", font=('Helvetica', 11), command=self.delete_record)
        self.del_button.grid(row=1, column=1, padx=(0, 50), pady=30, ipadx=10)

    def delete_record(self):
        # Whether value for select_entry was provided
        if self.select_Entry.get() == '':
            messagebox.showwarning(
                "Warning", "Please Select a Machine_ID!", parent=self.root)
        else:
            try:
                conn = sqlite3.connect(database_file_path)
                c = conn.cursor()

                # Fetching Machine info for corresponding Machine_ID
                query1 = "Select * from Machines where Machine_ID=?"
                c.execute(query1, (self.select_Entry.get(),))

                # Whether any record was fetched
                if c.fetchone() is None:
                    messagebox.showerror(
                        "Error", "No Record Found to Delete\nPlease Try Again!!!", parent=self.root)
                else:
                    # Deleting record for the corresponding Machine_ID
                    query2 = "Delete from Machines where Machine_ID=?"
                    c.execute(query2, (self.select_Entry.get(),))

                    # Clearing the select_entry box
                    self.select_Entry.delete(0, END)

                    # Displaying info for successful deletion
                    messagebox.showinfo(
                        "Information", "Successfully Deleted", parent=self.root)

                conn.commit()
                conn.close()

            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Please Try Again!!!", parent=self.root)

    def close_window(self):
        level = Tk()
        WinMachine(level, self.user_oid)
        self.root.destroy()
