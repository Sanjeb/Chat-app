import tkinter
from PIL import Image, ImageTk
import customtkinter
import logging
import functions_chat
import connect
import threading
import time
import datetime

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

    switcher = customtkinter.CTkFrame(master=app, width=25) #Frame for Switcher between chat and DMs
    chats = customtkinter.CTkFrame(master=app, width=100) #All Chats
    chat_window = customtkinter.CTkFrame(master=app) #Frame for viewing messages
    profile = customtkinter.CTkFrame(master=app) #Frame for Profile
    
    #Configures grid for all the frames in window
    chats.grid(column = 1, row = 0, sticky = 'nsew')
    chat_window.grid(column = 2, row = 0, sticky = 'nsew')
    profile.grid(column = 3, row = 0, sticky = 'nsew')

    #Message viewer
    def message_viewer(id):
        nameHolder = customtkinter.CTkFrame(master=chat_window, height = 75, fg_color='yellow')
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
##    frame1 = tkinter.Frame(app, height=200, width=2000, border=0, bg='navy blue')  # 003366 #ec4d37
##    prof = customtkinter.CTkLabel(frame1, text='My Profile', text_font=('Uni Sans', 30, 'bold'))
##    prof.place(x=250, y=80)
##    frame1.place(x=0, y=0)

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
        img2 = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((300,300)))
        pictureLabel.configure(image=img2)
        pictureLabel.image = img2
        with open(profilePicturePath, 'rb') as file:
                binaryData = file.read()
        functions_chat.update_pfp(binaryData)
    
    def other_handles_clicked():
        global editProfileButton
        bar.place(x=910,y=150)
        acct_info.configure(text_color = 'gray')
        other.configure(text_color = 'white')
        for widget in acctframe.winfo_children():
            widget.destroy()
        editProfileButton.destroy()    
        other_handles(prof)

    def details_clicked():
        global editmedia
        bar.place(x=550,y=150)
        other.configure(text_color = 'gray')
        acct_info.configure(text_color = 'white')
        for widget in acctframe.winfo_children():
            widget.destroy()
        editmedia.destroy()
        details()

    def execute_edit(username, email, password):
        nonlocal acctframe
        functions_chat.profile_update(email, username, password)
        for widget in acctframe.winfo_children():
            widget.destroy()
        details()
        editProfileButton.configure(text = 'Edit Account details', command=lambda: details_edit(acctframe))

    def details_edit(win):
        nonlocal acctframe
        

        editProfileButton.configure(text = 'Done', command = lambda: execute_edit(unent.get(), emailent.get(), pwent.get()))

        for widget in acctframe.winfo_children():
            widget.destroy()

