import tkinter
from PIL import Image, ImageTk
import customtkinter
import logging
import functions_chat
import connect
import threading
import time

mydb = connect.mydb
cursor = mydb.cursor(buffered=True)

app = customtkinter.CTk()
lastMessageID = 0
def chat():
    global DisplayedUserID
    global lastMessageID

    app.withdraw()
    app.deiconify()
    app.columnconfigure(0, minsize = 75, weight = 0) #Column for sidebar/switcher between groups and DMs
    app.columnconfigure(1, minsize = 300, weight = 0) #Column for viewing chats
    app.columnconfigure(2, weight = 1) #Column for Viewing messages
    app.columnconfigure(3, minsize = 300, weight = 0) #Column for selected chat profile info

    switcher = customtkinter.CTkFrame(master=app, width=75) #Frame for Switcher between chat and DMs
    chats = customtkinter.CTkFrame(master=app, width=100) #All Chats
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
        messages = customtkinter.CTkFrame(master=messages_canvas, fg_color="#343638")
        messages_scrollbar = customtkinter.CTkScrollbar(master=chat_window, command=messages_canvas.yview)
        messages_canvas.configure(yscrollcommand=messages_scrollbar.set)
        
        entry.grid(row = 2, padx = 10, pady = 10, sticky = 'ew')
        messages_canvas.grid(row = 1, column= 0, sticky='nsew')
        messages_scrollbar.grid(row = 1, column = 1, sticky = 'nse')
        messages_canvas.create_window((0,0), window=messages, width=0, anchor="nw")

        def onFrameConfigure(messages_canvas):
            '''Reset the scroll region to encompass the inner frame'''
            messages_canvas.configure(scrollregion=messages_canvas.bbox("all"))

        messages.bind("<Configure>", lambda event, messages_canvas=messages_canvas: onFrameConfigure(messages_canvas))

        chat_window.rowconfigure(0, minsize = 75)
        chat_window.rowconfigure(1, weight = 1)
        chat_window.columnconfigure(0, weight = 1)

        m = functions_chat.get_dm_messages(id) #Returns list in the format [(MessageID, MessageText, SenderUserID, DMID, SenderUsername), (MessageID, MessageText, SenderUserID, DMID, SenderUsername)]
        global lastMessageID
        
        for x in m:
            m_frame = customtkinter.CTkFrame(master=messages, fg_color="#343638", pady = 10)

            fileName = 'ProfilePictures/' + str(x[2]) + '.png'
            profilePicture = ImageTk.PhotoImage(Image.open(fileName).resize((50, 50)))
            pictureLabel = customtkinter.CTkLabel(m_frame, image=profilePicture, width = 70)
            pictureLabel.image = profilePicture
            pictureLabel.grid(row = 0, column = 0, rowspan = 2, sticky = 'n')

            user_label = customtkinter.CTkLabel(master=m_frame, text=x[5], anchor='w', justify='left', text_font=('uni sans', 15, 'bold'), width=0)
            timestamp_label = customtkinter.CTkLabel(master=m_frame, text=x[4], anchor='w', justify='left', text_font=('uni sans', 8), text_color='grey')
            message_label = customtkinter.CTkLabel(master=m_frame, text=x[1], anchor='w', justify='left', text_font=('calibri', 12), wraplength=800)
            m_frame.columnconfigure(1, weight = 1)
            user_label.grid(column=1, row = 0, sticky = 'w')
            timestamp_label.grid(column = 2, row = 0, sticky = 'w', padx = 5)
            message_label.grid(column = 1, row = 1, sticky = 'w', columnspan = 2)
            m_frame.grid(column=0, sticky = 'w')
            lastMessageID = x[0]
        messages_canvas.update_idletasks()
        messages_canvas.yview_moveto(1.0)
        
        def update():
            global DisplayedUserID
            global lastMessageID
            m = functions_chat.get_latest_dm_messages(DisplayedUserID, lastMessageID) #Returns list in the format [(MessageID, MessageText, SenderUserID, DMID, SenderUsername), (MessageID, MessageText, SenderUserID, DMID, SenderUsername)]
            for x in m:
                m_frame = customtkinter.CTkFrame(master=messages, fg_color="yellow", pady = 10, padx = 0)
                fileName = 'ProfilePictures/' + str(x[2]) + '.png'
                profilePicture = ImageTk.PhotoImage(Image.open(fileName).resize((50, 50)))
                pictureLabel = customtkinter.CTkLabel(m_frame, image=profilePicture, bg_color= 'blue')
                pictureLabel.image = profilePicture
                pictureLabel.grid(row = 0, column = 0, sticky = 'w', rowspan = 2)

                user_label = customtkinter.CTkLabel(master=m_frame, text=x[5], anchor='w', justify='left', text_font=('uni sans', 15, 'bold'), width=0)
                timestamp_label = customtkinter.CTkLabel(master=m_frame, text=x[4], anchor='w', justify='left', text_font=('uni sans', 8), text_color='grey')
                message_label = customtkinter.CTkLabel(master=m_frame, text=x[1], anchor='w', justify='left', text_font=('calibri', 12), wraplength=800)
                m_frame.columnconfigure(1, weight = 1)
                user_label.grid(column=0, row = 0, sticky = 'w')
                timestamp_label.grid(column = 1, row = 0, sticky = 'w', padx = 5)
                message_label.grid(column = 0, row = 1, sticky = 'w', columnspan = 2)
                m_frame.grid(column=0, sticky = 'w')
                lastMessageID = x[0]
            messages_canvas.update_idletasks()
            messages_canvas.yview_moveto(1.0)


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
        
        def get_new_messages():
            global DisplayedUserID
            global lastMessageID
            global flag
            flag = True
            while flag:
                time.sleep(2)
                cursor.execute(f"SELECT * FROM `dm messages` WHERE `dm id` = {DisplayedUserID} AND `message id` > {lastMessageID}")
                mydb.commit()
                recs = cursor.fetchall()
                if recs != []:
                    update()
        
        t1 = threading.Thread(target=get_new_messages)
        t1.start()

    # Chats
    def chats_viewer():
        
        chats_canvas = tkinter.Canvas(master=chats, borderwidth=0, highlightthickness=0, background="#343638")
        chats_profiles = customtkinter.CTkFrame(master=chats_canvas, fg_color = '#343638', width=1000)
        chat_scrollbar = customtkinter.CTkScrollbar(master=chats, command=chats_canvas.yview)
        chats_canvas.configure(yscrollcommand=chat_scrollbar.set)

        chats_canvas.grid(row = 0, column= 0, sticky='nsew')
        chat_scrollbar.grid(row = 0, column = 1, sticky = 'nse')
        chats_profiles.columnconfigure(0, weight = 1)
        chats_canvas.create_window((0, 0), window=chats_profiles, anchor="nw", width = 380)

        def onFrameConfigure(chats_canvas):
            '''Reset the scroll region to encompass the inner frame'''
            chats_canvas.configure(scrollregion=chats_canvas.bbox("all"))

        chats_profiles.bind("<Configure>", lambda event, chats_canvas=chats_canvas: onFrameConfigure(chats_canvas))

        chats.rowconfigure(0, weight = 1)

        def func():
            m = functions_chat.get_dm_users() #Returns list in the format [(UserID, DMID, UserName, ProfilePicture), (UserID, DMID, UserName, ProfilePicture)]
            def enter(event):
                event.widget.configure(fg_color='black')
            def leave(event):
                event.widget.configure(fg_color='#343638')
            def click(event, id):
                global DisplayedUserID
                for widget in chat_window.winfo_children():
                    widget.destroy()
                DisplayedUserID = id
                message_viewer(id)
            for x in m:
                fileName = 'ProfilePictures/' + str(x[0]) + '.png'
                with open(fileName, 'wb') as file:
                    file.write(x[3])

                m_frame = customtkinter.CTkFrame(master=chats_profiles, fg_color='#343638', corner_radius= 5)
                message_label = customtkinter.CTkLabel(master=m_frame, text=x[2], anchor='w', text_font=('Uni Sans', 15))
                message_label.grid(row = 0, column = 1, pady = 30)

                profilePicture = ImageTk.PhotoImage(Image.open(fileName).resize((65, 65)))
                pictureLabel = customtkinter.CTkLabel(m_frame, image=profilePicture)
                pictureLabel.image = profilePicture
                pictureLabel.grid(row = 0, column = 0, sticky = 'w')

                m_frame.bind('<Enter>', enter)
                m_frame.bind('<Leave>', leave)
                m_frame.canvas.bind("<Button-1>", lambda event, id = x[1]: click(event, id))
                m_frame.grid(column = 0, sticky = 'ew')
            
        func()

    chats_viewer()

