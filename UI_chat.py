import tkinter
import customtkinter
import logging
import UI_app_frame
import functions_chat

def main():
    UI_app_frame.app.columnconfigure(0, minsize = 75)
    UI_app_frame.app.columnconfigure(1, minsize = 300)
    UI_app_frame.app.columnconfigure(2, weight = 1)

    chats = customtkinter.CTkFrame(master=UI_app_frame.app, fg_color='red')
    chat_window = customtkinter.CTkFrame(master=UI_app_frame.app)
    profile = customtkinter.CTkFrame(master=UI_app_frame.app, fg_color='red', width=10)
    scrollbar = customtkinter.CTkScrollbar(master=chat_window)
    #scrollbar.pack(side=RIGHT, fill=Y)
    
    chats.grid(column = 1, row = 0, sticky = 'nsew')
    chat_window.grid(column = 2, row = 0, sticky = 'nsew')
    profile.grid(column = 3, row = 0, sticky = 'nsew')

    def display_dm_messages(dmID):
        messages = functions_chat.get_dm_messages(dmID)
        for x in messages:
            customtkinter.CTkLabel(master=chat_window, text=x[1]).grid(column=1, sticky = 'w')
    display_dm_messages(1)
    display_dm_messages(1)