##        info = customtkinter.CTkLabel(detail, text='Account Info', width=20, text_font=('uni sans', 20, 'bold'))
##        info.place(x=15, y=10)

        credentials = functions_chat.get_user(functions_chat.email)
        emailent = customtkinter.CTkEntry(acctframe,
                            width = 325,
                            height = 27,
                            fg_color = '#151515',
                            border_width= 0,
                            corner_radius = 15,
                            text_font = ('Bahnschrift SemiLight',18))
        emailent.insert(0,credentials[1])
        emailent.place(x=60,y=100)

        email = customtkinter.CTkLabel(acctframe,
                         width=20,
                         height=7,
                         text='Email ID',
                         text_font = ('smth',18,'bold'))
        email.place(x=75, y = 65)

        unent = customtkinter.CTkEntry(acctframe,
                            width = 325,
                            height = 27,
                            fg_color = '#151515',
                            border_width= 0,
                            corner_radius = 15,
                         text_font = ('Bahnschrift SemiLight',18))
        unent.place(x=60,y=200)
        unent.insert(0,credentials[2])

        un = customtkinter.CTkLabel(acctframe,
                      width=10,
                      height=7,
                      text='Username',
                      text_font = ('smth',18,'bold'))
        un.place(x=75, y = 165)

        pwent = customtkinter.CTkEntry(acctframe,
                            width = 325,
                            height = 27,
                            fg_color = '#151515',
                            border_width= 0,
                            corner_radius = 15,
                         text_font = ('Bahnschrift SemiLight',18))
        pwent.place(x=60,y=300)
        pwent.insert(0,credentials[3])

        pw = customtkinter.CTkLabel(acctframe,
                      width=20,
                      height=7,
                      text='Password',
                      text_font = ('smth',18,'bold'))
        pw.place(x=75, y = 265)
    


    profile_mainframe = customtkinter.CTkFrame(app,
                                width = 1600,
                                height = 900,
                                fg_color = '#202020',
                                corner_radius = 0)
    profile_mainframe.place(x=0, y=0)

    prof = customtkinter.CTkFrame(profile_mainframe,
                          width = 1400,
                          height = 700,
                          fg_color = '#101010',
                          corner_radius = 0)
    prof.place(x=100, y = 100)

    #the labels on top
    toplabel = customtkinter.CTkLabel(prof,
                        width=1400,
                        height = 150,
                        fg_color = '#0d98ba',
                        corner_radius = 0,
                        text = '')
    toplabel.place(x=0,y=0)

    myprofile = customtkinter.CTkLabel(prof,
                         width = 20,
                         height = 10,
                         fg_color = '#0d98ba',
                         text = 'My Profile',
                         text_color = 'white',
                         text_font = ('Bahnschrift SemiLight',23,'bold')) #Ebrima
    myprofile.place(x=20,y=15)

    acct_info = customtkinter.CTkButton(prof,
                         width = 15,
                         height = 10,
                         fg_color = '#101010',
                         text = 'Account Info',
                         text_color = 'white',
                         text_font = ('Bahnschrift SemiLight',17,'bold'),
                          hover_color = '#101010',
                          command=details_clicked)
    acct_info.place(x=550,y=155)

    other = customtkinter.CTkButton(prof,
                         width = 15,
                         height = 10,
                         fg_color = '#101010',
                         bg_color = '#101010',
                         text = 'Other Handles',
                         text_color = 'silver',
                         text_font = ('Bahnschrift SemiLight',17,'bold'),
                         hover_color = '#101010',
                      command = other_handles_clicked)
    other.place(x=900,y=155)

    #the bar on top of chosen tab
    bar = tkinter.Canvas(prof,
                 width = 150,
                 height = 10,
                 bg = '#101010',
                 highlightbackground = '#101010',
                 highlightthickness = 1)
    bar.place(x= 550, y = 150)
    bar.create_line(2,2,150,2,fill='#7df9ff',width = 3)

    acctframe = customtkinter.CTkFrame(prof,
                         width = 800,
                         height = 400,
                         fg_color = '#101010')
    acctframe.place(x=375,y = 200)


##
##    masterFrame = customtkinter.CTkFrame(app, width = 1100, height = 500)
##    masterFrame.place(x = 250, y = 160)
##

    profilePicturePath = "ProfilePictures/" + str(functions_chat.CurrentUserID) + ".png"
    profilePicture = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((300,300)))
    pictureLabel = customtkinter.CTkLabel(profile_mainframe, image=profilePicture)
    pictureLabel.image = profilePicture
    pictureLabel.place(x =150, y = 200)

    edit_icon = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\edit.png').resize((25,25)))
    change = customtkinter.CTkButton(prof,
                       width = 10,
                       image = edit_icon,
                       text = '',
                       fg_color = '#0d98ba',
                       bg_color = '#0d98ba',
                       corner_radius = 15,
                       command = changeFile)
    change.place(x= 350,y = 100)
    

##    fileChange = customtkinter.CTkButton(masterFrame, text='Change Profile picture', command=changeFile, width = 250)
##    fileChange.place(x = 40, y = 340)


    aboutFrame = customtkinter.CTkFrame(profile_mainframe, height=250, width=300, fg_color = '#292929')
    # about
    def about():
        global abt
        aboutFrame.place(x=150, y=500)

        aboutme = customtkinter.CTkLabel(aboutFrame, text='About Me', text_color='white', width=40,  text_font=('uni sans', 15))
        aboutme.place(x=10, y=5)

        aboutlabel = customtkinter.CTkLabel(aboutFrame,text = functions_chat.get_bio(functions_chat.CurrentUserID)[1],bg_color = 'blue',height=210, width=290 )
        aboutlabel.place(x=2,y=37)


    
    def execute_about_edit(aboutStr):
        global abt
        global aboutlabel
        functions_chat.update_bio(aboutStr)
