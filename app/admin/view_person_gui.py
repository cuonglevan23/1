from tkinter import *
import customtkinter
from PIL import ImageTk, Image

from app.admin.update_person import UpdatePersonProfile
from app.admin.view_person import PersonProfile


class ViewPersonProfile():
    def __init__(self,profile, person_id, name, mobile, address, position, attendance_status, timestamp,count):
        self.profile=profile
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.profile.resizable(0, 0)
        self.profile.title("View {} Profile".format(name))
        width = 470
        height = 200
        myscreenwidth = self.profile.winfo_screenwidth()
        myscreenheight = self.profile.winfo_screenheight()
        xCordinate = int((myscreenwidth / 2) - (width / 2))
        yCordinate = int((myscreenheight / 2) - (height / 2))
        self.profile.geometry('{}x{}+{}+{}'.format(width, height, xCordinate+100, yCordinate - 50))
        self.profile.maxsize(950, 400)

        # ++++++++++++++++++++++++++++My Font++++++++++++++++++++++++++++++++++++++++++
        font720 = customtkinter.CTkFont(family='Times New Roman', size=19, weight='normal')

        viewprofileframe=customtkinter.CTkFrame(self.profile, width=200, height=150)
        viewprofileframe.place(x=20, y=20)

        image = Image.open('/Users/lvc/PycharmProjects/pythonProject6/app/image/user-solid-72.png')
        image = image.resize((80, 80))
        image = ImageTk.PhotoImage(image)
        Image_Label = Label(viewprofileframe, image=image, bg="#2b2b2b")
        Image_Label.image = image
        Image_Label.place(x=75, y=20)

        def open_profile():
            # self.profile.destroy()
            main = customtkinter.CTkToplevel()
            PersonProfile(main, person_id, name, mobile, address, position, attendance_status, timestamp,count)
            main.mainloop()


        label=customtkinter.CTkButton(viewprofileframe,fg_color="#2b2b2b",command=open_profile,  hover_color="#2b2b2b", text="View Profile",font=font720 )
        label.place(x=25, y=100)

        updateprofileframe = customtkinter.CTkFrame(self.profile, width=200, height=150)
        updateprofileframe.place(x=250, y=20)


        image1 = Image.open('/Users/lvc/PycharmProjects/pythonProject6/app/image/user-solid-72.png')
        image1 = image1.resize((80, 80))
        image1 = ImageTk.PhotoImage(image1)
        Image_Label1 = Label(updateprofileframe, image=image1, bg="#2b2b2b")
        Image_Label1.image = image1
        Image_Label1.place(x=75, y=20)

        def open_personprofile():

            updateprofile = customtkinter.CTkToplevel()
            UpdatePersonProfile(updateprofile, person_id, name, mobile, address, position,count)
            updateprofile.mainloop()

        label1 = customtkinter.CTkButton(updateprofileframe, fg_color="#2b2b2b", hover_color="#2b2b2b",command=open_personprofile,
                                        text="Update Profile", font=font720)
        label1.place(x=25, y=100)



if __name__=='__main__':
    profile=customtkinter.CTk()
    ViewPersonProfile(profile)
    profile.mainloop()