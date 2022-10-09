import tkinter
import customtkinter
import logging
import time
import UI_chat

app = customtkinter.CTk()

def main():
    global app
    app.geometry("1600x900")
    app.title("CHAT")

    app.rowconfigure(0, weight = 1)
    app.rowconfigure(1, minsize = 75)
    
    UI_chat.main()

    app.mainloop()