##        for widget in aboutFrame.winfo_children():
##            widget.destroy()
        abt.destroy()
        aboutEditButton.configure(text = 'Edit', command=about_edit)
        aboutlabel = customtkinter.CTkLabel(aboutFrame,text = functions_chat.get_bio(functions_chat.CurrentUserID)[1])
        aboutlabel.place(x=10,y=20)

        about()

    def about_edit():
        global abt
        global aboutlabel
##        for widget in aboutFrame.winfo_children():
##            widget.destroy()
        
##        aboutFrame.place(x=745, y=50)
##
##        aboutme = customtkinter.CTkLabel(aboutFrame, text='About Me', text_color='white', width=40, text_font=('Uni Sans', 13))
##        aboutme.place(x=10, y=5)

        aboutEditButton.configure(text = 'Done', command = lambda: execute_about_edit(abt.get("1.0")))
        aboutlabel.destroy()

        abt = tkinter.Text(aboutFrame, height=12, width=33, bg = '#292929',fg='white',bd=0)
        abt.place(x=20, y=30)
        abt.insert('1.0',functions_chat.get_bio(functions_chat.CurrentUserID)[1])


    aboutEditButton = customtkinter.CTkButton(aboutFrame, text = 'Edit', width = 30, command=about_edit)
    aboutEditButton.place(x = 250, y = 5)

    def details():
        nonlocal acctframe
        global editProfileButton
        credentials = functions_chat.get_user(functions_chat.email)
        
        emailent = customtkinter.CTkLabel(acctframe,

                            height = 27,
                            fg_color = '#151515',
                            text = credentials[1],               
                            corner_radius = 15,
                            text_font = ('Bahnschrift SemiLight',18),
                            justify = 'left')
        emailent.place(x=60,y=100)

        email = customtkinter.CTkLabel(acctframe,
                         width=20,
                         height=7,
                         text='Email ID',
                         text_font = ('smth',18,'bold'))
        email.place(x=75, y = 65)

        unent = customtkinter.CTkLabel(acctframe,

                            height = 27,
                            fg_color = '#151515',
                            text = credentials[2],           
                            corner_radius = 15,
                         text_font = ('Bahnschrift SemiLight',18),
                                       justify = 'left')
        unent.place(x=60,y=200)


        un = customtkinter.CTkLabel(acctframe,
                      width=10,
                      height=7,
                      text='Username',
                      text_font = ('smth',18,'bold'))
        un.place(x=75, y = 165)

        pwent = customtkinter.CTkLabel(acctframe,

                            height = 27,
                            fg_color = '#151515',
                            text = '****',           
                            corner_radius = 15,
                         text_font = ('Bahnschrift SemiLight',18),
                                       justify = 'left')
        pwent.place(x=60,y=300)

        pw = customtkinter.CTkLabel(acctframe,
                      width=20,
                      height=7,
                      text='Password',
                      text_font = ('smth',18,'bold'))
        pw.place(x=75, y = 265)

        editProfileButton = customtkinter.CTkButton(prof,
                         width = 725,
                         text = 'Edit account details',
                         text_font = ('uni sans',14),
                         corner_radius = 15,
                         border_width = 1,
                         border_color = '#0d98ba',
                         fg_color = '#151515',
                         hover_color = '#0d98ba',
                         command=lambda: details_edit(acctframe))
        editProfileButton.place(x=450, y = 550)

    def execute_socials_edit(facebook,instagram,spotify,youtube):
        nonlocal acctframe
        functions_chat.update_socials(facebook,instagram,spotify,youtube)
        for widget in acctframe.winfo_children():
            widget.destroy()
        other_handles()
        editmedia.configure(text = 'Edit media handles', command=other_handles_edit)


    def other_handles_edit():
        global editmedia
        editmedia.configure(text = 'Done', command = lambda: execute_socials_edit(fbent.get(), igent.get(), spotifyent.get(), ytent.get()))

        for widget in acctframe.winfo_children():
            widget.destroy()

        bio = functions_chat.get_bio(CurrentUserID)
            
        fbent = customtkinter.CTkEntry(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                            border_width= 1,
                            placeholder_text= 'Facebook profile',
                            placeholder_text_color = 'silver',
                         text_font = ('uni sans',15),
                            corner_radius = 5,
                            text_color = 'silver')
        fbent.insert(0,bio[4])
        fbent.place(x=100,y=50)
        fb = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\fb.png').resize((40,40)))

        facebook = customtkinter.CTkButton(acctframe,
                      width = 20,
                      height = 20,
                      image = fb,
                      text = '',
                      fg_color = '#151515')
        facebook.place(x=760,y = 40)

        igent = customtkinter.CTkEntry(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                            border_width= 1,
                            placeholder_text= 'Instagram profile',
                         text_font = ('uni sans',15),
                            placeholder_text_color = 'silver',
                            corner_radius = 5,
                            text_color = 'silver')
        igent.insert(0,bio[2])
        igent.place(x=100,y=100)
        insta = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\insta.png').resize((40,40)))

        instagram = customtkinter.CTkButton(acctframe,
                              width = 20,
                              height = 20,
                              image = insta,
                              text = '',
                              fg_color = '#151515',
                             hover_color = '#151515')
        instagram.place(x=760,y =90)


        ytent = customtkinter.CTkEntry(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                            border_width= 1,
                            placeholder_text= 'YouTube channel',
                         text_font = ('uni sans',15),
                            placeholder_text_color = 'silver',
                            corner_radius = 5,
                            text_color = 'silver')
        ytent.insert(0,bio[5])
        ytent.place(x=100,y=150)
        yt = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\yt.png').resize((40,40)))

        youtube = customtkinter.CTkButton(acctframe,
                              width = 20,
                              height = 20,
                              image = yt,
                              text = '',
                            fg_color = '#151515')
        youtube.place(x=760,y = 140)


        spotifyent = customtkinter.CTkEntry(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                            border_width= 1,
                            placeholder_text= 'Spotify account',
                         text_font = ('uni sans',15),
                            placeholder_text_color = 'silver',
                            corner_radius = 5,
                            text_color = 'silver')
        spotifyent.insert(0,bio[3])
        spotifyent.place(x=100,y=200)
        tw = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\twitter.png').resize((40,40)))

        twitter = customtkinter.CTkButton(acctframe,
                              width = 20,
                              height = 20,
                              image = tw,
                              text = '',
                              fg_color = '#151515',
                            text_font = ('uni sans',15),
                             hover_color = '#151515')
        twitter.place(x=760,y = 190)


        
    about()
    details()
    mode()
    #log_out(masterFrame)
    def other_handles():
        global editmedia
        bio = functions_chat.get_bio(CurrentUserID)    
  
        fbent = customtkinter.CTkLabel(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                         text_font = ('uni sans',15),
                            corner_radius = 5,
                            text_color = 'silver',
                                       text=bio[4])

        fbent.place(x=100,y=50)
        fb = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\fb.png').resize((40,40)))

        facebook = customtkinter.CTkButton(acctframe,
                      width = 20,
                      height = 20,
                      image = fb,
                      text = '',
                      fg_color = '#151515')
        facebook.place(x=760,y = 40)

        igent = customtkinter.CTkLabel(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                         text_font = ('uni sans',15),
                            corner_radius = 5,
                            text_color = 'silver',
                                       text=bio[2])

        igent.place(x=100,y=100)
        insta = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\insta.png').resize((40,40)))

        instagram = customtkinter.CTkButton(acctframe,
                              width = 20,
                              height = 20,
                              image = insta,
                              text = '',
                              fg_color = '#151515',
                             hover_color = '#151515')
        instagram.place(x=760,y =90)


        ytent = customtkinter.CTkLabel(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                         text_font = ('uni sans',15),
                            corner_radius = 5,
                            text_color = 'silver',
                                       text=bio[5])

        ytent.place(x=100,y=150)
        yt = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\yt.png').resize((40,40)))

        youtube = customtkinter.CTkButton(acctframe,
                              width = 20,
                              height = 20,
                              image = yt,
                              text = '',
                            fg_color = '#151515')
        youtube.place(x=760,y = 140)


        spotifyent = customtkinter.CTkLabel(acctframe,
                            width = 645,
                            height = 25,
                            fg_color = '#292929',
                            corner_radius = 5,
                            text_color = 'silver',
                            text=bio[3])

        spotifyent.place(x=100,y=200)
        tw = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\twitter.png').resize((40,40)))

        twitter = customtkinter.CTkButton(acctframe,
                              width = 20,
                              height = 20,
                              image = tw,
                              text = '',
                              fg_color = '#151515',
                            text_font = ('uni sans',15),
                             hover_color = '#151515')
        twitter.place(x=760,y = 190)

        editmedia = customtkinter.CTkButton(prof,
                         width = 750,
                         text = 'Edit media handles',
                         corner_radius = 15,
                         border_width = 1,
                         border_color = '#0d98ba',
                         text_font = ('uni sans',14),
                         fg_color = '#151515',
                         hover_color = '#0d98ba',
                         command=other_handles_edit)
        editmedia.place(x=450, y = 550)
        
    about()
    details()
    mode()

