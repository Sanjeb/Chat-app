import tkinter
import customtkinter
import functions_user
import logging

def login():
    #Declaring win variables
    customtkinter.set_appearance_mode("dark")
    win = customtkinter.CTk()
    win.geometry("1280x720")
    win.title("LOGIN")
  
    #Checks if user has already logged in and authenticates with database
    def credentials():
        global id
        global email
        with open('credentials.txt', 'r') as f:
            id, email, password = f.read().split()
        ret = functions_user.login(email, password)
        if ret == 0:
            win.destroy()
            import UI_app_frame
            UI_app_frame.main()
            print("auth")
            logging.info("Succesfully authenticated")

    #On login button press function
    def on_press():
        ret = functions_user.login(entryEmail.get(), entryPassword.get())
        if ret == 0:
            labelIncorrect.configure(text="")
            win.destroy()
            import UI_app_frame
            UI_app_frame.main()
        elif ret == 1:
            labelIncorrect.configure(text="Incorrect email or password. Please try again")
        else:
            labelIncorrect.configure(text="Unknown error. Please check your internet connection.")

    def create_account():
        win.destroy()
        import UI_Signup
        UI_Signup.main()

    #Configures win grid rows
    win.rowconfigure((0, 12), weight = 4)
    win.rowconfigure(9, minsize = 50)
    #Configures win grid columns
    win.columnconfigure((0, 1), minsize = 50)
    win.columnconfigure((1, 2), weight = 1)

    #Text labels
    labelWelcome = customtkinter.CTkLabel(master=win, text="Welcome back", text_font=('comic sans', 30))
    labelSignIn = customtkinter.CTkLabel(master=win, text="Sign in to start using DISCARD", text_font=('comic sans', 20))
    labelEmail = customtkinter.CTkLabel(master=win, text="E-mail:", text_font=('comic sans', 10), anchor='w', justify='left')
    labelPassword = customtkinter.CTkLabel(master=win, text="Password:", text_font=('comic sans', 10), anchor='w', justify='left')
    labelIncorrect = customtkinter.CTkLabel(master=win, text="", text_font=('comic sans', 10), text_color='red')
    labelNew = customtkinter.CTkLabel(master=win, text = "New to discard? Create an account", text_font=('comic sans', 10))
    #Entry boxes
    entryEmail = customtkinter.CTkEntry(master=win, placeholder_text="Enter your email", width=200)
    entryPassword = customtkinter.CTkEntry(master=win, placeholder_text="Enter you password", width=200, show = '\u2022')
    #Buttons
    buttonLogin = customtkinter.CTkButton(master=win, text='LOGIN', width=200, command=on_press)
    buttonCreateAccount = customtkinter.CTkButton(master=win, text = 'Create a new account', width = 200, command = create_account)

    #Arranging all widgetes on screen
    labelWelcome.grid(row=1, column=1, sticky='w', pady = 0)
    labelSignIn.grid(row=2, column=1, sticky = 'w', pady = 0)
    labelEmail.grid(row=3, column=1, sticky = 'w', pady = (20, 0), padx = (0, 50))
    entryEmail.grid(row=4, column=1, sticky='w')
    labelPassword.grid(row=5, column=1, sticky = 'w', pady = (10, 0), padx = (0, 50))
    entryPassword.grid(row=6, column=1, sticky='w', pady = (0, 20))
    buttonLogin.grid(row=7, column=1, sticky='w')
    labelIncorrect.grid(row=8, column=1, sticky='w')
    labelNew.grid(row=10, column=1, sticky='w')
    buttonCreateAccount.grid(row = 11, column = 1, sticky = 'w')

    win.mainloop()

def main():
    #Checks if user has already logged in and authenticates with database
    try:
        global id
        global email
        with open('credentials.txt', 'r') as f:
            id, email, password = f.read().split()
        ret = functions_user.login(email, password)
        if ret == 0:
            import UI_app_frame
            UI_app_frame.main()
            print("auth")
            logging.info("Succesfully authenticated")
        else:
            login()
    except FileNotFoundError:
        login()