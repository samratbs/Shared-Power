#!/usr/bin/env python
import json
import datetime
from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
import os


class Login(object):
    top = Tk()  # calling Tk class of tkinter as top

    # Login Page(GUI)
    def log_in(self):
        self.top.geometry('600x701+50+50')  # size of the window
        self.top.resizable(False, False)  # removes maximize button
        self.top.title('Shared Power| Login')  # title of the screen

        # background of the login screen
        self.welcome_background = PhotoImage(file="register.png", width=600, height=701)
        self.background_label = Label(self.top, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=600, height=701)

        # Placing Labels in the GUI
        login_username = Label(Login.top, text="Username", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        login_username.place(x=100, y=100, width=200, height=40)
        login_password = Label(Login.top, text="Password", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        login_password.place(x=100, y=150, width=200, height=40)

        # taking in entries from the GUI
        self.login_username_entry = Entry(Login.top)
        self.login_username_entry.place(x=300, y=100, width=200, height=40)
        self.login_password_entry = Entry(Login.top, show='*')
        self.login_password_entry.place(x=300, y=150, width=200, height=40)

        # buttons which calls other functions to move between pages and functions.
        self.login_button = Button(Login.top, text="Sign in", font=('Verdana', 12), bg="#1c1c20", fg='yellow', command=self.sign_in)
        self.login_button.place(x=260, y=300, width=80, height=35)

        # Goes to the account registration page
        self.create_button = Button(Login.top, text="Create a new account", font=('Verdana', 12), bg="#1c1c20", fg='yellow'
                                 , command=Register().register)
        self.create_button.place(x=180, y=400, width=245, height=25)

        Login.top.mainloop()  # starts a continuous loop to keep the GUI running.

    # backend work of Login GUI.
    def sign_in(self):  # Sign in (backend)

        # opening the registration json file as read
         with open("registration.txt", 'r') as fh:
            fileDict = json.load(fh)

            # initializing the variables
            self.user_username = " "
            self.user_pass = " "

        # checking if the entered username is admin username or not
         if self.login_username_entry.get() == "admin":
             HomePage().admin("admin")  # if yes go to the admin's homepage
         else:  #if no look up the username in the database
            for data in fileDict['info']:  # loops around the json database

                # checks if the entered username is in the database
                if data['Username'] == self.login_username_entry.get():
                    self.user_username = data['Username']

                    # checks if the entered password matches the above username in the database
                    if self.login_password_entry.get() == data['Password']:
                        self.user_pass = data['Password']

            # Return error if the username and password doesn't match else go to the HomePage
            if self.user_username !=self.login_username_entry.get() or self.user_pass != self.login_password_entry.get():
                messagebox.showinfo('Error', "Invalid username or Password.")  # error message
            else:
                HomePage().welcome(self.login_username_entry.get())  # goes to the general welcome page


class Register(object):

    # Registration Page(GUI)
    def register(self):
        Login.top.withdraw()  # withdraws the Login_Page
        self.top = Toplevel()  # opens register page as top level

        self.top.geometry('600x701+50+50')  # size of the window
        self.top.title('Shared Power| Register')  # title of the window
        self.top.resizable(False, False)  # removes maximize button

        # background of the register screen
        self.welcome_background = PhotoImage(file="register.png", width=600, height=701)
        self.background_label = Label(self.top, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=600, height=701)

        # Placing Labels  in the GUI
        username = Label(self.top, text="Username:", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        username.place(x=100, y=100, width=200, height=40)

        # Taking in entries from the GUI
        self.username_entry = Entry(self.top)
        self.username_entry.place(x=300, y=100, width=200, height=40)

        # Password Label
        password_store = Label(self.top, text="Password:", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        password_store.place(x=100, y=150, width=200, height=40)

        # Password Entry
        self.password_entry = Entry(self.top, show='*')
        self.password_entry.place(x=300, y=150, width=200, height=40)

        # Email Labels
        email = Label(self.top, text="Gmail:", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        email.place(x=100, y=200, width=200, height=40)
        email_warning = Label(self.top, text="Note:Please do not write @gmail.com.", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        email_warning.place(x=100, y=250, width=400, height=30)

        # Email Entries
        self.email_entry = Entry(self.top)
        self.email_entry.place(x=300, y=200, width=200, height=40)

        # After entering data Sign Up button is clicked which then verifies registers your data.
        self.sign_up_button = Button(self.top, text="Sign Up", font=('Verdana', 12), bg="#1c1c20", fg="yellow",
                                     command=self.check_username)  # stores the input to the database
        self.sign_up_button.place(x=265, y=300, width=80, height=35)

        # Goes back to the login page
        self.back_button = Button(self.top, text="Back", font=('Verdana', 12), bg="#1c1c20", fg="yellow",
                                  command=lambda: Login.top.deiconify() or self.top.destroy())
        self.back_button.place(x=265, y=350, width=80, height=35)

    # Registers the user in database after verification
    def sign_up(self):  # registration(backend)

        self.information = " "
        # opening the json file
        with open("registration.txt", 'r') as f:
            file_data = json.load(f)

            #checking if the user has entered any data
            if self.username_entry.get() and self.password_entry.get() and self.email_entry.get():
                if file_data: #if there is data in the file

                    # appends the information in following format into the read data from json
                    file_data['info'].append(
                        {
                            "Username": self.username_entry.get(),  # stores username entered
                            "Password": self.password_entry.get(),  # store the password entered
                            "Email": self.email_entry.get() + "@gmail.com"  # stores the gmail entered and adds @gmail.com automatically.
                        }
                    )
                    messagebox.showinfo('Info', "Registration complete successfully. ")

                    # writing the read and edited data in the json file
                    with open('registration.txt', 'w') as fh:
                        json.dump(file_data, fh, indent=2)

                    # goes back to the initial Login Page and destroys the current Register Page
                    Login.top.deiconify()
                    self.top.destroy()
            # if no data is entered by the user
            else:
                messagebox.showinfo('Error', "Please fill all the boxes.")  # Error Message

    # checks if the entered username exists in the database
    def check_username(self):

        # Opens json file as read.
        with open("registration.txt", 'r') as fh:
            file_data = json.load(fh)

            # Takes in the entry from the GUI and stores the data in name_store
            name_store = self.username_entry.get()

            # loops around the database
            for data in file_data['info']:
                if name_store == data['Username']:  # checks if the entered username is in the database
                    break #if yes then break the loop to get the exact data value of the username in json file
            if name_store == data['Username']:  # rechecks the condition
                messagebox.showerror("Error", "Username already exists in the database.")  # error message
            else:
                self.sign_up()  # go to sign_up function.


class HomePage(object):

    # Welcome Page to the app
    def welcome(self, name):
        Login.top.withdraw()  # withdraws the login GUI
        self.top = Toplevel()  # opens the welcome page as TopLevel

        self.top.geometry('600x701+50+50')  # size of the window
        self.top.title('Shared Power| Welcome')  # title of the screen
        self.top.resizable(False, False)  # removes maximize button

        # background of the Welcome screen
        self.welcome_background = PhotoImage(file="welcome.png", width=600, height=701)
        self.background_label = Label(self.top, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=600, height=701)

        # button which goes to the Home Page and passes the variable name which is the username entered during login
        self.signup_button = Button(self.top, text="Continue", fg="yellow", bg="black", command=lambda:self.homepage(name),font=("Verdana", 11))
        self.signup_button.place(x=205, y=410, height=40, width=200)

    # HomePage GUI of the application
    def homepage(self, name):
        self.top.withdraw()  # withdraws the welcome page GUI
        self.top1 = Toplevel()  # opens the welcome page as TopLevel

        self.top1.geometry('1280x720+100+80')  # size of the window
        self.top1.title('Shared Power| Main Menu')  # title of the screen
        self.top1.resizable(False, False)  # removes maximize button

        # background of the HomePage
        self.welcome_background = PhotoImage(file="homepage.png", width=1280, height=720)
        self.background_label = Label(self.top1, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=1280, height=720)

        # button which directs to add tools screen.
        self.addtool = Button(self.top1, text='Add Tool', font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                              command=lambda: AddTools().add_tools(name))
        self.addtool.place(x=200, y=150, width=200, height=100)

        # button which directs to remove tools screen
        self.removetool = Button(self.top1, text='Remove tools', font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                 command=lambda: Remove().remove_tools(name))
        self.removetool.place(x=600, y=150, width=200, height=100)

        # button to search the tools
        self.searchtool = Button(self.top1, text='Search Tool', font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                 command=lambda: Search().search_bar(name))
        self.searchtool.place(x=200, y=450, width=200, height=100)

        # button which directs us to screen for returning the hired tools
        self.return_tools_button = Button(self.top1, text='Return Tool', font=('Verdana', 12), bg="#1c1c20",
                                          fg='yellow', command=lambda: Return().return_tools(name))
        self.return_tools_button.place(x=600,y=450, width=200, height=100)

        # Label of login username displayed.
        self.login_info = Label(self.top1, text = "Logged in as "+ name,font=('Verdana', 8), bg="#1c1c20", fg='yellow')
        self.login_info.place(x=1120, y=0)

        # opens the withdrawn login screen and destroys the current screen
        self.back = Button(self.top1, text="Log out", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                           command=lambda: Login().top.deiconify() or self.top1.destroy())
        self.back.place(x=1160, y=20, width=70)

        # checks if its 30th or 31st of any month
        current_date = datetime.datetime.today()  # gets current datetime
        if current_date.month != 2:  # checks to see if the month is february or not
            if current_date.day == 30 or current_date.day == 31:
                # displays the invoice button if the condition is satisfied and calls the invoice screen.
                self.invoice_tools_button = Button(self.top1, text='Invoice', font=('Verdana', 12), bg="#1c1c20",
                                               fg='yellow', command=lambda: self.show_invoice(name))
                self.invoice_tools_button.place(x=400, y=650, width=200, height=40)
        else:
            if current_date.day == 28 or current_date.day == 29:
                # displays the invoice button if the condition is satisfied and calls the invoice screen.
                self.invoice_tools_button = Button(self.top1, text='Invoice', font=('Verdana', 12), bg="#1c1c20",
                                                   fg='yellow', command=lambda: self.show_invoice(name))
                self.invoice_tools_button.place(x=400, y=650, width=200, height=40)

    # admin's HomePage GUI
    def admin(self,name):
        Login.top.withdraw()  # withdraws the login page GUI
        self.top2 = Toplevel()  # opens the welcome page as TopLevel

        self.top2.geometry('1280x720+100+80')  # size of the window
        self.top2.title('Shared Power| Admin Menu')   # title of the screen
        self.top2.resizable(False, False)  #removes maximize button

        # background of the admin HomePage
        self.welcome_background = PhotoImage(file="homepage.png", width=1280, height=720)
        self.background_label = Label(self.top2, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=1280, height=720)

        # Labels and entry of Owner's username
        self.adder_photo = Label(self.top2, text='Owner Username', font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        self.adder_photo.place(x=54, y=150, height =40)
        self.adder_photos_entry = Entry(self.top2, font=('Verdana', 12),)
        self.adder_photos_entry.place(x=200, y=150, width=200, height=40)

        # Labels and entry of Renter's username
        self.renter_photo = Label(self.top2, text='Renter Username', font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        self.renter_photo.place(x=253, y=400, height=40)
        self.renter_photos_entry = Entry(self.top2, font=('Verdana', 12) )
        self.renter_photos_entry.place(x=400, y=400, width=200, height=40)

        # Labels and entry of the Tool name
        self.tool_photo=Label(self.top2, text="Tool name", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        self.tool_photo.place(x=509,y=150, height=40)
        self.tool_photos_entry = Entry(self.top2, font=('Verdana', 12))
        self.tool_photos_entry.place(x=600, y=150, width=200, height=40)

        #User login info
        self.login_info = Label(self.top2, text="Logged in as " + name, font=('Verdana', 8), bg="#1c1c20", fg='yellow')
        self.login_info.place(x=1150, y=0)


        #Ok button redirects to admin_data function
        self.admin_ok = Button(self.top2, text="Ok", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                           command=lambda:self.owner_data(self.adder_photos_entry.get(),self.tool_photos_entry.get())
                                          or self.renter_data(self.tool_photos_entry.get(),self.renter_photos_entry.get()))
        self.admin_ok.place(x=750, y=400, width=70,height=40)

        # Destroys the Homepage and goes back to login page by opening the withdrawn page
        self.back = Button(self.top2, text="Log out", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                           command=lambda: Login().top.deiconify() or self.top2.destroy())
        self.back.place(x=1160, y=20, width=70)

    # backend of admin's homepage to open the required uploaded photo
    def owner_data(self,owner,tool):

        # only goes inside if all the entries are entered by the admin
        if self.adder_photos_entry.get() and self.tool_photos_entry.get() and self.renter_photos_entry.get():
            # loops in the Tools directory
            for f in os.listdir('./Tools'):
                if f.startswith(owner) and f.endswith(tool + '.jpg'):  # searches directory using the passed values
                    img1 = Image.open('./Tools/' + f)  # opens the selected image
                    img1.show()  # displays the opened image

        else:  #if no data is entered
            messagebox.showinfo('Info','Please fill all the required data')  #Error message

    # backend of admin's homepage to open the required rented photo
    def renter_data(self, tool, renter):

        # only goes inside if all the entries are entered by the admin
        if self.adder_photos_entry.get() and self.tool_photos_entry.get() and self.renter_photos_entry.get():
            # loops in the Return directory
            for j in os.listdir('./Return'):
                if j.startswith(renter) and j.endswith(tool + '.jpg'):  # searches directory using the passed values
                    img2 = Image.open('./Return/' + j)  # opens the selected image
                    img2.show()  # displays the opened image

    # displays the invoice at the end of month
    def show_invoice(self,name):
        self.top3 = Toplevel()  # opens invoice screen as TopLevel
        self.top3.resizable(False, False)  # removes the maximize button

        self.top3.title('Shared Power| Invoice')  # title of the screen
        self.top3.geometry('1350x800+0+0')  # size of the window

        # Labels of the title of the data to be displayed
        invoice_label= Label(self.top3,text="Invoice",font=('Verdana', 18),fg='Black')
        invoice_label.grid(row=0,column=7)
        user_name = Label(self.top3, text="Owner", font=('Verdana', 12))
        user_name.grid(row=1, column=1)
        rent_name = Label(self.top3, text="Rented by", font=('Verdana', 12))
        rent_name.grid(row=1, column=2)
        tool_name = Label(self.top3, text="Tool Name", font=('Verdana', 12))
        tool_name.grid(row=1, column=3)
        rate = Label(self.top3, text="Rate per day", font=('Verdana', 12))
        rate.grid(row=1, column=4)
        rate_half = Label(self.top3, text="Rate per half day", font=('Verdana', 12))
        rate_half.grid(row=1, column=5)
        book_date1 = Label(self.top3, text="Booked Date", font=('Verdana', 12))
        book_date1.grid(row=1, column=6)
        days = Label(self.top3, text="Days hired", font=('Verdana', 12))
        days.grid(row=1, column=7)
        dispatch_status = Label(self.top3, text="Hired Dispatched?", font=('Verdana', 12))
        dispatch_status.grid(row=1, column=8)
        dispatch_amt = Label(self.top3, text="Dispatch amount", font=('Verdana', 12))
        dispatch_amt.grid(row=1, column=9)
        fined_status = Label(self.top3, text="Fined?", font=('Verdana', 12))
        fined_status.grid(row=1, column=10)
        fined_amt = Label(self.top3, text="Amount fined", font=('Verdana', 12))
        fined_amt.grid(row=1, column=11)
        total_cost = Label(self.top3, text="Total cost", font=('Verdana', 12))
        total_cost.grid(row=1, column=12)

        # opens the transaction json file
        with open('transactions.json') as f:
            tools_data = json.load(f)
            data = tools_data['transaction']

        count = 2  # initializing count

        # loops around the opened json file
        for keys in data:

            # displays the data in file if the renter value of the file is the entered username
            if keys['renter'] == name:

                # labels of data from file which is placed in different row and column according to the title above
                username_label = Label(self.top3, text=keys['owner'], font=('Verdana', 12))
                username_label.grid(row=count, column=1)
                renter_name_label = Label(self.top3, text=keys['renter'], font=('Verdana', 12), bg="black",
                                       fg='yellow')
                renter_name_label.grid(row=count, column=2)
                tool_label = Label(self.top3, text=keys['tool_name'], font=('Verdana', 12))
                tool_label.grid(row=count, column=3)
                pday_rate_label = Label(self.top3, text=keys['per_day_rate'], font=('Verdana', 12))
                pday_rate_label.grid(row=count, column=4)
                hday_rate_label = Label(self.top3, text=keys['half_day_rate'], font=('Verdana', 12))
                hday_rate_label.grid(row=count, column=5)
                booked_date_label = Label(self.top3, text=keys['booked_date'], font=('Verdana', 12),)
                booked_date_label.grid(row=count, column=6)
                days_label = Label(self.top3, text=keys['days_owned'], font=('Verdana', 12))
                days_label.grid(row=count, column=7)
                hire_status_label = Label(self.top3, text=keys['dispatch_hire_status'], font=('Verdana', 12))
                hire_status_label.grid(row=count, column=8)
                hire_label = Label(self.top3, text=keys['hire_charge'], font=('Verdana', 12))
                hire_label.grid(row=count, column=9)
                fine_status_label = Label(self.top3, text=keys['fine_status'], font=('Verdana', 12))
                fine_status_label.grid(row=count, column=10)
                fine_cost_label = Label(self.top3, text=keys['fine_cost'], font=('Verdana', 12))
                fine_cost_label.grid(row=count, column=11)
                cost_label = Label(self.top3, text=keys['total_cost'], font=('Verdana', 12))
                cost_label.grid(row=count, column=12)
                count = count + 1  # places every read data in a new row


class AddTools(object):

    # GUI of adding tools
    def add_tools(self, name):
        self.top = Toplevel()  # opens the Add tools page as TopLevel
        self.top.title('Shared Power| Add Tools')  # title of the screen
        self.top.geometry('600x701+200+50')  # size of the window
        self.top.resizable(False, False)  # removes maximize button

        # background for the add tools GUI
        self.welcome_background = PhotoImage(file="login.png", width=600, height=701)
        self.background_label = Label(self.top, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=600, height=701)

        # Label and entry box for the toolname
        self.tool_name = Label(self.top, text="Tool name :", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        self.tool_name.place(x=100, y=80, width=200, height=40)
        self.toolname_entry = Entry(self.top)
        self.toolname_entry.place(x=300, y=80, width=200, height=40)

        # Label and entry box for the toolcondition
        self.tool_condition = Label(self.top, text="Tool Condition :", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        self.tool_condition.place(x=100, y=170, width=200, height=40)
        self.toolname_condition = Entry(self.top)
        self.toolname_condition.place(x=300, y=170, width=200, height=40)

        #Rate per day and half day rate entry boxes and labels.
        self.rateperday = Label(self.top, text="Rate per day :", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        self.rateperday.place(x=100, y=450, width=200, height=40)
        self.rateperday_entry = Entry(self.top)
        self.rateperday_entry.place(x=300, y=450, width=200, height=40)
        self.rateperhalfday = Label(self.top, text="Rate per half day :", font=('Verdana', 12), bg="#1c1c20",
                                    fg='yellow')
        self.rateperhalfday.place(x=100, y=500, width=200, height=40)
        self.rateperhalfday_entry = Entry(self.top)
        self.rateperhalfday_entry.place(x=300, y=500, width=200, height=40)

        #Okay button which calls the backend of adding the tools
        self.okay_button = Button(self.top, text="OK", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                  command=lambda: self.tools_add(name))
        self.okay_button.place(x=250, y=550, width=80, height=30)

        #Adds photos
        self.browse_button =Button(self.top, text ="Add Pic", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                   command=lambda:self.browse_photos(name))
        self.browse_button.place(x=350, y=550, width=100, height=25)

        #Back button to exit the current window
        self.addtools_back_button = Button(self.top, text="Quit", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                           command=lambda: self.top.destroy())
        self.addtools_back_button.place(x=250, y=600, width=80, height=30)

    #backend of adding tools
    def tools_add(self, name):  # Add tools(backend)

        #open tools.json file as read
        with open('tools.json', 'r') as f:
            tools_data = json.load(f)
            current_date = datetime.date.today()  # current date
            str_date = datetime.datetime.strftime(current_date, '%Y/%m/%d')  # convert today's day into string
            # checks in data is entered the entry boxes above
            if self.toolname_entry.get() and self.rateperday_entry.get() and self.rateperhalfday_entry.get():
                try: # exception handling to check the the rates are in numbers
                    if float(self.rateperday_entry.get()) and float(self.rateperhalfday_entry.get()):
                        # append the following data in the read file
                        tools_data['tools'].append({
                            "adder_username": name,
                            "renter_username": " ",
                            "tool_name": self.toolname_entry.get(),
                            "rent_status": "no",
                            "added_date": str_date,
                            "booked_date": " ",
                            "per_day_rate": self.rateperday_entry.get(),
                            "half_day_rate": self.rateperhalfday_entry.get(),
                            "tools_condition":self.toolname_condition.get(),
                        })
                        messagebox.showinfo('Info', "Your tool has been added. ")
                        self.top.destroy() #destroy the add tool GUI
                except:
                    messagebox.showerror('Error', "The rates have to be numbers ") #Error Message
            else:
                messagebox.showwarning('Error', "Fill all the required data ")
        # open the json file as write
        with open('tools.json', 'w') as fh:
            json.dump(tools_data, fh, indent=2)  # write the edited data in the opened file.

    #renames and stores the added photos in a directory
    def browse_photos(self,name):
        browse = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                             filetype=(("jpeg", "*.jpg"), ("png", "*.png*")))  # select a photo
        image1=Image.open(browse) #opens a photo
        image1.save('Tools/{} owner tool {}.jpg'.format(name, self.toolname_entry.get())) # renames and saves the photo in the given folder
        self.browse_button.destroy()  # removes the browse button after adding photo

        # places the photo's name as label instead of button
        self.label=Label(self.top, text=" ",font=('Verdana', 8), bg="#1c1c20", fg='yellow')
        self.label.place(x=350, y=550)
        self.label.configure(text= browse)


class Search(object):

    # GUI implementation of title column of the search window
    def search_grid(self, top):
        self.top = top  # set the toplevel variable as top from another module

        # Label to display the given title in the window.
        user_name = Label(self.top, text="Owner", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        user_name.grid(row=0, column=0)
        tool_name = Label(self.top, text="Tool Name", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        tool_name.grid(row=0, column=1)
        rate = Label(self.top, text="Rate per day", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        rate.grid(row=0, column=2)
        rateh = Label(self.top, text="Rate per half day", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        rateh.grid(row=0, column=3)
        date1 = Label(self.top, text="Date Added", font=('Verdana', 12), bg="#1c1c20", fg='yellow')
        date1.grid(row=0, column=4)

        self.top.configure(background="black")  # set background as black

    # GUI implementation of search data
    def search_bar(self, name):
        self.top1 = Toplevel()  # open the search window as top level
        self.top1.title('Shared Power| Search Tools')  # title of the window
        self.top1.resizable(False, False)  #removes the maximize button

        #opens the tools.json file as read
        with open('tools.json') as f:
            tools_data = json.load(f)
            data = tools_data['tools']

        length = len(data)  # finds length of the data inside the json dictionary
        yscrollbar = Scrollbar(self.top1, orient=VERTICAL)  #sets the scrollbar for vertical

        # Create a tree view widget
        self.tv = ttk.Treeview(
            self.top1,
            columns=(
                'Owner',
                'Tool Name',
                'Per Day Rate',
                'Half Day Rate',
                'Added Date',
                'Booked Date',
                'Rent Status',
                'Hire Status',
                'Tool Status'
            ),yscrollcommand=yscrollbar.set) # sets the y scrollbar in the window


        # sets the column width of the page
        self.tv.heading('#0', text='SN')
        self.tv.column('#0', width=30, stretch=NO, anchor='center')
        self.tv.heading('#1', text='Owner')
        self.tv.column('#1', width=100, stretch=NO, anchor='center')
        self.tv.heading('#2', text='Tool Name')
        self.tv.column('#2', width=100, stretch=NO, anchor='center')
        self.tv.heading('#3', text='Rate per Day')
        self.tv.column('#3', width=90, stretch=NO, anchor='center')
        self.tv.heading('#4', text='Rate per Half Day')
        self.tv.column('#4', width=120, stretch=NO, anchor='center')
        self.tv.heading('#5', text='Added Date')
        self.tv.column('#5', width=100, stretch=NO, anchor='center')
        self.tv.heading('#6', text='Booked Date')
        self.tv.column('#6', width=100, stretch=NO, anchor='center')
        self.tv.heading('#7', text='Rent Status')
        self.tv.column('#7', width=75, stretch=NO, anchor='center')
        self.tv.heading('#9', text='Tool Condition')
        self.tv.column('#9', width=100, stretch=NO, anchor='center')
        self.tv.heading('#8', text='Hire Status')
        self.tv.column('#8', width=125, stretch=NO, anchor='center')

        self.tv.bind("<ButtonRelease-1>", self.add_book_date)  # binds the function to button 1

        self.tv.grid(row=0, columnspan=length, sticky='nsew')  # places the tv in grid starting from row 0
        self.treeview = self.tv
        yscrollbar.config(command=self.tv.yview)   # sets the scrollbar to the treeview's y axis

        # loops through the json database
        for i in range(length):
            if data[i]['rent_status'] == "no":  # if the rent status is no
                self.tool_box = StringVar()  # sets as a String Variable
                self.tool_box.set("Hire " + data[i]["tool_name"])  # stores a string value in the String Variable
                self.j_user = data[i]['adder_username']  # stores the current accessed username in a variable
            else:  # if the tool is rented shows its already booked
                self.tool_box = StringVar()
                self.tool_box.set("Already Booked")

            # inserts the data from json file to the treeview in the corresponding field
            self.treeview.insert(
                '',
                'end',
                text=str(i),
                values=(
                    data[i]['adder_username'],
                    data[i]['tool_name'],
                    data[i]['per_day_rate'],
                    data[i]['half_day_rate'],
                    data[i]['added_date'],
                    data[i]['booked_date'],
                    data[i]['rent_status'],
                    self.tool_box.get(),
                    data[i]['tools_condition']
                )
            )
            self.store_name = name  # storing the entered login username in a variable

    # the window which asks for booking date and dispatch hire status
    def add_book_date(self,event):
        data = self.tv.item(self.tv.selection())  # passes the values of currently clicked treeview row in data variable

        # show error if data is already rented or if it is user's own tool
        if data['values'][6] == "yes" or data['values'][0] == self.store_name:
            messagebox.showerror("Error", "This tool is unavailable")
        else:
            self.top1.withdraw()  # withdraws the the search bar
            self.top2 = Toplevel()  # opens book date window as a TopLevel window
            self.top2.title('Shared Power| Hire Tools')  # title of the window
            self.top2.geometry('450x220+300+200')  # size of the window
            self.top2.resizable(False, False) #removes the maximize button

            #Label and entries of booking date
            self.adder_date = Label(self.top2, text="When do you want to book the tool?\n(yyyy/mm/dd)",
                                font=('Verdana', 12),
                                bg="black", fg='yellow')
            self.adder_date.place(x=70, y=30)
            self.adder_date_entry = Entry(self.top2)
            self.adder_date_entry.place(x=165, y=90, height=25)

            # Label and entries of dispatch rider
            self.dispatch = Label(self.top2, text="Hire a dispatch?(yes/no)", font=('Verdana',12), bg="black", fg="yellow")
            self.dispatch.place(x=120, y=120)
            self.dispatch_entry = Entry(self.top2)
            self.dispatch_entry.place(x=165, y=150, height=25)

            # hire button which calls the hire tools function to store the required data
            self.hire_button = Button(self.top2, text="OK",
                                  command=lambda: self.hire_tools(self.store_name) or self.top1.deiconify
                                  , font=('Verdana', 12),
                                  bg="black", fg='yellow')
            self.hire_button.place(x=185, y=185, width=60, height=30)

    # backend of hiring the tools
    def hire_tools(self, name):
        stuff = self.tv.item(self.tv.selection())  # passes the values of currently clicked treeview row in data variable

        # open the tool json file as read
        with open('tools.json') as f:
            tools_data = json.load(f)

        # open the transaction json file as read
        with open('transactions.json', 'r') as g:
            transaction_data = json.load(g)

        current_date = datetime.datetime.today()  # find the current date and time
        if current_date.day == 1:  # checks if the current day is 1
            i = 0
            with open('transactions.json', 'r+') as fh:
                transaction_data = json.load(fh)
                a = transaction_data['transaction']
                a.clear()
        if self.adder_date_entry.get() and self.dispatch_entry.get():  # checks if a value was given by the user
            # checks if the dispatch value entered is yes or no.
            if self.dispatch_entry.get() == "yes" or self.dispatch_entry.get() == "no":
                try:  # exception handling to check whether the booked date entered above is in correct format
                    str_date =datetime.datetime.strptime(self.adder_date_entry.get(),'%Y/%m/%d')  # convert the string received to datetime
                    current_date=datetime.datetime.today()  # find the current date and time
                    days_rented = datetime.datetime.today() + datetime.timedelta(days=3)  # add 3 days to the current date
                    # allow data to be updated only if the entered booked date is greater than today's date and upto 3 days
                    if str_date>=current_date and str_date <=days_rented:
                        # loops around the tools json file
                        for data in tools_data['tools']:
                            # checks if the username and tool name matches the clicked value from the treeview
                            if data['adder_username'] == stuff['values'][0]:
                                if data['tool_name'] == stuff['values'][1]:
                                    data['renter_username'] = name   # store renter's name
                                    data['booked_date'] = self.adder_date_entry.get()  # store the entered date
                                    data['rent_status'] = "yes"  # change the rent status
                                    if data['rent_status'] == "yes" and data['renter_username'] == name and data['booked_date'] \
                                        == self.adder_date_entry.get():
                                        messagebox.showinfo("Info", 'Tool Hired successfully.')  # info message to show tool has been hired
                                        # appends data on the transaction database to update the invoice
                                        transaction_data['transaction'].append({
                                    "owner":stuff['values'][0],
                                    "renter":name,
                                    "tool_name": stuff['values'][1],
                                    "booked_date": self.adder_date_entry.get(),
                                    "days_owned": " ",
                                    "per_day_rate": data['per_day_rate'],
                                    "half_day_rate": data['half_day_rate'],
                                    "fine_cost": " ",
                                    "fine_status": "no",
                                    "dispatch_hire_status": self.dispatch_entry.get(),
                                    "hire_charge":"0",
                                    "total_cost": " ",
                                    "tool_condition": " "
                                    }
                                    )
                                        self.top2.destroy()  # destroys the previous window
                    # if it doesn't satisty the condtion above display error message
                    else:
                        messagebox.showerror("Info", "The date should be more than the current date under and under 3 days")
                except:
                    messagebox.showwarning("Error", "Please fill the date in correct format")
            else:
                messagebox.showerror("Info", "The dispatch hired status should either be yes or no.")
        else:
            messagebox.showwarning("Error", 'Please fill the required data.')

        # write the edited values into their respective files
        with open('tools.json', "w+") as fh:
            json.dump(tools_data, fh, indent=2)
        with open('transactions.json', "w+") as gh:
            json.dump(transaction_data, gh, indent=2)


class Remove(object):

    # GUI of remove tools
    def remove_tools(self, name):
        self.top1 = Toplevel()  # open the remove tools window as toplevel
        self.top1.geometry('600x701+650+50')  # window size
        self.top1.resizable(False, False)  # removes the maximize button
        self.top1.title('Shared Power| Remove Tools')  # title of the window

        # background for the remove tools GUI
        self.welcome_background = PhotoImage(file="login.png", width=600, height=701)
        self.background_label = Label(self.top1, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=600, height=701)

        # Labels and entries of remove tools
        self.toolname_to_remove = Label(self.top1, text="Tool to remove:", font=('Verdana', 12), bg="#1c1c20",
                                        fg='yellow')
        self.toolname_to_remove.place(x=100, y=150, width=200, height=40)
        self.toolname_to_remove_entry = Entry(self.top1)
        self.toolname_to_remove_entry.place(x=300, y=150, width=200, height=40)

        # ok button which directs to backend of removing tools
        self.ok_remove = Button(self.top1, text="OK", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                command=lambda: self.tool_remove(name))
        self.ok_remove.place(x=250, y=450, width=80, height=30)

        # back button which destroys itself
        self.back_remove = Button(self.top1, text="Quit", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                  command=lambda: self.top1.destroy())
        self.back_remove.place(x=250, y=500, width=80, height=30)

        self.remove_tools_list(name)  # opens the tool list side by side which are available to remove

    # displays the available tools to remove
    def remove_tools_list(self,name):
        self.top3 = Toplevel()  # opens remove tool list window in toplevel
        self.top3.resizable(False, False) # removes the maximize button
        self.top3.title('Shared Power| Remove Tools')  # title of the window
        Search().search_grid(self.top3)  # calls the search grid method of the Search object
        #open tools.json as read
        with open('tools.json') as f:
            tools_data = json.load(f)
            data = tools_data['tools']
        count = 1  # initialize count
        #loops through the data in tools key in the json file
        for keys in data:
            if keys['adder_username'] == name:  # condition to show the tools the user has added

                #label to display the required data from the json file in rows and columns
                username_label = Label(self.top3, text=keys['adder_username'], font=('Verdana', 12), bg="black",
                                       fg='yellow')
                username_label.grid(row=count, column=0)
                tool_name_label = Label(self.top3, text=keys['tool_name'], font=('Verdana', 12), bg="black",
                                        fg='yellow')
                tool_name_label.grid(row=count, column=1)
                pday_rate_label = Label(self.top3, text=keys['per_day_rate'], font=('Verdana', 12), bg="black",
                                        fg='yellow')
                pday_rate_label.grid(row=count, column=2)
                hday_rate_label = Label(self.top3, text=keys['half_day_rate'], font=('Verdana', 12), bg="black",
                                        fg='yellow')
                hday_rate_label.grid(row=count, column=3)
                added_date_label = Label(self.top3, text=keys['added_date'], font=('Verdana', 12), bg="black",
                                         fg='yellow')
                added_date_label.grid(row=count, column=4)
                count = count + 1  # increasing this value so that the row value also increases storing data a in new row
        self.top3.configure(background="black")  # sets background of the window as black

    # backend of remove tools
    def tool_remove(self, name):
        # open tools.json as read
        with open('tools.json', 'r') as f:
            tools_data = json.load(f)
        # checks if the user has entered the data in entry box
        if self.toolname_to_remove_entry.get():
            # loops through the data in tools key in the json file
            for data in tools_data['tools']:
                # checks to see if the tool name matches the tool in the database
                if data['tool_name'] == self.toolname_to_remove_entry.get():
                    # checks to see if the username matches the username in the database
                    if data['adder_username'] == name:
                        i = tools_data['tools'].index(data) # find the index value of the current data
                        del tools_data['tools'][i] #delete the current data in the list
                        messagebox.showinfo("Info", "Your tool has been successfully removed.")
                        try:  # exception handling to avoid errors if one of the window has been closed somehow
                            self.top3.withdraw()
                            self.top1.withdraw()
                        except:
                            self.top1.withdraw()
                        break  # breaks the loop
            # show error if tool is not found
            if data['tool_name'] != self.toolname_to_remove_entry.get():
                    messagebox.showinfo("Info", "No such tool available.")
        else:
            messagebox.showerror("Error", "Please fill in the tool name.")

        # write the edited file data into tools.json
        with open("tools.json", "w+") as fh:
            json.dump(tools_data, fh, indent=2)


class Return(object):

   # return tools GUI
    def return_tools(self, name):
        self.top = Toplevel()  # open the return tools window as toplevel
        self.top.geometry('600x701+650+50')  # window size
        self.top.resizable(False, False)  # removes the maximize button
        self.top.title('Shared Power| Return Tools')  # title of the window

        # background for the return tools GUI
        self.welcome_background = PhotoImage(file="login.png", width=600, height=701)
        self.background_label = Label(self.top, image=self.welcome_background)
        self.background_label.place(x=0, y=0, width=600, height=701)

        #Required Label and entries for the backend to work
        self.toolname_to_return = Label(self.top, text="Tool to return:", font=('Verdana', 12),bg="#1c1c20",fg ='yellow')
        self.toolname_to_return.place(x=100, y=100, width=200, height=40)
        self.toolname_to_return_entry = Entry(self.top)
        self.toolname_to_return_entry.place(x=300, y=100, width=200, height=40)
        self.condition_to_return = Label(self.top, text="Tool Condition:", font=('Verdana', 12), bg="#1c1c20",
                                        fg='yellow')
        self.condition_to_return.place(x=100, y=150, width=200, height=40)
        self.condition_to_return_entry = Entry(self.top)
        self.condition_to_return_entry.place(x=300, y=150, width=200, height=40)


        # button goes to the browse_photos function passing the username entered by user during login
        self.browse_button = Button(self.top, text="Add pic", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                    command=lambda: self.browse_photos(name))
        self.browse_button.place(x=350, y=550, width=100, height=25)

        # goes to the backend of return tools using the data entered in this GUI
        self.ok_return = Button(self.top, text="OK", font=('Verdana', 12), bg="#1c1c20", fg='yellow'
                                ,command=lambda: self.user_return(name))
        self.ok_return.place(x=250, y=450, width=80, height=30)


        self.back_return = Button(self.top, text="Quit", font=('Verdana', 12), bg="#1c1c20", fg='yellow',
                                  command=lambda: self.top.destroy())  # goes to the homepage window
        self.back_return.place(x=250, y=500, width=80, height=30)

        self.return_tool_list(name) # Shows the tool list side by side which are available to return

    # displays the available tools to return
    def return_tool_list(self, name):
        self.top2 = Toplevel()  # opens return tool list in toplevel window
        self.top2.resizable(False, False)  # remove the maximize button
        self.top2.title('Shared Power| Return Tools')  # title of the window

        Search().search_grid(self.top2)  # calls the search grid method of the Search object
        # open tools.json as read
        with open('tools.json') as f:
            tools_data = json.load(f)
            data = tools_data['tools']
        count = 1  # initialize the count variable
        # loops through the data in tools key in the json file
        for keys in data:

            if keys['renter_username'] == name: #condition to show the tools the user has rented
                username_label = Label(self.top2, text=keys['adder_username'], font=('Verdana', 12), bg="black",
                                       fg='yellow')
                username_label.grid(row=count, column=0)
                tool_name_label = Label(self.top2, text=keys['tool_name'], font=('Verdana', 12), bg="black",
                                        fg='yellow')
                tool_name_label.grid(row=count, column=1)
                pday_rate_label = Label(self.top2, text=keys['per_day_rate'], font=('Verdana', 12), bg="black",
                                        fg='yellow')
                pday_rate_label.grid(row=count, column=2)
                hday_rate_label = Label(self.top2, text=keys['half_day_rate'], font=('Verdana', 12), bg="black",
                                        fg='yellow')
                hday_rate_label.grid(row=count, column=3)
                added_date_label = Label(self.top2, text=keys['added_date'], font=('Verdana', 12), bg="black",
                                         fg='yellow')
                added_date_label.grid(row=count, column=4)
                count = count + 1 # increasing this value so the row value is also increased in the GUI
        self.top2.configure(background="black")  # sets background as black

    # backend of return tools
    def user_return(self, name):
        # open tools.json as read
        with open("tools.json") as f:
            tools_data = json.load(f)
        # checks to see if the user has entered a tool name
        if self.toolname_to_return_entry.get():
            # loops through the data in tools key in the json file
            for data in tools_data['tools']:
                # checks only the tools which are rented
                if data['rent_status'] == 'yes':
                    # finds the entered tool name in the database
                    if data['tool_name'] == self.toolname_to_return_entry.get():
                        # matches if the entered tool name is hired by the user logged in
                        if data['renter_username'] == name:
                            messagebox.showinfo("Success", 'Tool has been successfully returned.')
                            data['rent_status'] = "no"
                            data['booked_date'] = " "
                            data['renter_username'] = " "
                            self.transaction(name, data['adder_username'],data['tool_name'] ) # passes the values to transaction function to update the invoice
                            break  # breaks the loop
        else:  # displays error if tool name is not entered
            messagebox.showinfo("Error", 'State the tool name.')

        if data['tool_name'] != self.toolname_to_return_entry.get():
                messagebox.showerror("Error", 'Enter a correct tool name')

        # writes the edited data above into the json file
        with open("tools.json", "w+") as fh:
            json.dump(tools_data, fh, indent=2)

    # renames and saves the returned tool photos into a directory
    def browse_photos(self,name):
        browse = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                             filetype=(("jpeg", "*.jpg"), ("png", "*.png*")))  # select a photo
        image1=Image.open(browse)  # opens the photo from the above directory
        image1.save('Return/{} renter tool {}.jpg'.format(name, self.toolname_to_return_entry.get()))  # rename and save the photo into the Return directory
        self.browse_button.destroy()  # removes the add photo button after the photo has been added

        # Places a label of the file location instead of the button
        self.label=Label(self.top, text=" ",font=('Verdana', 8), bg="#1c1c20", fg='yellow')
        self.label.place(x=350, y=550)
        self.label.configure(text= browse)

    # database for the invoice
    def transaction(self,name,owner,tool):

        try:  # exception handling to to close both opened windows if one is already closed
            self.top2.withdraw()
            self.top.withdraw()
        except:
            self.top.withdraw()
        # open transaction.json as read
        with open('transactions.json', 'r') as g:
            transaction_data = json.load(g)
        cost = 0  # initialize the cost variable
        # loops through the data in transaction key in the json file
        for value in transaction_data['transaction']:
            if value['owner']== owner:  # checks if the owner's username matches the username in the database
                if value['renter']== name: # checks if the renter is same as the one in the database
                    if value['tool_name']==tool: #checks if the matched renter and owner has the tool booked
                        converted_date = datetime.datetime.strptime(value['booked_date'], '%Y/%m/%d')  # converts the booked date in string to datetime in the given format
                        if datetime.datetime.today() <= converted_date:
                            days_rented = 0
                            str_days_rented = days_rented
                        else:
                            days_rented = datetime.datetime.today() - converted_date  # subtracts current and booked date to find the days tool was owned
                            str_days_rented = days_rented.days  # gets the days value of the datetime
                        time_rented=days_rented.seconds  # gets the second value of the datetime
                        if time_rented>=43200 and time_rented<=86400:  # checks if the time is > 12 h
                            cost=float(value['half_day_rate'])  # if it is add the half day rate from the database in float
                        # check to see if the user is fined or not
                        if str_days_rented >= 4:
                            value['fine_status']="yes"
                            value['tool_condition'] = self.condition_to_return_entry.get()
                            value['days_owned']=str(str_days_rented)
                            messagebox.showinfo("Fined",
                                               'You have been fined for late return.')
                            cost=cost+ (3*float(value['per_day_rate']))
                            fine = float(value['per_day_rate'])*2*(float(str_days_rented)-3)  # calculation to find fine amount
                            value['fine_cost'] = str(fine)  # store the fined amount
                            cost=cost+fine
                            cost=cost+5  # total cost after fine
                        else:
                            value['fine_status']="no"
                            value['tool_condition']=self.condition_to_return_entry.get()
                            value['days_owned'] = str(str_days_rented)
                            cost=cost+(float(str_days_rented)*float(value['per_day_rate']))  # calculation without fine
                            cost=cost+5
                            value['fine_cost'] = "0"
                        if value['dispatch_hire_status']=="yes":  # checks if the user has hired a dispatch
                            cost=cost + 10  # gives 10 pound charge to dispatch
                            # stores the cost value in the database
                            value['total_cost']=str(cost)
                            value['hire_charge']="10.0"
                        else:
                            value['total_cost']=str(cost)   # stores the cost value in the database
        #writes the edited files in the transaction.json file
        with open("transactions.json", "w+") as gh:
            json.dump(transaction_data, gh, indent=2)


Login().log_in()  # calling the log_in method of object Login()
