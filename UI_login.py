import tkinter
import customtkinter
import functions_user
import logging
import UI_Signup

def main():

    #Declaring app variables
    app = customtkinter.CTk()
    app.geometry("1280x720")
    app.title("LOGIN")
  
    #Checks if user has already logged in and authenticates with database
    def credentials():
        global id
        global email
        try:
            with open('credentials.txt', 'r') as f:
                id, email, password = f.read().split()
            ret = functions_user.login(email, password)
            if ret == 0:
                app.destroy()
                import UI_app_frame
                UI_app_frame.main()
                logging.info("Succesfully authenticated")
        except:
            pass

    #On login button press function
    def on_press():
        ret = functions_user.login(entryEmail.get(), entryPassword.get())
        if ret == 0:
            labelIncorrect.configure(text="")
            app.destroy()
            import UI_app_frame
            UI_app_frame.main()
        elif ret == 1:
            labelIncorrect.configure(text="Incorrect email or password. Please try again")
        else:
            labelIncorrect.configure(text="Unknown error. Please check your internet connection.")

    def create_account():
        print("Create account button pressed")
        

    #Configures app grid rows
    app.rowconfigure((0, 12), weight = 4)
    app.rowconfigure(9, minsize = 50)
    #Configures app grid columns
    app.columnconfigure((0, 1), minsize = 50)
    app.columnconfigure((1, 2), weight = 1)

    #Text labels
    labelWelcome = customtkinter.CTkLabel(master=app, text="Welcome back", text_font=('comic sans', 30))
    labelSignIn = customtkinter.CTkLabel(master=app, text="Sign in to start using DISCARD", text_font=('comic sans', 20))
    labelEmail = customtkinter.CTkLabel(master=app, text="E-mail:", text_font=('comic sans', 10), anchor='w', justify='left')
    labelPassword = customtkinter.CTkLabel(master=app, text="Password:", text_font=('comic sans', 10), anchor='w', justify='left')
    labelIncorrect = customtkinter.CTkLabel(master=app, text="", text_font=('comic sans', 10), text_color='red')
    labelNew = customtkinter.CTkLabel(master=app, text = "New to discard? Create an account", text_font=('comic sans', 10))
    #Entry boxes
    entryEmail = customtkinter.CTkEntry(master=app, placeholder_text="Enter your email", width=200)
    entryPassword = customtkinter.CTkEntry(master=app, placeholder_text="Enter you password", width=200, show = '\u2022')
    #Buttons
    buttonLogin = customtkinter.CTkButton(master=app, text='LOGIN', width=200, command=on_press)
    buttonCreateAccount = customtkinter.CTkButton(master=app, text = 'Create a new account', width = 200, command = create_account)

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

    credentials()
    app.mainloop()