from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import time
import sqlite3


class School_Portal():
    db_name = 'students.db'
    # constructor

    def __init__(self):
        self.root = root
        self.root.title('Students Record')

        # ----------------------------Logo and Title------------------------------
        # logo removed
        # ----------------------Title----------------------------
        # title removed

        # ----------------------------New Record------------------------------
        #  For Frame
        frame = LabelFrame(self.root, text='Add New Record')
        frame.grid(row=0, column=1)
        frame.config(borderwidth=3, relief=SUNKEN, padx=30, pady=5, labelanchor=N)

        #  For First name
        Label(frame, text='First name').grid(row=1, column=1, sticky=W)
        self.firstName = Entry(frame)
        self.firstName.grid(row=1, column=2, ipady=2, pady=2)
        self.firstName.config(width=30, relief=RAISED)

        #  For Last name
        Label(frame, text='Last name').grid(row=2, column=1, sticky=W)
        self.lastName = Entry(frame)
        self.lastName.grid(row=2, column=2, ipady=2, pady=2)
        self.lastName.config(width=30, relief=RAISED)

        #  For Username
        Label(frame, text='Username').grid(row=3, column=1, sticky=W)
        self.username = Entry(frame)
        self.username.grid(row=3, column=2, ipady=2, pady=2)
        self.username.config(width=30, relief=RAISED)

        #  For Email
        Label(frame, text='Email').grid(row=4, column=1, sticky=W)
        self.email = Entry(frame)
        self.email.grid(row=4, column=2, ipady=2, pady=2)
        self.email.config(width=30, relief=RAISED)

        #  For subject
        Label(frame, text='subject').grid(row=5, column=1, sticky=W)
        self.subject = Entry(frame)
        self.subject.grid(row=5, column=2, ipady=2, pady=2)
        self.subject.config(width=30, relief=RAISED)

        #  For Age
        Label(frame, text='Age').grid(row=6, column=1, sticky=W)
        self.age = Entry(frame)
        self.age.grid(row=6, column=2, ipady=2, pady=2)
        self.age.config(width=30, relief=RAISED)

        # --------------------- Add button -----------------------------
        self.addButton = ttk.Button(frame, text='Add Record', command=self.add).grid(row=7, column=2)

        # message label display'
        self.messageLabel = Label(text='')
        self.messageLabel.grid(row=8, column=1)
        self.messageLabel.config(bg='#eaeaea')

        # --------------------------Database Table Display Box-----------------------------
        self.tree = ttk.Treeview(height=10, column=['', '', '', '', '', ''])
        self.tree.grid(row=9, column=1, columnspan=5, pady=15)

        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=39, stretch=FALSE)

        self.tree.heading('#1', text='First Name')
        self.tree.column('#1', width=122)

        self.tree.heading('#2', text='Last Name')
        self.tree.column('#2', width=122)

        self.tree.heading('#3', text='Username')
        self.tree.column('#3', width=100)

        self.tree.heading('#4', text='Email')
        self.tree.column('#4', width=122)

        self.tree.heading('#5', text='Subject')
        self.tree.column('#5', width=105)

        self.tree.heading('#6', text='Age')
        self.tree.column('#6', width=39, stretch=FALSE)

        # ----------------------------------Date-------------------------------------
        def tick():
            d = datetime.datetime.now()
            # Month Day, Year
            today = '{:%B %d, %Y}'.format(d)

            # -------------------------------Time-------------------------------------
            #     %I=12hours(%H=24hours), %M=Minutes, %S=Seconds, %p=PM/AM
            mytime = time.strftime('%I:%M:%S%p')
            self.lblInfo.config(text=(mytime + '\n' + today))
            # after 200ms call the tick subject
            self.lblInfo.after(200, tick)

        self.lblInfo = Label(font=('arial', 12, 'bold'), anchor=W, justify=LEFT)
        self.lblInfo.grid(row=12, column=0, columnspan=10)
        tick()

        # -------------------------------Menu Bar-------------------------------------
        Chooser = Menu()
        itemone = Menu(tearoff=0)

        itemone.add_command(label='Add Record', command=self.add)
        itemone.add_command(label='Edit Record', command=self.edit)
        itemone.add_command(label='Delete Record', command=self.delete_record_confirm)
        itemone.add_command(label='Help', command=self.help)
        itemone.add_separator()
        itemone.add_command(label='Exit', command=self.quit_app)

        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_cascade(label='Add', command=self.add)
        Chooser.add_cascade(label='Edit', command=self.edit)
        Chooser.add_cascade(label='Delete', command=self.delete_record_confirm)
        Chooser.add_cascade(label='Help', command=self.help)
        Chooser.add_cascade(label='Exit', command=self.quit_app)

        root.config(menu=Chooser)

        # call the viewing_records subject
        self.viewing_records()

        # ---------------------------------View Database Table-----------------------------------
        # connecting to database

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # SQL
        query = 'SELECT * FROM Studentlist'
        db_table = self.run_query(query)
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:])

        #             Validation to Add New Record
    def validation(self):
        # length of firstname and lastname IS NOT EQUAL TO ZERO
        return len(self.firstName.get()) != 0 and \
               len(self.lastName.get()) != 0 and \
               len(self.username.get()) != 0 and \
               len(self.email.get()) != 0 and \
               len(self.subject.get()) != 0 and \
               len(self.age.get()) != 0

        # ------------------------------ Add Records ---------------------------------
    def add_record(self):
        if self.validation():
            # ID is autoincremented so it's null
            query = 'INSERT INTO Studentlist VALUES (NULL, ?,?,?,?,?,?)'
            parameters = (
                self.firstName.get(),
                self.lastName.get(),
                self.username.get(),
                self.email.get(),
                self.subject.get(),
                self.age.get()
            )
            self.run_query(query, parameters)
            # ---------------shows message if the new data has been added
            self.messageLabel['text'] = '{} {} added successfully'.format(self.firstName.get(), self.lastName.get()).capitalize()
            self.messageLabel.config(fg='green', font=("Arial", 13))

            # -----------To  clear the field when a new record is to be added-----------------------------
            self.firstName.delete(0, END)
            self.lastName.delete(0, END)
            self.username.delete(0, END)
            self.email.delete(0, END)
            self.subject.delete(0, END)
            self.age.delete(0, END)

        else:
            self.messageLabel['text'] = 'Please fill all fields to proceed.'
            self.messageLabel.config(fg='red', font=("Arial", 13))

        self.viewing_records()

        # ---------------------Creates Message Box to add record --------------------
    def add(self):
        ad = messagebox.askquestion('Add Record', 'Want to Add a new Record?')
        if ad == 'yes':
            self.add_record()

        # -------------------Delete record --------------------

    def delete_record(self):
        self.messageLabel['text'] = ''

        try:
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as e:
            self.messageLabel['text'] = 'Select a record to delete!'
            self.messageLabel.config(fg='red', font=("Arial", 13))
            return
        self.messageLabel['text'] = ''
        number = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Studentlist WHERE ID = ?'
        self.run_query(query, (number,))
        self.messageLabel['text'] = 'Record {} has been deleted'.format(number)

        # Then we call the table to view the record to view the record
        self.viewing_records()

        # Message box(Delete Confirmation)

    def delete_record_confirm(self):
        dRc = messagebox.askquestion('Delete Record!', 'Do you want to delete this record?')
        if dRc == 'yes':
            self.delete_record()

