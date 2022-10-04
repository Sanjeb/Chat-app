import tkinter
import customtkinter

#Declaring app variables
app = customtkinter.CTk()
app.geometry("10000*10000")
app.title("LOGIN")

#Configures app grid rows
app.rowconfigure((0, 7), weight = 4)
#Configures app grid columns
app.columnconfigure((0, 3), minsize = 50)
app.columnconfigure((1, 2), weight = 1)

labelWelcome = customtkinter.CTkLabel(master=app, text="Welcome back", text_font=('comic sans', 30))
labelSignIn = customtkinter.CTkLabel(master=app, text="Sign In to start using chat", text_font=('comic sans', 20))
labelEmail = customtkinter.CTkLabel(master=app, text="E-mail:\t\t\t", text_font=('comic sans', 10))
labelPassword = customtkinter.CTkLabel(master=app, text="Password:\t\t", text_font=('comic sans', 10))
email = customtkinter.CTkEntry(master=app, placeholder_text="Enter your email", width=200)
password = customtkinter.CTkEntry(master=app, placeholder_text="Enter you password", width=200, show = '\u2022')


labelWelcome.grid(row=1, column=1, sticky='w', pady = 0)
labelSignIn.grid(row=2, column=1, sticky = 'w', pady = 0)
labelEmail.grid(row=3, column=1, sticky = 'w', pady = (20, 0), padx = (0, 50))
email.grid(row=4, column=1, sticky='w')
labelPassword.grid(row=5, column=1, sticky = 'w', pady = (10, 0), padx = (0, 50))
password.grid(row=6, column=1, sticky='w')

app.mainloop()