def add_dms():

    def search():
        email = userSearchEntry.get()
        user = functions_chat.get_user(email)
        bio = functions_chat.get_bio(user[0])
        for widget in resultframe.winfo_children():
            widget.destroy()
        
        profilePicturePath = "ProfilePictures/" + str(user[0]) + ".png"
        profilePicture = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((350,350)))
        pictureLabel = customtkinter.CTkLabel(resultframe, image=profilePicture)
        pictureLabel.image = profilePicture
        pictureLabel.place(x=975,y = 0)
        username = customtkinter.CTkLabel(resultframe,
                          width = 40,
                          height = 10,
                          text = user[2],
                          fg_color = '#101010',
                          text_color = 'White',
                          text_font = ('Gill Sans MT',40))
        username.place(x=90,y=50)

        aboutme = customtkinter.CTkLabel(resultframe,
                          width = 40,
                          height = 10,
                          text = '[About Me]',
                          fg_color = '#101010',
                          text_color = 'light gray',
                          text_font = ('Calibri',20))
        aboutme.place(x=85,y=140)

        desc = customtkinter.CTkLabel(resultframe,
                          width = 40,
                          height = 10,
                          text = bio[1],
                          fg_color = '#101010',
                          text_color = 'light gray',
                          text_font = ('Calibri',19),
                          justify = 'left')
        desc.place(x=85,y=175)
        canvas2 = tkinter.Canvas(resultframe,
                        width = 550,
                        height = 20,
                        bg = '#101010',
                        highlightbackground = '#101010',
                        highlightthickness = 1)
        canvas2.place(x= 850, y = 460)
        canvas2.create_line(2,2,550,2,fill='#d24e01',width = 2)

        def add_friend():
            functions_chat.new_dm(user[0])
            friendButton.configure(state = 'disabled')
            warningLabel.configure(text = 'added friend')

        
        friendButton = customtkinter.CTkButton(resultframe,
                           width = 70,
                           height = 20,
                           corner_radius = 15,
                           text = '     Friend     ',
                           text_font = ('uni sans',18),
                           fg_color = '#101010',
                           text_color = 'white',
                           hover_color = '#ff4800',
                           border_width = 1,
                           border_color = '#ff4800',
                           command=add_friend,
                           state = 'normal',
                           text_color_disabled='silver'	)
        friendButton.place(x=1200,y=415)

        warningLabel = customtkinter.CTkLabel(resultframe, text = '', anchor='w', justify='left')