# ------------------------------ Edit Record ---------------------------------
    def edit_box(self):
        self.messageLabel['text'] = ''

        try:
            # tree.selection to select the item to be edited
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError as e:
            # if no item was select then 'Select a record to edit'
            self.messageLabel['text'] = 'Select a record to edit'
            self.messageLabel.config(fg='red', font=("Arial", 13))
            return

        fname = self.tree.item(self.tree.selection())['values'][0]
        lname = self.tree.item(self.tree.selection())['values'][1]
        uname = self.tree.item(self.tree.selection())['values'][2]
        email = self.tree.item(self.tree.selection())['values'][3]
        subject = self.tree.item(self.tree.selection())['values'][4]
        age = self.tree.item(self.tree.selection())['values'][5]

        # --------------- Pop-up Box for editing-----------
        self.edit_root = Toplevel()
        self.edit_root.title('Edit Record')


        Label(self.edit_root, text='Old First Name').grid(row=0, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=fname), state='readonly').grid(row=0, column=2)
        Label(self.edit_root, text='New First Name').grid(row=1, column=1, sticky=W)
        new_fname = Entry(self.edit_root)
        new_fname.grid(row=1, column=2)

        Label(self.edit_root, text='Old Last Name').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=lname), state='readonly').grid(row=2, column=2)
        Label(self.edit_root, text='New Last Name').grid(row=3, column=1, sticky=W)
        new_lname = Entry(self.edit_root)
        new_lname.grid(row=3, column=2)

        Label(self.edit_root, text='Old Username').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=uname), state='readonly').grid(row=4, column=2)
        Label(self.edit_root, text='New Username').grid(row=5, column=1, sticky=W)
        new_uname = Entry(self.edit_root)
        new_uname.grid(row=5, column=2)

        Label(self.edit_root, text='Old Email Address').grid(row=6, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=email), state='readonly').grid(row=6, column=2)
        Label(self.edit_root, text='New Email Address').grid(row=7, column=1, sticky=W)
        new_email = Entry(self.edit_root)
        new_email.grid(row=7, column=2)

        Label(self.edit_root, text='Old subject').grid(row=8, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=subject), state='readonly').grid(row=8, column=2)
        Label(self.edit_root, text='New subject').grid(row=9, column=1, sticky=W)
        new_subject = Entry(self.edit_root)
        new_subject.grid(row=9, column=2)

        Label(self.edit_root, text='Previous Age').grid(row=10, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=age), state='readonly').grid(row=10, column=2)
        Label(self.edit_root, text='New Age').grid(row=11, column=1, sticky=W)
        new_age = Entry(self.edit_root)
        new_age.grid(row=11, column=2)

        Button(self.edit_root, text='Save Changes', command=lambda: self.edit_record(new_fname.get(), fname,
                                                                                     new_lname.get(), lname,
                                                                                     new_uname.get(), uname,
                                                                                     new_email.get(), email,
                                                                                     new_subject.get(), subject,
                                                                                     new_age.get(), age
                                                                                     )).grid(row=12, column=2, sticky=W)

        self.edit_root.mainloop()

    def help(self):
        messagebox.showinfo('Info', 'Create, view, edit and delete students record.')

    def quit_app(self):
        ex = messagebox.askquestion('Exit Application!', 'Do you want to close this application?')
        if ex == 'yes':
            root.destroy()

    def edit_record(self, new_fname, fname, new_lname, lname, new_uname, uname,
                    new_email, email, new_subject, subject, new_age, age):
        query = 'UPDATE Studentlist SET First name=?,Last name=?, Username=?,Email=?, Subject=?, Age=? ' \
                'WHERE First name=? AND Last name=? AND Username=? AND Email=? AND Subject=? AND Age=?'
        parameters = (new_fname, new_lname, new_uname, new_email, new_subject, new_age,
                      fname, lname, uname, email, subject, age)
        self.run_query(query, parameters)
        # closes the popup box
        self.edit_root.destroy()

        #  --------------- message if successful ---------------
        self.messageLabel['text'] = '{} details has been changed to {}'.format(fname, new_fname)
        self.messageLabel.config(fg='green', font=("Arial", 13))

        self.viewing_records()

    def edit(self):
        ed = messagebox.askquestion('Edit Record', 'Do you want to edit this record?')
        if ed == 'yes':
            self.edit_box()


if __name__ == '__main__':
    root = Tk()
    root.iconbitmap(default="logo/student.ico")
    window_height = 500
    window_width = 653
    # specifies width and height of window1
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # specifies the co-ordinates for the screen
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    root.configure(background='#eaeaea')
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    root.resizable(False, False)  # This code helps to disable windows from resizing
    application = School_Portal()
    root.mainloop()