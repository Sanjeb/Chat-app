import tkinter
import customtkinter
import logging
import time
import UI_chat
import functions_chat

app = customtkinter.CTk()

def chat():
    global app

    app.columnconfigure(0, minsize = 75)
    app.columnconfigure(1, minsize = 300)
    app.columnconfigure(2, weight = 1)

    chats = customtkinter.CTkFrame(master=app, fg_color='red')
    chat_window = customtkinter.CTkFrame(master=app)
    profile = customtkinter.CTkFrame(master=app, fg_color='red', width=10)
    entry = customtkinter.CTkEntry(master=chat_window)
    messages = customtkinter.CTkFrame(master=chat_window)
    canvas = tkinter.Canvas(master=messages)
    scrollbar = customtkinter.CTkScrollbar(master=messages, command=canvas.yview)
    
    chats.grid(column = 1, row = 0, sticky = 'nsew')
    chat_window.grid(column = 2, row = 0, sticky = 'nsew')
    profile.grid(column = 3, row = 0, sticky = 'nsew')
    entry.grid(row = 2, padx = 10, pady = 10, sticky = 'ew')
    messages.grid(row = 1, column=0, sticky = 'nsew')
    canvas.grid(row = 0, column= 0, sticky='nsew')
    scrollbar.grid(row = 0, column = 2, sticky = 'nse')

    chat_window.rowconfigure(0, minsize = 75)
    chat_window.rowconfigure(1, weight = 1)
    chat_window.columnconfigure(0, weight = 1)
    messages.columnconfigure(0, weight = 1)
    messages.rowconfigure(0, weight = 1)

    m = functions_chat.get_dm_messages(1)
    for x in m:
        customtkinter.CTkLabel(master=canvas, text = x[1]).pack()

def main():
    global app
    app.geometry("1600x900")
    app.title("CHAT")

    app.rowconfigure(0, weight = 1)
    app.rowconfigure(1, minsize = 75)
    
    chat()

    app.mainloop()

main()