import tkinter
from PIL import Image, ImageTk
import customtkinter
import logging
import functions_chat
import connect
import threading
import time
from tktooltip import ToolTip
import os
from tkinter import filedialog

mydb = connect.mydb
cursor = mydb.cursor(buffered=True)

customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.geometry("1600x900")
app.title("DISCARD")
app.resizable(False, False)

lastMessageID = 0
def chat():
    global DisplayedUserID
    global lastMessageID

    app.withdraw()
    app.deiconify()
    app.columnconfigure(0, minsize = 0, weight = 0)
    app.columnconfigure(1, minsize = 300, weight = 0) #Column for viewing chats
    app.columnconfigure(2, weight = 1) #Column for Viewing messages
    app.columnconfigure(3, minsize = 300, weight = 0) #Column for selected chat profile info

    switcher = customtkinter.CTkFrame(master=app, width=75) #Frame for Switcher between chat and DMs
    chats = customtkinter.CTkFrame(master=app, width=100) #All Chats
    chat_window = customtkinter.CTkFrame(master=app) #Frame for viewing messages
    profile = customtkinter.CTkFrame(master=app) #Frame for Profile
    
    #Configures grid for all the frames in window
    chats.grid(column = 1, row = 0, sticky = 'nsew')
    chat_window.grid(column = 2, row = 0, sticky = 'nsew')
    profile.grid(column = 3, row = 0, sticky = 'nsew')

    #Message viewer
    def message_viewer(id):
        nameHolder = customtkinter.CTkFrame(master=chat_window, height = 75, fg_color='black')
        entry = customtkinter.CTkEntry(master=chat_window)
        messages_canvas = tkinter.Canvas(master=chat_window, borderwidth=0, highlightthickness=0, background="#343638")
        messages = customtkinter.CTkFrame(master=messages_canvas, fg_color="#343638")
        messages_scrollbar = customtkinter.CTkScrollbar(master=chat_window, command=messages_canvas.yview)
        messages_canvas.configure(yscrollcommand=messages_scrollbar.set)
        
        nameHolder.grid(row = 0, column = 0, columnspan = 3, sticky = 'nsew')
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
        nameHolder.rowconfigure(0, weight = 1)

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

        users = functions_chat.get_dm_users()
        for user in users:
            if user[1] == id:
                fileName = 'ProfilePictures/' + str(user[0]) + '.png'
                nameLabel = customtkinter.CTkLabel(nameHolder, text = user[2], text_font = ('uni sans', 25, 'bold'), anchor = 'w', justify = 'left')
                username = customtkinter.CTkLabel(profile, text=user[2], height=8, text_font=('uni sans', 17), width = 300, justify = 'center')
                
        profilePicture = ImageTk.PhotoImage(Image.open(fileName).resize((50, 50)))
        pictureLabel = customtkinter.CTkLabel(nameHolder, image=profilePicture, width = 70)
        pictureLabel.image = profilePicture
        pictureLabel.grid(row = 0, column = 0, sticky = 'nsew')
        nameLabel.grid(row = 0, column  = 1)

        messages_canvas.update_idletasks()
        messages_canvas.yview_moveto(1.0)

        profilePicture = ImageTk.PhotoImage(Image.open(fileName).resize((100, 100)))
        profpic = customtkinter.CTkLabel(profile, image=profilePicture, width = 100)#customtkinter.CTkButton(profile, fg_color='white', bg_color='black', text='', image=profilePicture, border_width=0, width=50, height=55)
        profpic.image = profilePicture
        profpic.place(x=100, y=60)

        def unfriend(id):
            functions_chat.unfriend(id)
            chat()

        username.place(x=0, y=180)

        unfr = customtkinter.CTkButton(profile, text="UNFRIEND", width=220, corner_radius=20, fg_color='#292929', border_width=2, border_color='teal', hover_color='teal', command= lambda: unfriend(id))
        unfr.place(x=40, y=210)

        abt = customtkinter.CTkFrame(profile, fg_color='#292929', width=280, height=100)
        abt.place(x=10, y=270)
        abtme = customtkinter.CTkLabel(abt, text='About me', text_font=('uni sans', 14), width=20)
        abtme.place(x=10, y=10)

        desc = customtkinter.CTkLabel(abt, text="About me isn't working yet", fg_color='#292929', corner_radius=10, width=240, height=75, anchor='nw')
        desc.place(x=0, y=35)

        def update():
            global DisplayedUserID
            global lastMessageID
            m = functions_chat.get_latest_dm_messages(DisplayedUserID, lastMessageID) #Returns list in the format [(MessageID, MessageText, SenderUserID, DMID, SenderUsername), (MessageID, MessageText, SenderUserID, DMID, SenderUsername)]
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
                pictureLabel = customtkinter.CTkLabel(master=m_frame, image=profilePicture)
                pictureLabel.image = profilePicture
                pictureLabel.grid(row = 0, column = 0, sticky = 'w')

                m_frame.bind('<Enter>', enter)
                m_frame.bind('<Leave>', leave)
                m_frame.canvas.bind("<Button-1>", lambda event, id = x[1]: click(event, id))
                m_frame.grid(column = 0, sticky = 'ew')
            
        func()

    chats_viewer()

