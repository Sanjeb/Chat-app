import tkinter
import customtkinter
import logging
import time
import functions_chat
import threading

app = customtkinter.CTk()

def chat():
    global app

    app.columnconfigure(0, minsize = 75) #Column for sidebar/switcher between groups and DMs
    app.columnconfigure(1, minsize = 300) #Column for viewing chats
    app.columnconfigure(2, weight = 1) #Column for Viewing messages
    app.columnconfigure(3, minsize = 300) #Column for selected chat profile info

    switcher = customtkinter.CTkFrame(master=app, width=75) #Frame for Switcher between chat and DMs
    chats = customtkinter.CTkFrame(master=app) #All Chats
    chat_window = customtkinter.CTkFrame(master=app) #Frame for viewing messages
    profile = customtkinter.CTkFrame(master=app, fg_color='red') #Frame for Profile

    #Configures grid for all the frames in window
    switcher.grid(column = 0, row = 0 , sticky = 'nsew')
    chats.grid(column = 1, row = 0, sticky = 'nsew')
    chat_window.grid(column = 2, row = 0, sticky = 'nsew')
    profile.grid(column = 3, row = 0, sticky = 'nsew')

    #Switcher     
    switcher.rowconfigure(0, weight = 1)
    switcher.rowconfigure(1, weight = 1)

    #Message viewer
    def message_viewer(id):
        entry = customtkinter.CTkEntry(master=chat_window)
        messages_canvas = tkinter.Canvas(master=chat_window, borderwidth=0, highlightthickness=0, background="#343638")
        messages = customtkinter.CTkFrame(master=messages_canvas)
        messages_scrollbar = customtkinter.CTkScrollbar(master=chat_window, command=messages_canvas.yview)
        messages_canvas.configure(yscrollcommand=messages_scrollbar.set)
        
        entry.grid(row = 2, padx = 10, pady = 10, sticky = 'ew')
        messages_canvas.grid(row = 1, column= 0, sticky='nsew')
        messages_scrollbar.grid(row = 1, column = 1, sticky = 'nse')
        messages_canvas.create_window((0,0), window=messages, width=800, anchor="nw")

        def onFrameConfigure(messages_canvas):
            '''Reset the scroll region to encompass the inner frame'''
            messages_canvas.configure(scrollregion=messages_canvas.bbox("all"))

        messages.bind("<Configure>", lambda event, messages_canvas=messages_canvas: onFrameConfigure(messages_canvas))


        chat_window.rowconfigure(0, minsize = 75)
        chat_window.rowconfigure(1, weight = 1)
        chat_window.columnconfigure(0, weight = 1)
        messages.columnconfigure(0, weight = 1)

        m = functions_chat.get_dm_messages(id) #Returns list in the format [(MessageID, MessageText, SenderUserID, DMID), (MessageID, MessageText, SenderUserID, DMID)]
        global lastMessageID

        def enter(event):
            event.widget.configure(fg_color='yellow')
        def leave(event):
            event.widget.configure(fg_color='#343638')
        for x in m:
            m_frame = customtkinter.CTkFrame(master=messages)
            message_label = customtkinter.CTkLabel(master=m_frame, text=x[1], anchor='w')
            message_label.pack()
            m_frame.grid(column=0, sticky = 'ew')
            m_frame.bind('<Enter>', enter)
            m_frame.bind('<Leave>', leave)
            lastMessageID = x[0]

        def update():
            global DisplayedUserID
            global lastMessageID
            m = functions_chat.get_latest_dm_messages(DisplayedUserID, lastMessageID)
            for x in m:
                m_frame = customtkinter.CTkFrame(master=messages)
                message_label = customtkinter.CTkLabel(master=m_frame, text=x[1], anchor='w')
                message_label.pack()
                m_frame.grid(column=0, sticky = 'ew')
                m_frame.bind('<Enter>', enter)
                m_frame.bind('<Leave>', leave)
                lastMessageID = x[0]


        def send(event):
            global DisplayedUserID
            message = entry.get()
            entry.delete(0, 'end')
            if message != '':
                finalMessage = ''
                for x in message:
                    if x != "'":
                        finalMessage += x
                    else:
                        finalMessage += "'" + x
                functions_chat.send_dm_messages(DisplayedUserID, finalMessage)
                update()
            
            
        
        entry.bind('<Return>', send)

    # Chats
    def chats_viewer():
        
        chats_canvas = tkinter.Canvas(master=chats, borderwidth=0, highlightthickness=0, background="#343638")
        chats_profiles = customtkinter.CTkFrame(master=chats_canvas)
        chat_scrollbar = customtkinter.CTkScrollbar(master=chats, command=chats_canvas.yview)
        chats_canvas.configure(yscrollcommand=chat_scrollbar.set)

        chats_canvas.grid(row = 0, column= 0, sticky='nsew')
        chat_scrollbar.grid(row = 0, column = 1, sticky = 'nse')
        chats_canvas.create_window((4,4), window=chats_profiles, anchor="nw")

        def onFrameConfigure(chats_canvas):
            '''Reset the scroll region to encompass the inner frame'''
            chats_canvas.configure(scrollregion=chats_canvas.bbox("all"))

        chats_profiles.bind("<Configure>", lambda event, chats_canvas=chats_canvas: onFrameConfigure(chats_canvas))

        chats.rowconfigure(0, weight = 1)

        def func():
            m = functions_chat.get_dm_users() #Returns list in the format [(UserID, DMID), (UserID, DMID)]
            def enter(event):
                event.widget.configure(fg_color='yellow')
            def leave(event):
                event.widget.configure(fg_color='#343638')
            def click(event, id):
                global DisplayedUserID
                for widget in chat_window.winfo_children():
                    widget.destroy()
                DisplayedUserID = id
                message_viewer(id)
            for x in m:
                m_frame = customtkinter.CTkFrame(master=chats_profiles)
                message_label = customtkinter.CTkLabel(master=m_frame, text=x[0], anchor='w')
                message_label.pack()
                m_frame.bind('<Enter>', enter)
                m_frame.bind('<Leave>', leave)
                chats_profiles.canvas.bind("<Button-1>", lambda event, id = x[1]: click(event, id))
                message_label.canvas.bind("<Button-1>", lambda event, id = x[1]: click(event, id))
                m_frame.grid(column = 0)
        func()

    chats_viewer()

def main():
    global app
    app.geometry("1600x900")
    app.title("CHAT")
    app.resizable(False, False)

    app.rowconfigure(0, weight = 1)
    app.rowconfigure(1, minsize = 75)
    
    chat()

    app.mainloop()

main()