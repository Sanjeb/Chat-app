import tkinter
import customtkinter
import functions_user
import UI_app_frame
import logging

def main():

    #Declaring app variables
    app = customtkinter.CTk()
    app.geometry("1600x900")
    app.title("LOGIN")
  
    #Checks if user has already logged in and authenticates with database
    def credentials():
        try:
            with open('credentials.txt', 'r') as f:
                id, email, password = f.read().split()
            ret = functions_user.login(email, password)
            if ret == 0:
                app.destroy()
                UI_app_frame.main()
                logging.info("Succesfully authenticated")
        except:
            pass

    credentials()

    #On login button press function
    def on_press():
        ret = functions_user.login(entryEmail.get(), entryPassword.get())
        if ret == 0:
            labelIncorrect.configure(text="")
            app.destroy()
            UI_app_frame.main()
        elif ret == 1:
            labelIncorrect.configure(text="Incorrect email or password. Please try again")
        else:
            labelIncorrect.configure(text="Unknown error. Please check your internet connection.")

    #Configures app grid rows
    app.rowconfigure((0, 9), weight = 4)
    #Configures app grid columns
    app.columnconfigure((0, 3), minsize = 50)
    app.columnconfigure((1, 2), weight = 1)

    #Text labels
    labelWelcome = customtkinter.CTkLabel(master=app, text="Welcome back", text_font=('comic sans', 30))
    labelSignIn = customtkinter.CTkLabel(master=app, text="Sign In to start using chat", text_font=('comic sans', 20))
    labelEmail = customtkinter.CTkLabel(master=app, text="E-mail:\t\t\t", text_font=('comic sans', 10))
    labelPassword = customtkinter.CTkLabel(master=app, text="Password:\t\t", text_font=('comic sans', 10))
    labelIncorrect = customtkinter.CTkLabel(master=app, text="", text_font=('comic sans', 10), text_color='red')
    #Entry boxes
    entryEmail = customtkinter.CTkEntry(master=app, placeholder_text="Enter your email", width=200)
    entryPassword = customtkinter.CTkEntry(master=app, placeholder_text="Enter you password", width=200, show = '\u2022')
    #Buttons
    buttonLogin = customtkinter.CTkButton(master=app, text='LOGIN', width=200, command=on_press)

    #Arranging all widgetes on screen
    labelWelcome.grid(row=1, column=1, sticky='w', pady = 0)
    labelSignIn.grid(row=2, column=1, sticky = 'w', pady = 0)
    labelEmail.grid(row=3, column=1, sticky = 'w', pady = (20, 0), padx = (0, 50))
    entryEmail.grid(row=4, column=1, sticky='w')
    labelPassword.grid(row=5, column=1, sticky = 'w', pady = (10, 0), padx = (0, 50))
    entryPassword.grid(row=6, column=1, sticky='w', pady = (0, 20))
    buttonLogin.grid(row=7, column=1, sticky='w')
    labelIncorrect.grid(row=8, column=1, sticky='w')

    app.mainloop()