def user_profile():
    app.columnconfigure(0, weight = 1)
    #Color background on top
    frame1 = tkinter.Frame(app, height=200, width=2000, border=0, bg='navy blue')  # 003366 #ec4d37
    prof = customtkinter.CTkLabel(frame1, text='My Profile', text_font=('Uni Sans', 30, 'bold'))
    prof.place(x=250, y=80)
    frame1.place(x=0, y=0)

    masterFrame = customtkinter.CTkFrame(app, width = 1100, height = 500)
    masterFrame.place(x = 250, y = 160)

    def Edit(win, det, a, b):
        edit = customtkinter.CTkButton(win, width=20, height=20, text='Edit', fg_color='teal', text_color='white', hover_color='teal', command=lambda: edit_clicked(det))
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

    profilePicturePath = "ProfilePictures/" + str(functions_chat.CurrentUserID) + ".png"
    profilePicture = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((250, 250)))
    pictureLabel = customtkinter.CTkLabel(masterFrame, image=profilePicture)
    pictureLabel.image = profilePicture
    pictureLabel.place(x = 40, y = 50)
    
    def changeFile():
        nonlocal profilePicturePath
        nonlocal pictureLabel
        filetypes = (
        ('image files', '*.png'),
        ('All files', '*.*')
        )
        profilePicturePath = filedialog.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes)
        img2 = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((250, 250)))
        pictureLabel.configure(image=img2)
        pictureLabel.image = img2
        with open(profilePicturePath, 'rb') as file:
                binaryData = file.read()
        functions_chat.update_pfp(binaryData)

    fileChange = customtkinter.CTkButton(masterFrame, text='Change Profile picture', command=changeFile, width = 250)
    fileChange.place(x = 40, y = 340)


    aboutFrame = customtkinter.CTkFrame(masterFrame, height=120, width=200, bg='#292929')
    # about
    def about():
        aboutFrame.place(x=745, y=50)

        aboutme = customtkinter.CTkLabel(aboutFrame, text='About Me', text_color='white', width=40,  text_font=('uni sans', 15, 'bold'))
        aboutme.place(x=10, y=5)

        abt = customtkinter.CTkLabel(aboutFrame, height=80, width=180, text = functions_chat.get_bio(functions_chat.CurrentUserID)[1], anchor='nw', justify = 'left')
        abt.place(x=10, y=30)
    
    def execute_about_edit(aboutStr):
        functions_chat.update_bio(aboutStr)
        for widget in aboutFrame.winfo_children():
            widget.destroy()
        aboutEditButton.configure(text = 'Edit About me', command=about_edit)
        about()

    def about_edit():
        for widget in aboutFrame.winfo_children():
            widget.destroy()
        
        aboutFrame.place(x=745, y=50)

        aboutme = customtkinter.CTkLabel(aboutFrame, text='About Me', text_color='white', width=40, text_font=('Uni Sans', 13))
        aboutme.place(x=10, y=5)

        abt = customtkinter.CTkEntry(aboutFrame, height=80, width=180)
        abt.place(x=10, y=30)

        aboutEditButton.configure(text = 'Done', command = lambda: execute_about_edit(abt.get()))

    aboutEditButton = customtkinter.CTkButton(masterFrame, text = 'Edit About me', width = 200, command=about_edit)
    aboutEditButton.place(x = 745, y = 180)

    detail = customtkinter.CTkFrame(masterFrame, width=425, height=250)  # fg_color='black'

    def details(win):
        nonlocal detail
        detail.place(x=310, y=50)
        info = customtkinter.CTkLabel(detail, text='Account Info', width=20, text_font=('uni sans', 20, 'bold'))
        info.place(x=15, y=10)

        credentials = functions_chat.get_user(functions_chat.email)

        email = customtkinter.CTkLabel(detail, width=20, height=10, text='Email ID', text_font=('uni sans', 15, 'bold'))
        email.place(x=15, y=50)

        emailLabel = customtkinter.CTkLabel(detail, text = credentials[1], anchor = 'w', justify = 'left', text_font=('uni sans', 12))
        emailLabel.place(x=15, y=75)

        username = customtkinter.CTkLabel(detail, width=10, height=10, text='Username', text_font=('uni sans', 15, 'bold'))
        username.place(x=15, y=115)

        usernameLabel = customtkinter.CTkLabel(detail, text=credentials[2], anchor = 'w', justify = 'left', text_font=('uni sans', 12))
        usernameLabel.place(x=15, y=140)

        password = customtkinter.CTkLabel(detail, width=20, height=10, text='Password', text_font=('uni sans', 15, 'bold'))
        password.place(x=15, y=180)

        passwordLabel = customtkinter.CTkLabel(detail, text='*****', anchor = 'w', justify = 'left', text_font=('uni sans', 12))
        passwordLabel.place(x=15, y=205)
    
    def execute_edit(username, email, password):
        nonlocal detail
        functions_chat.profile_update(email, username, password)
        for widget in detail.winfo_children():
            widget.destroy()
        details(masterFrame)
        editProfileButton.configure(text = 'Edit Account details', command=lambda: details_edit(masterFrame))

    def details_edit(win):
        nonlocal detail
        nonlocal editProfileButton

        editProfileButton.configure(text = 'Done', command = lambda: execute_edit(usernameEntry.get(), emailEntry.get(), passwordEntry.get()))

        for widget in detail.winfo_children():
            widget.destroy()

        info = customtkinter.CTkLabel(detail, text='Account Info', width=20, text_font=('uni sans', 20, 'bold'))
        info.place(x=15, y=10)

        credentials = functions_chat.get_user(functions_chat.email)

        email = customtkinter.CTkLabel(detail, width=20, height=10, text='Email ID', text_font=('uni sans', 15, 'bold'))
        email.place(x=15, y=50)

        emailEntry = customtkinter.CTkEntry(detail, width=350, height=15, fg_color='#292929', border_width=2, corner_radius=15, state='normal')
        emailEntry.insert(0, credentials[1])
        emailEntry.place(x=15, y=80)

        username = customtkinter.CTkLabel(detail, width=10, height=10, text='Username', text_font=('uni sans', 15, 'bold'))
        username.place(x=15, y=115)

        usernameEntry = customtkinter.CTkEntry(detail, width=350, height=15, fg_color='#292929', border_width=2, corner_radius=15, state='normal')
        usernameEntry.insert(0, credentials[2])
        usernameEntry.place(x=15, y=145)

        password = customtkinter.CTkLabel(detail, width=20, height=10, text='Password', text_font=('uni sans', 15, 'bold'))
        password.place(x=15, y=180)

        passwordEntry = customtkinter.CTkEntry(detail, width=350, height=15, fg_color='#292929', border_width=2, corner_radius=15, state='normal')
        passwordEntry.insert(0, credentials[3])
        passwordEntry.place(x=15, y=210)    

    editProfileButton = customtkinter.CTkButton(masterFrame, width = 425, text = 'Edit Account details', command=lambda: details_edit(masterFrame))
    editProfileButton.place(x = 310, y = 310)

    def log_out(win):
        def delete():
            os.remove('credentials.txt')
            app.destroy()

        lo = Image.open(r"C:\Users\Sanje\Downloads\logout.png")
        lo_resize = lo.resize((40, 40))
        lo1 = ImageTk.PhotoImage(lo_resize)
        logout = customtkinter.CTkButton(win, width=125, height=50, image=lo1, fg_color='#292929', text='Log Out', compound='top', command = delete)
        logout.place(x=310, y=355)

    about()
    details(masterFrame)
    log_out(masterFrame)

