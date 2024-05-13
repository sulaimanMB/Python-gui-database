from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

"""
THIS IS A GRAPHICAL USER INTERFACE MADE BY SULAIMAN MUHAMMED BELLO A STUDENT OF THE MODIBBO ADAMA UNIVERSITY YOLA,
ADAMAWA STATE NIGERIA
CONTACT ME ON +2348168181414 FOR SIMILAR PROJECTS
"""

class DatabaseHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS LAMIS_RECORD (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT,
                occupation TEXT,
                phone_number TEXT
            )
        ''')
        self.conn.commit()
    
    def get_record_id(self, fullname, occupation, phone_number):
        self.cursor.execute('''
            SELECT id FROM LAMIS_RECORD
            WHERE fullname = ? AND occupation = ? AND phone_number = ?
        ''', (fullname, occupation, phone_number))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Return the ID of the matching record
        else:
            return None  # No matching record found

    def insert_data(self, fullname, occupation, phone_number):
        self.cursor.execute('''
            INSERT INTO LAMIS_RECORD (fullname, occupation, phone_number)
            VALUES (?, ?, ?)
        ''', (fullname, occupation, phone_number))
        self.conn.commit()
        # return self.cursor.lastrowid  # Get the ID of the last inserted row

    def retrieve_data(self):
        self.cursor.execute('SELECT fullname, occupation, phone_number FROM LAMIS_RECORD')
        return self.cursor.fetchall()

    def remove_data(self, fullname, occupation, phone_number):
        self.cursor.execute('''
            DELETE FROM LAMIS_RECORD
            WHERE fullname = ? AND occupation = ? AND phone_number = ?
        ''', (fullname, occupation, phone_number))
        self.conn.commit()
    
    def update_record(self, record_id, new_fullname, new_occupation, new_phone_number):
        try:
            self.cursor.execute('''
                UPDATE LAMIS_RECORD
                SET fullname = ?, occupation = ?, phone_number = ?
                WHERE id = ?
            ''', (new_fullname, new_occupation, new_phone_number, record_id))
            self.conn.commit()
            return True  # Update successful
        except Exception as e:
            print(f"An error occurred while updating the record: {str(e)}")
            return False  # Update failed
    
    def number_of_records(self):
        self.cursor.execute("""
        SELECT COUNT(*) FROM LAMIS_RECORD
        """)
        count = self.cursor.fetchone()[0]
        return count

    def close_connection(self):
        self.conn.close()

db = DatabaseHandler('Lamis.db') #start teh database


def get_user_inputted_records():
    inputted_fullname = full_name_entry.get()
    inputted_occupation = occupation_entry.get()
    inputted_phoneNumber = phone_entry.get()

    return(inputted_fullname,inputted_occupation,inputted_phoneNumber)


def add_record_feature():
    #perform entry validation
    fullname = full_name_entry.get()
    occupation = occupation_entry.get()
    phone = phone_entry.get()

    if fullname != "" and occupation != "" and phone != "":
        if len(phone) >= 6:
            db.insert_data(fullname.title(),occupation.title(),phone)
            refresh_treeview()
            records_length()
            AddLog.record_added()
            messagebox.showinfo("success","record was added successfully")
            clearEntryFields()

         
        else:
            messagebox.showwarning("invalid input","Phone number should not be less than 6 digits")
    else:
        messagebox.showwarning("Error","input fields should not be empty")

def delete_selected_item():
    try:
        # Get a list of all selected items
        selected_items = tree.selection()

        if not selected_items:
            messagebox.showerror("Error", "Please select at least one record to delete.")
            return

        for selected_item in selected_items:
            item_values = tree.item(selected_item, 'values')
            
            # Extract values for fullname, occupation, and phone_number
            fullname, occupation, phone_number = item_values[0], item_values[1], item_values[2]
            
            # Delete the record from the database
            db.remove_data(fullname, occupation, phone_number)
            
            # Remove the item from the Treeview
            tree.delete(selected_item)
        
        # Show a success message
        records_length() 
        AddLog.record_removed()
        messagebox.showinfo("Success", "Selected records deleted successfully.")
    except Exception as e:
        # Handle exceptions gracefully
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# i havent implemented the functionality for the database yet, but i am done with the gui interface part

def clearEntryFields():
    """clear all the entry fields """
    full_name_entry.delete(0,END)
    occupation_entry.delete(0,END)
    phone_entry.delete(0,END)

def exit_command():
    """function to kill/exit the window """
    db.close_connection() # close connection to the database before exiting the application
    Tk.quit(window)
   
def modifySelected():
    # add_record_btn.config(state="disabled")
     
    selected_items = tree.selection()

    if len(selected_items) != 1:
        messagebox.showinfo("Info", "Please select exactly one record to modify.")
        return

    # Get the selected item and its values
    selected_item = selected_items[0]
    item_values = tree.item(selected_item, 'values')

    #insert this values to the entry fields so user can modify as needed
    clearEntryFields()
    full_name_entry.insert(0,item_values[0])
    occupation_entry.insert(0,item_values[1])
    phone_entry.insert(0,item_values[2])
    add_record_btn.config(state="disabled") #disable the add record button 
    UpdateRecordButton.enabled() #enable the updaterecord button using the defined class 
    records_length()

def updateRecord_feature():
    modified_fullname = full_name_entry.get()
    modified_occupation = occupation_entry.get()
    modified_phone_number = phone_entry.get()

    selected_items = tree.selection()
    selected_item = selected_items[0]
    item_values = tree.item(selected_items,'values')

    record_id = db.get_record_id(item_values[0], item_values[1], item_values[2])

    if record_id is not None:
        # Replace these with actual values
        modified_fullname = full_name_entry.get()
        modified_occupation = occupation_entry.get()
        modified_phone_number = phone_entry.get()

        if db.update_record(record_id, modified_fullname, modified_occupation, modified_phone_number):
            refresh_treeview()  # Refresh the Treeview to reflect changes
            messagebox.showinfo("Success", "Record updated successfully.")  
            AddLog.record_modified()         
            clearEntryFields() # clear input fields 
            add_record_btn.config(state="normal")
        else:
            refresh_treeview()  # Refresh the Treeview to reflect changes
            messagebox.showerror("Error", "Failed to update the record.")
            add_record_btn.config(state="normal")
            clearEntryFields() # clear input fields 

    else:
        messagebox.showerror("Error", "No matching record found.")


    # add_record_btn.grid(row=0,column=0)
    # updateRecord_btn.grid(row=1,column=0)


window = Tk()
window.title("LAMIS DATA MANAGER")
window.config(background="skyblue")



#making the gui interface 
functionality_frame = Frame(window,bd=0,background="skyblue")

full_name_label = Label(functionality_frame, text="Full name ",background="skyblue")
full_name_label.grid(row=0, column=0)

full_name_entry = Entry(functionality_frame, width=30,font=("consolas",12))
full_name_entry.grid(row=0, column=1)

occupation_label = Label(functionality_frame, text="Occupation",background="skyblue")
occupation_label.grid(row=1, column=0)

occupation_entry = Entry(functionality_frame, width=30,font=("consolas",12))
occupation_entry.grid(row=1, column=1,pady=10)

phone_label = Label(functionality_frame, text="Phone number",background="skyblue")
phone_label.grid(row=2, column=0)

phone_entry = Entry(functionality_frame, width=30,font=("consolas",12))
phone_entry.grid(row=2, column=1)

#BUTTONS FRAME
add_update_btn_frame = Frame(functionality_frame,background="skyblue")

add_record_btn = Button(add_update_btn_frame, text= "ADD RECORD",activebackground="green", bd=5, font=20,activeforeground="white",width=20,command=add_record_feature)
add_record_btn.grid(row=0, column=0, ipadx=5, ipady=10,columnspan=2,pady=5)

update_record_btn = Button(add_update_btn_frame, text= "UPDATE RECORD",activebackground="green", bd=5, font=20,activeforeground="white",width=20,command=updateRecord_feature)
update_record_btn.grid(row=1, column=0, ipadx=5, ipady=10,columnspan=2)

add_update_btn_frame.grid(row=3, column=1,pady=10)

#buttons for functionaliy

functionality_frame.grid(row=0, column=0,padx=10, pady=10)





table_frame = LabelFrame(window, font=("tahoma",12), bd=0,background="skyblue" )
# Create a Treeview widget
tree = ttk.Treeview(table_frame, show='headings')
tree["columns"] = ("FULLNAME", "OCCUPATION","PHONE NUMBER")

# Define column headings
tree.heading("FULLNAME", text="FULLNAME")
tree.heading("OCCUPATION", text="OCCUPATION")
tree.heading("PHONE NUMBER", text="PHONE NUMBER")


# Add sample data to the Treeview

# Create a vertical scrollbar
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

# Pack the Treeview and Scrollbar widgets

tree.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")

table_frame.grid(row=0,column=1, padx=10,pady=10)

def refresh_treeview():
    """refresh the whole treeview to reflect changes """
    tree.delete(*tree.get_children())  # Clear the Treeview
    data = db.retrieve_data()
    for row in data:
        tree.insert("", "end", values=row)
    # updateRecord_btn.grid(row=0,column=0)

refresh_treeview()

class UpdateRecordButton:
    def __init__(self) -> None:
        pass

    def enabled():
        update_record_btn.config(state="normal")
    
    def disabled():
        update_record_btn.config(state="disabled")



    

UpdateRecordButton.disabled() #disable update record button at the start of the program
dbStatus_frame = Frame(window, background="skyblue")
records_length_lbl = Label(dbStatus_frame,text="No. of records: ")
records_length_number = Label(dbStatus_frame, text="", foreground="red",font=("tahoma",15),bg="skyblue")

records_length_lbl.grid(row=0,column=0)
records_length_number.grid(row=0, column=1)

def records_length():
    """diplay the number of the records in the database """
    text = db.number_of_records() # get the number of records in the database
    records_length_number.configure(text=text)
    # print(db.number_of_records())
    # print(type(db.number_of_records()))

records_length()

dbStatus_frame.grid(row=1, column=1)



#remove record button
rem_exit_btn_Frame = Frame(window, background="skyblue")

remove_btn = Button(rem_exit_btn_Frame,text="REMOVE RECORD",activebackground="red", font=10,activeforeground="white",width=20,command=delete_selected_item)
remove_btn.grid(row=0, column=0, ipady=5)

modify_btn = Button(rem_exit_btn_Frame,text="MODIFY RECORD",activebackground="blue", font=10,activeforeground="white",width=20,command=modifySelected)
modify_btn.grid(row=0, column=1,padx=10, ipady=5)

exit_btn = Button(rem_exit_btn_Frame,text="EXIT",activebackground="red", font=10,activeforeground="white",width=20,command=exit_command)
exit_btn.grid(row=0, column=2, pady=10, ipady=5)

rem_exit_btn_Frame.grid(row=2, column=1)

log_field = Text(window, height=5,state="disabled",width=125)
log_field.grid(row=3, column=0, columnspan=4)

class AddLog:
    def __init__(self) -> None:
        pass

    def record_added():
        log_field.config(state="normal")
        log_field.insert(END,"A record was added\n")
        log_field.config(state="disabled")

    def record_modified():
        log_field.config(state="normal")
        log_field.insert(END,"A record was modifed\n")
        log_field.config(state="disabled")
    
    def record_removed():
        log_field.config(state="normal")
        log_field.insert(END,"A record was removed\n")
        log_field.config(state="disabled")


        



window.mainloop()