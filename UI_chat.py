import tkinter
import customtkinter
import logging
import UI_app_frame
import functions_chat

app = customtkinter.CTk()

def main():
    global app

    app.columnconfigure(0, minsize = 75)
    app.columnconfigure(1, minsize = 300)
    app.columnconfigure(2, weight = 1)

    chats = customtkinter.CTkFrame(master=app, fg_color='red')
    chat_window = customtkinter.CTkFrame(master=app)
    profile = customtkinter.CTkFrame(master=app, fg_color='red', width=10)
    entry = customtkinter.CTkEntry(master=chat_window)
    messages = customtkinter.CTkFrame(master=chat_window)
    scrollbar = customtkinter.CTkScrollbar(master=chat_window)
    
    chats.grid(column = 1, row = 0, sticky = 'nsew')
    chat_window.grid(column = 2, row = 0, sticky = 'nsew')
    profile.grid(column = 3, row = 0, sticky = 'nsew')
    entry.grid(row = 2, padx = 10, pady = 10, sticky = 'ew')
    messages.grid(row = 1, column=0, padx = 10, sticky = 'ews')
    scrollbar.grid(row = 1, column = 2, sticky = 'nse')

    chat_window.rowconfigure(0, minsize = 75)
    chat_window.rowconfigure(1, weight = 1)
    chat_window.columnconfigure(0, weight = 1)
    messages.columnconfigure(0, weight = 1)
   
    def display_dm_messages(dmID):
        messages = functions_chat.get_dm_messages(dmID)
        for x in messages:
            message = customtkinter.CTkLabel(master = messages, text='hi')
            message.grid(column = 1)
        
    
    for x in range(25):
        display_dm_messages(1)