def add_dms():

    def search():
        email = userSearchEntry.get()
        user = functions_chat.get_user(email)
        bio = functions_chat.get_bio(user[0])
        for widget in userInfoFrame.winfo_children():
            widget.destroy()
        
        profilePicturePath = "ProfilePictures/" + str(user[0]) + ".png"
        profilePicture = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((250, 250)))
        pictureLabel = customtkinter.CTkLabel(userInfoFrame, image=profilePicture)
        pictureLabel.image = profilePicture
        pictureLabel.place(x = 20, y = 75)

        usernameTitleLabel = customtkinter.CTkLabel(userInfoFrame, text="USERNAME", justify='left', anchor='w', text_font = ('uni sans', 20, 'bold'))
        usernameLabel = customtkinter.CTkLabel(userInfoFrame, text = user[2], justify='left', anchor='w', text_font = ('uni sans', 15))
        bioTitleLabel = customtkinter.CTkLabel(userInfoFrame, text = "ABOUT ME", justify='left', anchor='w', text_font = ('uni sans', 20, 'bold'))
        bioLabel = customtkinter.CTkLabel(userInfoFrame, text = bio[1], width = 300, justify='left', anchor='w', text_font = ('uni sans', 15))
        
        def add_friend():
            functions_chat.new_dm(user[0])
            addFriendButton.configure(state = 'disabled')
            warningLabel.configure(text = 'added friend')

        
        addFriendButton = customtkinter.CTkButton(userInfoFrame, text = 'Add Friend', width = 100, state='normal', command=add_friend)
        warningLabel = customtkinter.CTkLabel(userInfoFrame, text = '', anchor='w', justify='left')
        usernameTitleLabel.place(x = 300, y = 75)
        usernameLabel.place(x = 300, y = 110)
        bioTitleLabel.place(x = 300, y = 180)
        bioLabel.place(x = 300, y = 215)
        addFriendButton.place(x = 300, y = 300)
        warningLabel.place(x = 410, y = 300)
        friends = functions_chat.get_dm_users()
        for friend in friends:
            if friend[0] == user[0]:
                addFriendButton.configure(state = 'disabled')
                warningLabel.configure(text = 'user is already your friend')

    app.columnconfigure(0, weight = 1)
    masterFrame = customtkinter.CTkFrame(app)
    masterFrame.grid(row = 0, column = 0, columnspan = 5, sticky = 'nsew')
    bg = customtkinter.CTkFrame(masterFrame, height=200, width=2000, border=0, fg_color='purple')  # 003366 #ec4d37
    addFriendsLabel = customtkinter.CTkLabel(bg, text='Add Friends', text_font=('Uni Sans', 30, 'bold'))
    userInfoFrame = customtkinter.CTkFrame(masterFrame, width = 800, height = 400)
    userSearchEntry = customtkinter.CTkEntry(masterFrame, width = 600, height = 40, placeholder_text='Enter email')
    searchButton = customtkinter.CTkButton(app, text='Search', command=search, width = 190, height = 40)
    messageLabel = customtkinter.CTkLabel(userInfoFrame, text = 'Find new friends', text_font=('Uni Sans', 20), width = 200, justify = 'center')
    messageLabel.place(x = 300, y = 200)
    userInfoFrame.place(x = 400, y = 160)
    userSearchEntry.place(x = 400, y = 610)
    searchButton.place(x = 1010, y = 610)
    bg.place(x=0, y=0)
    addFriendsLabel.place(x=250, y=80)