##        usernameTitleLabel.place(x = 300, y = 75)
##        usernameLabel.place(x = 300, y = 110)
##        bioTitleLabel.place(x = 300, y = 180)
##        bioLabel.place(x = 300, y = 215)
##        addFriendButton.place(x = 300, y = 300)
        warningLabel.place(x = 1225, y = 465)
        friends = functions_chat.get_dm_users()
        for friend in friends:
            if friend[0] == user[0]:
                friendButton.configure(state = 'disabled')
                warningLabel.configure(text = 'User is already your friend',text_color = 'red')

        message = customtkinter.CTkButton(resultframe,
                           width = 35,
                           height = 10,
                           corner_radius = 15,
                           text = '   Message   ',
                            text_font = ('uni sans',18),
                           fg_color = '#101010',
                           text_color = 'white',
                           hover_color = '#ff4800',
                           border_width = 1,
                           border_color = '#ff4800')
        message.place(x=1000,y=415)    

        insta = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\insta.png').resize((40,40)))

        instagram = customtkinter.CTkButton(resultframe,
                              width = 20,
                              height = 20,
                              image = insta,
                              text = '',
                              fg_color = '#101010',
                             hover_color = '#101010')
        instagram.place(x=450,y = 500)

        fb = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\fb.png').resize((40,40)))

        facebook = customtkinter.CTkButton(resultframe,
                              width = 20,
                              height = 20,
                              image = fb,
                              text = '',
                              fg_color = '#101010',
                             hover_color = '#101010')
        facebook.place(x=600,y = 500)

        yt = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\yt.png').resize((40,40)))

        youtube = customtkinter.CTkButton(resultframe,
                              width = 20,
                              height = 20,
                              image = yt,
                              text = '',
                              fg_color = '#101010',
                             hover_color = '#101010')
        youtube.place(x=750,y = 500)

        tw = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\twitter.png').resize((40,40)))

        twitter = customtkinter.CTkButton(resultframe,
                              width = 20,
                              height = 20,
                              image = tw,
                              text = '',
                              fg_color = '#101010',
                             hover_color = '#101010')
        twitter.place(x=900,y = 500)

    
    friend_mainframe = customtkinter.CTkFrame(app,
                            width = 1600,
                            height = 900,
                                fg_color = 'blue',
                                corner_radius = 0)
    friend_mainframe.grid(row = 0, column = 0, columnspan = 5, sticky = 'nsew')
    

    toplabel = customtkinter.CTkLabel(friend_mainframe,
                        width=1600,
                        height = 600,
                        fg_color = '#151515',
                        corner_radius = 0,
                        text = '')
    toplabel.place(x=0,y=0)

    bottomlabel = customtkinter.CTkLabel(friend_mainframe,
                        width=1600,
                        height = 300,
                        fg_color = '#d24e01',
                           text = '',
                        corner_radius = 0)
    bottomlabel.place(x=0, y = 600 )


    heading = customtkinter.CTkLabel(friend_mainframe,
                       width = 20,
                       text = 'Friends',
                       fg_color = '#151515',
                       text_color = '#e8e7ea',
                       text_font = ('Calibri', 50))
    heading.place(x=35, y = 10)

    add_friend = customtkinter.CTkFrame(friend_mainframe,
                          width = 1400,
                          height = 700,
                          fg_color = '#101010',
                          corner_radius = 0)
    add_friend.place(x=100, y = 100)
            
    userSearchEntry = customtkinter.CTkEntry(add_friend,
                        width = 725,
                        height = 35,
                        corner_radius = 10,
                        placeholder_text = 'Enter email',
                        placeholder_text_color = 'gray',
                        text_font = ('georgia',11),
                        fg_color = '#101010',
                        border_width = 0)
    userSearchEntry.place(x=35, y = 75)

    canvas = tkinter.Canvas(add_friend,
                    width = 730,
                    height = 10,
                    bg = '#101010',
                    highlightbackground = '#101010',
                    highlightthickness = 1)
    canvas.place(x=33, y = 113)
    canvas.create_line(2,2,727,2,fill='#d24e01')

    

    searchimage = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\search.png').resize((25,25)))
    addsearch = customtkinter.CTkButton(add_friend,
                          width = 25,
                          height = 10,
                          image = searchimage,
                          text = '',
                          fg_color = '#101010',
                          hover_color = '#101010',
                          command = search)
    addsearch.place(x=725,y = 73)
    resultframe = customtkinter.CTkFrame(add_friend,
                           width = 1400,
                           height = 550,
                           fg_color = '#101010')
    resultframe.place(x=0,y=150)
    msg = customtkinter.CTkLabel(resultframe,
                   text = 'Find new friends',
                   fg_color = '#101010',
                   text_color = 'gray',
                   text_font = ('inter',22))
    msg.place(x=600,y=200)

        


    app.columnconfigure(0, weight = 1)
