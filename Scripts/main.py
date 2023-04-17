########################################################################################
# ********** FACTORY SIMULATION PROJECT **********
# Developed By: Arijeet De
# Last Updated: 17/04/2023
########################################################################################

from tkinter import *
import LoginSystem

########################################################################################

# conn = sqlite3.connect('../FS_database.db')
# c = conn.cursor()

# Create Table Machines
# c.execute('''Create table Machines ([Machine_ID] text PRIMARY KEY,
# [Machine_Type] text,
# [MTTF] FLOAT,
# [Status] text),
# [nFails] INTEGER''')

# Create Table Adjusters
# c.execute('''Create table Adjusters ([Adjuster_ID] text PRIMARY KEY,
# [First_Name] text,
# [Last_Name] text,
# [Expertise] text,
# [Email_id] text,
# [Status] text,
# [nFixes] INTEGER)''')

# Create Table Users
# c.execute('''Create table Users ([Username] text PRIMARY KEY,
# [Email_id] text,
# [Password] blob)''')

# Create Table Maintenance
# c.execute('''Create table Maintenance ([Machine_ID] text,
# [Adjuster_ID] text)''')

# Encryption Code
# path = Path('../.env')
# load_dotenv(dotenv_path=path)
# key = os.environ.get('ENCRYPTION_KEY')
# cipher_suite = Fernet(key)
# message = "7777"
# encMessage = cipher_suite.encrypt(message.encode())

# Decryption Code
# path = Path('../.env')
# load_dotenv(dotenv_path=path)
# key = os.environ.get('ENCRYPTION_KEY')
# cipher_suite = Fernet(key)
# query = "Select Password from Users where OID=1"
# c.execute(query)
# password = c.fetchone()[0]
# decMessage1 = cipher_suite.decrypt(password).decode()

# Insert Data values in Users
# query = "Insert Into Users(Username, Email_id, Password) values(?, ?, ?)"
# c.execute(query, ('Mrinal', 'mrinal@gmail.com', encMessage))

# Adding column to a Table
# query = "Alter table table_name add column col_name col_data_type"
# c.execute(query)

# Renaming a column
# query = "Alter table table_name rename column old_col_name to new_col_name"
# c.execute(query)

# Making the newly added column in Table filled with zeros
# query = "Update table_name set col_name=0 where exists (select oid from table_name)"
# c.execute(query)

# conn.commit()
# conn.close()

#######################################################################################
# ADMIN: Arijeet
# Secret Key: 12345

# Users = ['Arijeet', 'Aushish', 'Aravind', 'Anwesha', 'Ankit', 'Gunadeep', 'Mrinal']
# Password = ['1234', '1999', '4321', '5555', '9876', '6969', '7777']
########################################################################################


# Declaring File Paths
env_file_path = '../.env'
database_file_path = '../FS_database.db'

# Executed when file is run directly
if __name__ == "__main__":
    # Initialising the Interface
    root = Tk()

    # The First Window which appears
    LoginSystem.WinLogin(root)

    mainloop()