def mode():
    app.rowconfigure(0, weight = 1)
    app.rowconfigure(1, minsize = 10)
    modeSelecter = customtkinter.CTkFrame(master=app)
    modeSelecter.columnconfigure(0, weight = 1)
    modeSelecter.columnconfigure(1, weight = 1)
    modeSelecter.columnconfigure(2, weight = 1)
    modeSelecter.grid(row = 1, columnspan = 4, sticky = 'ew')

    chatMode = customtkinter.CTkFrame(master=modeSelecter, height=75)
    friendsMode = customtkinter.CTkFrame(master=modeSelecter, height=75)
    settingsMode = customtkinter.CTkFrame(master=modeSelecter, height=75)

    chatMode.columnconfigure(0, weight = 1)
    friendsMode.columnconfigure(0, weight = 1)
    settingsMode.columnconfigure(0, weight = 1)

    chatsPicture = ImageTk.PhotoImage(Image.open('ImageResources/chats.png').resize((70, 70)))
    chatsLabel = customtkinter.CTkLabel(chatMode, image=chatsPicture, width = 75)
    chatsLabel.image = chatsPicture
    chatsLabel.grid(row = 0, column = 0, pady = 5)

    friendsPicture = ImageTk.PhotoImage(Image.open('ImageResources/friends.png').resize((70, 70)))
    friendsLabel = customtkinter.CTkLabel(friendsMode, image = friendsPicture, width = 75)
    friendsLabel.image = friendsPicture
    friendsLabel.grid(row = 0, column = 0, pady = 5)

    settingsPicture = ImageTk.PhotoImage(Image.open('ImageResources/settings.png').resize((70, 70)))
    settingsLabel = customtkinter.CTkLabel(settingsMode, image = settingsPicture, width = 75)
    settingsLabel.image = settingsPicture
    settingsLabel.grid(row = 0, column = 0, pady = 5)

    def enter(event):
        event.widget.configure(fg_color='yellow')
    def leave(event):
        event.widget.configure(fg_color='#343638')
    def click(event, id):
        for widget in app.winfo_children():
            widget.destroy()
        mode()
        global flag
        flag = False
        if id == 0:
            chat()
        elif id == 1:
            add_dms()
        elif id == 2:
            user_profile()
        
    chatMode.bind('<Enter>', enter)
    chatMode.bind('<Leave>', leave)
    chatMode.canvas.bind("<Button-1>", lambda event, id = 0: click(event, id))

    friendsMode.bind('<Enter>', enter)
    friendsMode.bind('<Leave>', leave)
    friendsMode.canvas.bind("<Button-1>", lambda event, id = 1: click(event, id))

    settingsMode.bind('<Enter>', enter)
    settingsMode.bind('<Leave>', leave)
    settingsMode.canvas.bind("<Button-1>", lambda event, id = 2: click(event, id))

    chatMode.grid(column = 0, row = 0, sticky = 'nsew')
    friendsMode.grid(column = 1, row = 0, sticky = 'nsew')
    settingsMode.grid(column = 2, row = 0, sticky = 'nsew')

def on_close(): 
    global flag
    flag = False 
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)

def main():
    
    mode()
    chat()

    app.mainloop()

main()