def user_profile():
    
    def Edit(win, det, a, b):
        edit = customtkinter.CTkButton(win, width=20, height=20, text='Edit', fg_color='teal', text_color='white', hover_color='teal', command=lambda: edit_clicked(det) )
        edit.place(x=a, y=b)

        def edit_clicked(entry):
            nonlocal edit
            fl = True
            if fl:
                edit.configure(text='Done')
                entry.configure(state='normal')

            def edit_clicked_twice():
                nonlocal edit
                nonlocal det
                edit.configure(text='Edit')
                entry.configure(state='disabled')
            edit.configure(command=edit_clicked_twice)

    #Color background on top
    def frame1(win):
        frame1 = tkinter.Frame(win, height=200, width=2000, border=0, bg='navy blue')  # 003366 #ec4d37
        prof = customtkinter.CTkLabel(frame1, text='My Profile', text_font=('Uni Sans', 30, 'bold'))
        prof.place(x=250, y=100)
        frame1.place(x=0, y=0)

    #Profile Picture
    def frame2(win):
        pfp = Image.open(r"C:\Users\Sanje\Downloads\pfp.jpg")
        pfp_resize = pfp.resize((200, 300))
        pfp1 = ImageTk.PhotoImage(pfp_resize)
        frame2 = tkinter.Frame(win, height=400, width=200, bg='violet')
        frame2.place(x=40, y=50)
        profpic = customtkinter.CTkButton(frame2, image=pfp1, fg_color='black', corner_radius=0, state='disabled')
        profpic.place(x=0, y=0)

    # about
    def about(win):
        about = tkinter.Frame(win, height=120, width=200, bg='#292929')
        about.place(x=40, y=340)

        aboutme = customtkinter.CTkLabel(about, text='About Me', text_color='white', width=40, text_font=('Georgia', 13))
        aboutme.place(x=10, y=5)

        abt = customtkinter.CTkTextbox(about, height=80, width=180)
        abt.place(x=10, y=30)

    def details(win):
        detail = customtkinter.CTkFrame(win, width=425, height=150)  # fg_color='black'
        detail.place(x=250, y=160)
        info = customtkinter.CTkLabel(detail, text='Account Info', width=20)
        info.place(x=10, y=5)

        emailEntry = customtkinter.CTkEntry(detail, width=350, height=27, fg_color='#292929', border_width=2, corner_radius=15, state='disabled')
        emailEntry.place(x=15, y=40)

        email = customtkinter.CTkLabel(detail, width=20, height=10, text='Email ID')
        email.place(x=25, y=33)
        Edit(detail, emailEntry, 370, 42)

        usernameEntry = customtkinter.CTkEntry(detail, width=350, height=27, fg_color='#292929', border_width=2, corner_radius=15, state='disabled')
        usernameEntry.place(x=15, y=80)

        usernameLabel = customtkinter.CTkLabel(detail, width=10, height=10, text='Username')
        usernameLabel.place(x=25, y=70)
        Edit(detail, usernameEntry, 370, 82)

        passwordEntry = customtkinter.CTkEntry(detail, width=350, height=27, fg_color='#292929', border_width=2, corner_radius=15, state='disabled')
        passwordEntry.place(x=15, y=120)

        passwordLabel = customtkinter.CTkLabel(detail, width=20, height=10, text='Password')
        passwordLabel.place(x=25, y=110)
        Edit(detail, passwordEntry, 370, 122)

    def socials(win):
        social = customtkinter.CTkFrame(win, height=185, width=260)
        social.place(x=682, y=160)

        fbent = customtkinter.CTkEntry(social, width=225, height=23, fg_color='#292929', border_width=1, placeholder_text='Facebook profile', placeholder_text_color='silver', corner_radius=5, text_color='silver')
        fbent.place(x=5, y=30)

        igent = customtkinter.CTkEntry(social, width=225, height=23, fg_color='#292929', border_width=1, placeholder_text='Instagram profile', placeholder_text_color='silver', corner_radius=5, text_color='silver')
        igent.place(x=5, y=60)

        ytent = customtkinter.CTkEntry(social, width=225, height=23, fg_color='#292929', border_width=1, placeholder_text='YouTube channel', placeholder_text_color='silver', corner_radius=5, text_color='silver')
        ytent.place(x=5, y=90)

        twent = customtkinter.CTkEntry(social, width=225, height=23, fg_color='#292929', border_width=1, placeholder_text='Twitter account', placeholder_text_color='silver', corner_radius=5, text_color='silver')
        twent.place(x=5, y=120)

        otent = customtkinter.CTkEntry(social, width=225, height=23, fg_color='#292929', border_width=1, placeholder_text='yourwebsite.com', placeholder_text_color='silver', corner_radius=5, text_color='silver')
        otent.place(x=5, y=150)

    def status(win):
        stat = customtkinter.CTkFrame(win, width=425, height=30)
        stat.place(x=250, y=317)
        statuslabel = customtkinter.CTkLabel(stat, width=20, text='Status : ')
        statuslabel.place(x=10, y=2)
        options = ['Available', 'Away', 'Busy', 'Invisible', 'Do Not Disturb']
        st = customtkinter.CTkOptionMenu(stat, values=options, width=250, height=20, fg_color='#404040', button_color='teal')
        st.place(x=65, y=5)
        bell = Image.open(r"C:\Users\Sanje\Downloads\notif.png")
        bell_resize = bell.resize((20, 20))
        bell1 = ImageTk.PhotoImage(bell_resize)
        notif = customtkinter.CTkButton(stat, width=7, height=7, fg_color='#292929', image=bell1, text='', state='disabled')
        notif.place(x=325, y=2)
        notification = customtkinter.CTkSwitch(stat, width=50, height=20, onvalue='on', offvalue='off', fg_color='teal', text='')
        notification.place(x=360, y=3)

    def switch(win):
        sw = Image.open(r"C:\Users\Sanje\Downloads\switch.png")
        sw_resize = sw.resize((40, 40))
        sw1 = ImageTk.PhotoImage(sw_resize)
        switch_acc = customtkinter.CTkButton(win, width=50, height=40, image=sw1, fg_color='#292929', text='Switch Accounts', compound='top')
        switch_acc.place(x=250, y=355)

    def log_out(win):
        lo = Image.open(r"C:\Users\Sanje\Downloads\logout.png")
        lo_resize = lo.resize((40, 40))
        lo1 = ImageTk.PhotoImage(lo_resize)
        logout = customtkinter.CTkButton(win, width=125, height=50, image=lo1, fg_color='#292929', text='Log Out', compound='top')
        logout.place(x=375, y=355)

    frame1(app)
    frame2(app)
    about(app)
    details(app)
    socials(app)
    status(app)
    switch(app)
    log_out(app)

