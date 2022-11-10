from tkinter import *
import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme("dark-blue")
#window stuff
bob = customtkinter.CTk()
bob.title('sign up')
bob.geometry('1000x500')
bob.resizable(False,False)


#bg
'''
background = PhotoImage(file = 'screwmecuzphotoimgdoesntwork')
bg = Label(bob, image=background)
bg.place(x=50,y=50)
'''

signupframe = customtkinter.CTkFrame(bob, width = 400, height = 400, corner_radius= 15) #bg='#292929'
signupframe.place(x=490, y = 55)


#email
email= customtkinter.CTkLabel(signupframe, text = 'Email ID')
email.place(x= 20, y = 75)
emailentry = customtkinter.CTkEntry(signupframe, width = 50, border_width= 2, placeholder_text= 'discard001@gmail.com', placeholder_text_color = 'silver') 
emailentry.place(x= 20, y = 105)

#username
username= customtkinter.CTkLabel(signupframe, text = 'Username')
username.place(x= 20, y = 135)
usernameentry = customtkinter.CTkEntry(signupframe, width = 50,border_width= 2, placeholder_text= 'Username123', placeholder_text_color = 'silver')
usernameentry.place(x= 20, y = 165)

#password
password= customtkinter.CTkLabel(signupframe, text = 'Password')
password.place(x= 20, y = 195)
passwordentry = customtkinter.CTkEntry(signupframe, width = 50,border_width= 2, placeholder_text= 'hfkdiu@#jd469', placeholder_text_color = 'silver')
passwordentry.place(x= 20, y = 225)
#eyeimg = PhotoImage(file='')
eye = customtkinter.CTkButton(signupframe, corner_radius=15) #image = eyeimg
eye.place(x=305, y = 222)

#terms and conditions
terms= customtkinter.CTkCheckBox(signupframe, text="I've read and agree to", onvalue = 1, offvalue=0)
terms.place(x=20, y = 250)
tc= customtkinter.CTkButton(signupframe, text= 'Terms & Conditions',border_width=0)
tc.place(x=157, y=252)



#sign up
signup = customtkinter.CTkButton(signupframe, text = 'Sign up', width= 50, corner_radius=15, hover_color='violet')
signup.place(x=20, y= 290)


#already have an account

already = customtkinter.CTkLabel(signupframe, text='Already have an account?')
already.place(x= 110, y = 330)
signin = customtkinter.CTkButton(signupframe, text = 'Sign in',border=0)
signin.place(x= 248, y = 330)

bob.mainloop()