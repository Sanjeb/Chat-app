import tkinter
import customtkinter

app = customtkinter.CTk()
app.geometry("1600x900")
app.title("CHAT")


app.columnconfigure(1, minsize=400)
app.columnconfigure(2, weight = 1)
app.columnconfigure(0, minsize=80)

app.rowconfigure(0, weight = 1)
app.rowconfigure(1, minsize = 75)

chats = customtkinter.CTkFrame(master=app, fg_color='red')
chat_window = customtkinter.CTkFrame(master=app)

chats.grid(column = 1, row = 0, sticky = 'nsew')
chat_window.grid(column = 2, row = 0, sticky = 'nsew')

app.mainloop()