def add_dms():
    app.columnconfigure(0, weight = 1)
    masterFrame = customtkinter.CTkFrame(app)
    masterFrame.grid(row = 0, column = 0, columnspan = 5, sticky = 'nsew')
    userSearch = customtkinter.CTkEntry(masterFrame, height = 35, width = 600)
    userSearch.place(x = 450, y = 50)
    goButton = customtkinter.CTkButton(app, text='Search') 
    goButton.place(x = 600, y = 10)

def mode():
    app.rowconfigure(0, weight = 1)
    app.rowconfigure(1, minsize = 10)
    modeSelecter = customtkinter.CTkFrame(master=app)
    modeSelecter.columnconfigure(0, weight = 1)
    modeSelecter.columnconfigure(1, weight = 1)
    #modeSelecter.grid_propagate()
    modeSelecter.grid(row = 1, columnspan = 4, sticky = 'ew')

    chatMode = customtkinter.CTkFrame(master=modeSelecter, height=75)
    friendsMode = customtkinter.CTkFrame(master=modeSelecter, height=75)

    def enter(event):
        event.widget.configure(fg_color='yellow')
    def leave(event):
        event.widget.configure(fg_color='#343638')
    def click(event, id):
        for widget in app.winfo_children():
            widget.destroy()
        mode()
        #add_dms()
        chat()
    
    chatMode.bind('<Enter>', enter)
    chatMode.bind('<Leave>', leave)
    chatMode.canvas.bind("<Button-1>", lambda event, id = 0: click(event, id))

    friendsMode.bind('<Enter>', enter)
    friendsMode.bind('<Leave>', leave)
    friendsMode.canvas.bind("<Button-1>", lambda event, id = 1: click(event, id))

    chatMode.grid(column = 0, row = 0, sticky = 'nsew')
    friendsMode.grid(column = 1, row = 0, sticky = 'nsew')

def on_close(): 
    global flag
    flag = False 
    app.destroy()

def main():
    global app
    app.geometry("1600x900")
    app.title("DISCARD")
    app.resizable(False, False)
    
    mode()
    #chat()
    add_dms()

    app.protocol("WM_DELETE_WINDOW", on_close)

    app.mainloop()

main()