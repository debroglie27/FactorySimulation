##################################################################################################################
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from main import database_file_path
import Home
##################################################################################################################


# Window for Maintenance Database
class WinMaintenance:

    def __init__(self, master, user_oid):
        self.root = master
        self.user_oid = user_oid
        self.root.title("Maintenance Window")
        self.root.geometry("340x275+480+150")
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
        self.my_tree = ttk.Treeview(
            self.tree_frame, height=6, yscrollcommand=self.tree_scroll.set)
        self.my_tree.pack()

        # Configure ScrollBar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define our columns
        self.my_tree['columns'] = ("OID", "Machine_ID", "Adjuster_ID")

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("OID", anchor=CENTER, width=40)
        self.my_tree.column("Machine_ID", anchor=CENTER, width=110)
        self.my_tree.column("Adjuster_ID", anchor=CENTER, width=110)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=CENTER)
        self.my_tree.heading("OID", text="OID", anchor=CENTER)
        self.my_tree.heading("Machine_ID", text="Machine_ID", anchor=CENTER)
        self.my_tree.heading("Adjuster_ID", text="Adjuster_ID", anchor=CENTER)

        # Count Variable for number of records
        self.count = 0

        # Create Stripped row Tags
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")

        try:
            conn = sqlite3.connect(database_file_path)
            c = conn.cursor()

            c.execute("Select OID, Machine_ID, Adjuster_ID from Maintenance")
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

        # Back Button
        self.back_button = Button(self.root, text="Back", bg="#add8e6", font=("Helvetica", 11), command=self.close_window)
        self.back_button.pack(pady=(25, 0), ipadx=10)

    def close_window(self):
        level = Tk()
        Home.WinHome(level, self.user_oid)
        self.root.destroy()