##    masterFrame = customtkinter.CTkFrame(app)
##    masterFrame.grid(row = 0, column = 0, columnspan = 5, sticky = 'nsew')
##    bg = customtkinter.CTkFrame(masterFrame, height=200, width=2000, border=0, fg_color='purple')  # 003366 #ec4d37
##    addFriendsLabel = customtkinter.CTkLabel(bg, text='Add Friends', text_font=('Uni Sans', 30, 'bold'))
##    userInfoFrame = customtkinter.CTkFrame(masterFrame, width = 800, height = 400)
##    userSearchEntry = customtkinter.CTkEntry(masterFrame, width = 600, height = 40, placeholder_text='Enter email')
##    searchButton = customtkinter.CTkButton(app, text='Search', command=search, width = 190, height = 40)
##    messageLabel = customtkinter.CTkLabel(userInfoFrame, text = 'Find new friends', text_font=('Uni Sans', 20), width = 200, justify = 'center')
##    messageLabel.place(x = 300, y = 200)
##    userInfoFrame.place(x = 400, y = 160)
##    userSearchEntry.place(x = 400, y = 610)
##    searchButton.place(x = 1010, y = 610)
##    bg.place(x=0, y=0)
##    addFriendsLabel.place(x=250, y=80)


def rate_us():
    #CREATE TABLE feedback(userid INT, rate INT, feedback_text VARCHAR(1000), date DATE);
    
    def submit_clicked():
        credentials = functions_chat.get_user(functions_chat.email)
        feedbackRecord = (credentials[0],slider.get(),feedbackTextbox.get("1.0"), datetime.date.today())
        command = f'INSERT INTO feedback VALUES(%s,%s,%s,%s)'
        cursor.execute(command, feedbackRecord)
        mydb.commit()

        rateus.destroy()
        
    rateus = customtkinter.CTkToplevel()
    rateus.geometry('400x600')
    rateus.title('Feedback form')


    rateimg = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\rate.png').resize((100,100)))
    rateimglabel = customtkinter.CTkLabel(rateus,
                            width = 100,
                            height = 100,
                            text = '',
                            image = rateimg)
    rateimglabel.place(x=150,y = 15)
    ratelabel = customtkinter.CTkLabel(rateus,
                         text = 'Enjoying Discard?',
                         text_font = ('uni sans', 15, 'bold'))
    ratelabel.place(x=115, y = 125)
    rate_sublabel = customtkinter.CTkLabel(rateus,
                             height = 10,
                             text = 'Rate your experience so far.',
                             text_color = 'gray',
                             text_font = ('uni sans', 10))
    rate_sublabel.place(x=117, y = 150)
    rateframe = customtkinter.CTkFrame(rateus,
                         fg_color = '#292929',
                         width = 350,
                         height = 75)
    rateframe.place(x=25,y=200)

    slider = customtkinter.CTkSlider(rateframe,
                       from_=0,
                       to=5,
                       number_of_steps = 5,
                       width = 250,
                       button_color = 'sky blue')
    slider.place(x=50, y = 30)
    slider.set(0)

    smiley = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\smiley.png').resize((40,40)))
    smileylabel = customtkinter.CTkLabel(rateframe,
                            width = 15,
                            height = 15,
                            text = '',
                            image = smiley)
    smileylabel.place(x=7,y =17)
    sad = ImageTk.PhotoImage(Image.open(r'C:\Users\ajnil\Downloads\Chat-app-master\Chat-app-master\ImageResources_new\ImageResources\sad.png').resize((43,43)))
    sadlabel = customtkinter.CTkLabel(rateframe,
                            width = 15,
                            height = 15,
                            text = '',
                            image = sad)
    sadlabel.place(x=300,y = 15)


    feedbacklabel = customtkinter.CTkLabel(rateus,
                         text = 'Care to share more?',
                         text_font = ('uni sans', 14, 'bold'),
                         justify = 'left')
    feedbacklabel.place(x=25, y = 300)
    feedback_sublabel = customtkinter.CTkLabel(rateus,
                             height = 10,
                             text = 'Let us know how we can improve.',
                             text_color = 'gray',
                             text_font = ('uni sans', 10),
                             justify = 'left')
    feedback_sublabel.place(x=25, y = 325)

    
    feedbackframe = customtkinter.CTkFrame(rateus,
                         fg_color = '#292929',
                         width = 350,
                         height = 200)
    feedbackframe.place(x=25,y=355)
    feedbackTextbox = tkinter.Text(feedbackframe,
                        width = 42,
                        height = 11,
                        bg= '#292929',
                        fg = 'white',
                    bd = 0)
    feedbackTextbox.place(x=5,y=5)

    cancel = customtkinter.CTkButton(rateus,
                       width = 150,
                       text = 'Cancel',
                       text_color = 'red',
                       border_color = 'red',
                       corner_radius = 5,
                       border_width = 1,
                       fg_color = '#202020',
                       command = rateus.destroy)
    cancel.place(x = 25, y = 565)
    submit = customtkinter.CTkButton(rateus,
                       width = 150,
                       text = 'Submit',
                       text_color = 'green',
                       border_color = 'green',
                       corner_radius = 5,
                       border_width = 1,
                       fg_color = '#202020',
                       command =submit_clicked)
    submit.place(x = 225, y = 565)
    
    rateus.mainloop()

