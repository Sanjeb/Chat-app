from tkinter import *
from tkinter import filedialog
from customtkinter import *
from PIL import Image, ImageTk
import functions_user


# window stuff
bob = CTk()
bob.title('sign up')
bob.geometry('950x500')
bob.resizable(False, False)
bob.configure(fg_color='#1e1c1c')


def main():
    # bg
    
    #background = Image.open(r"C:\Users\Sanje\Downloads\background.jpg")
    #bg_resize = background.resize((1000, 500))
    #bg1 = ImageTk.PhotoImage(bg_resize)

    '''
    bg = CTkButton(bob, image=bg1, text='', state='disabled')
    bg.pack()
    '''

    signupframe = CTkFrame(bob, width=400, height=450, corner_radius=15, fg_color='black')  # bg='#292929'
    signupframe.place(x=490, y=25)

    pictureFrame = CTkFrame(bob, width = 400, height = 450, corner_radius = 15, fg_color='#1e1c1c')
    pictureFrame.place(x= 50, y = 25)

    profilePicturePath = "ImageResources/DefaultProfile.png"
    profilePicture = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((300, 300)))
    pictureLabel = CTkLabel(pictureFrame, image=profilePicture)
    pictureLabel.image = profilePicture
    pictureLabel.pack()

    def changeFile():
        global profilePicturePath
        filetypes = (
        ('image files', '*.png'),
        ('All files', '*.*')
        )

        profilePicturePath = filedialog.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes)
        print(profilePicturePath)
        img2 = ImageTk.PhotoImage(Image.open(profilePicturePath).resize((300, 300)))
        pictureLabel.configure(image=img2)
        pictureFrame.image = img2

    fileChange = CTkButton(bob, text='Change Profile picture', command=changeFile)
    fileChange.place(x = 150, y = 400)

    # email
    email = CTkLabel(signupframe, text='Email ID', width=20)
    email.place(x=25, y=75)
    emailentry = CTkEntry(signupframe, width=350, border_width=2, placeholder_text='someone@gmail.com', placeholder_text_color='silver')
    emailentry.place(x=20, y=105)

    # username
    username = CTkLabel(signupframe, text='Username', width=20)
    username.place(x=20, y=135)
    usernameentry = CTkEntry(signupframe, width=350, border_width=2, placeholder_text='Enter Username', placeholder_text_color='silver')
    usernameentry.place(x=20, y=165)

    # password
    password = CTkLabel(signupframe, text='Password', width=20)
    password.place(x=20, y=195)
    passwordentry = CTkEntry(signupframe, width=350, border_width=2, placeholder_text='Enter Password', placeholder_text_color='silver')
    passwordentry.place(x=20, y=225)

    #Fill all fields
    warning = CTkLabel(signupframe, text = '', text_color='red', anchor = 'w')
    warning.place(x = 20, y = 255)

    #terms and conditions
    terms = CTkCheckBox(signupframe, text="I've read and agree to", onvalue=1, offvalue=0)
    terms.place(x=20, y=285)
    tc = Button(signupframe, text='Terms & Conditions', border=0, bg='black', fg='white', activeforeground='sky blue', activebackground='black')
    tc.place(x=172, y=286)

    # already have an account
    already = CTkLabel(signupframe,
                       text='Already have an account?')
    already.place(x=90, y=360)
    signin = Button(signupframe, text='Sign in', border=0, bg="black", fg='white', activeforeground='sky blue', activebackground='black')
    signin.place(x=235, y=363)

    def signup():
        if emailentry.get().replace(" ", "") != '' and usernameentry.get().replace(" ", "") != '' and passwordentry.get().replace(" ", "") != '':
            with open(profilePicturePath, 'rb') as file:
                binaryData = file.read()
            functions_user.create_user(emailentry.get().replace(" ", ""), usernameentry.get().replace(" ", ""), passwordentry.get().replace(" ", ""), binaryData)
            #User already exists
        else:
            warning.configure(text = "Complete all fields   ")

    # sign up
    signup = CTkButton(signupframe, text='Sign up', width=350, corner_radius=15, fg_color='teal', hover_color='sea green', command=signup)
    signup.place(x=20, y=320)

main()

bob.mainloop()