def log_out():
    os.remove('credentials.txt')
    app.destroy()

def mode():
    app.rowconfigure(0, weight = 1)
    app.rowconfigure(1, minsize = 10)
    modeSelecter = customtkinter.CTkFrame(master=app)
    modeSelecter.columnconfigure(0, weight = 1)
    modeSelecter.columnconfigure(1, weight = 1)
    modeSelecter.columnconfigure(2, weight = 1)
    modeSelecter.columnconfigure(3, weight = 1)
    modeSelecter.columnconfigure(4, weight = 1)
    modeSelecter.grid(row = 1, columnspan = 4, sticky = 'ew')

    chatMode = customtkinter.CTkFrame(master=modeSelecter, height=75)
    friendsMode = customtkinter.CTkFrame(master=modeSelecter, height=75)
    settingsMode = customtkinter.CTkFrame(master=modeSelecter, height=75)
    rateMode = customtkinter.CTkFrame(master=modeSelecter, height=75)
    logoutButton = customtkinter.CTkFrame(master=modeSelecter, height=75)

    chatMode.columnconfigure(0, weight = 1)
    friendsMode.columnconfigure(0, weight = 1)
    settingsMode.columnconfigure(0, weight = 1)
    rateMode.columnconfigure(0, weight = 1)
    logoutButton.columnconfigure(0, weight = 1)

    chatsPicture = ImageTk.PhotoImage(Image.open('ImageResources/chats.png').resize((35,35)))
    chatsLabel = customtkinter.CTkLabel(chatMode, image=chatsPicture, width = 35)
    chatsLabel.image = chatsPicture
    chatsLabel.grid(row = 0, column = 0, pady = 5)

    friendsPicture = ImageTk.PhotoImage(Image.open('ImageResources/friends.png').resize((35,35)))
    friendsLabel = customtkinter.CTkLabel(friendsMode, image = friendsPicture, width = 35)
    friendsLabel.image = friendsPicture
    friendsLabel.grid(row = 0, column = 0, pady = 5)

    settingsPicture = ImageTk.PhotoImage(Image.open('ImageResources/settings.png').resize((35,35)))
    settingsLabel = customtkinter.CTkLabel(settingsMode, image = settingsPicture, width = 35)
    settingsLabel.image = settingsPicture
    settingsLabel.grid(row = 0, column = 0, pady = 5)

    ratePicture = ImageTk.PhotoImage(Image.open('ImageResources/star.png').resize((35,35)))
    rateLabel = customtkinter.CTkLabel(rateMode, image=ratePicture, width = 35)
    rateLabel.image = ratePicture
    rateLabel.grid(row = 0, column = 0, pady = 5)

    logoutPicture = ImageTk.PhotoImage(Image.open('ImageResources/logout.png').resize((35,35)))
    logoutLabel = customtkinter.CTkLabel(logoutButton, image=logoutPicture, width = 35)
    logoutLabel.image = logoutPicture
    logoutLabel.grid(row = 0, column = 0, pady = 5)

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
        elif id == 3:
            rate_us()
        elif id==4:
            log_out()
            
        
    chatMode.bind('<Enter>', enter)
    chatMode.bind('<Leave>', leave)
    chatMode.canvas.bind("<Button-1>", lambda event, id = 0: click(event, id))

    friendsMode.bind('<Enter>', enter)
    friendsMode.bind('<Leave>', leave)
    friendsMode.canvas.bind("<Button-1>", lambda event, id = 1: click(event, id))

    settingsMode.bind('<Enter>', enter)
    settingsMode.bind('<Leave>', leave)
    settingsMode.canvas.bind("<Button-1>", lambda event, id = 2: click(event, id))

    rateMode.bind('<Enter>', enter)
    rateMode.bind('<Leave>', leave)
    rateMode.canvas.bind("<Button-1>", lambda event, id = 3: click(event, id))

    logoutButton.bind('<Enter>', enter)
    logoutButton.bind('<Leave>', leave)
    logoutButton.canvas.bind("<Button-1>", lambda event, id = 4: click(event, id))

    chatMode.grid(column = 0, row = 0, sticky = 'nsew')
    friendsMode.grid(column = 1, row = 0, sticky = 'nsew')
    settingsMode.grid(column = 2, row = 0, sticky = 'nsew')
    rateMode.grid(column = 3, row = 0, sticky = 'nsew')
    logoutButton.grid(column = 4, row = 0, sticky = 'nsew')

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
