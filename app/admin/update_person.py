from tkinter import *
from PIL import ImageTk, Image
import customtkinter
from tkinter import messagebox

from app.dbms.person_management import update_person_record
from app.libs.person_lib import Person_Libs


#+++++++++++++++++++++++++++++++++Main Class++++++++++++++++++++++++++++++
class UpdatePersonProfile():
    def __init__(self, updateprofile, person_id, name, mobile, address, position,count):
        self.updateprofile = updateprofile
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.updateprofile.resizable(0,0)
        self.updateprofile.title("{} Profile".format(name))  # Định dạng tên người dùng vào tiêu đề

        width = 750
        height = 440
        myscreenwidth = self.updateprofile.winfo_screenwidth()
        myscreenheight = self.updateprofile.winfo_screenheight()
        xCordinate = int((myscreenwidth / 2) - (width / 2))
        yCordinate = int((myscreenheight / 2) - (height / 2))
        self.updateprofile.geometry('{}x{}+{}+{}'.format(width, height, xCordinate, yCordinate - 50))
        self.updateprofile.maxsize(750, 440)

        id=Entry(self.updateprofile)
        id.insert(0, person_id)

        #++++++++++++++++++++++++++++My Font++++++++++++++++++++++++++++++++++++++++++
        font720 =customtkinter.CTkFont(family='Times New Roman', size=19, weight='normal')

        #++++++++++++++++++++++++++++++Center Frame+++++++++++++++++++++++++++++++++++
        centerFrame = customtkinter.CTkFrame(master=self.updateprofile, width=710, height=360)
        centerFrame.place(x=20, y=60)

        #++++++++++++++++++++++++++++++++++++++Name Label+++++++++++++++++++++++++++++++++++++++
        namelbl = customtkinter.CTkLabel(centerFrame, text="Name: ", font=font720)
        namelbl.place(x=50, y=100)


        namelbl1=customtkinter.CTkEntry(centerFrame,width=180,font=font720)
        namelbl1.insert(0, name)
        namelbl1.place(x=150, y=100)


        mobilebl = customtkinter.CTkLabel(centerFrame, text="Mobile: ", font=font720)
        mobilebl.place(x=50, y=150)


        mobile1 = customtkinter.CTkEntry(centerFrame,width=180, font=font720)
        mobile1.insert(0,mobile)
        mobile1.place(x=150, y=150)


        addressbl = customtkinter.CTkLabel(centerFrame, text="Address: ", font=font720)
        addressbl.place(x=50, y=200)


        address1 = customtkinter.CTkEntry(centerFrame,width=180, font=font720)
        address1.insert(0,address)
        address1.place(x=150, y=200)


        positionbl = customtkinter.CTkLabel(centerFrame, text="Position: ", font=font720)
        positionbl.place(x=50, y=250)


        position1 = customtkinter.CTkEntry(centerFrame,width=180, font=font720)
        position1.insert(0, position)
        position1.place(x=150, y=250)


        countbl = customtkinter.CTkLabel(centerFrame, text="NUMBER of attendance days: ", font=font720)
        countbl.place(x=410, y=100)


        count1 = customtkinter.CTkEntry(centerFrame,width=180,  font=font720)
        count1.insert(0,count)
        count1.place(x=510, y=100)



        def updateperson():
            person=Person_Libs(id=id.get(),name=namelbl1.get(),mobile=mobile1.get(),address=address1.get(),position=position1.get())
            updateResult=update_person_record(person)
            if updateResult==True:
                messagebox.showinfo("LC SECURITY System","The {} details is updated successfully!".format(name))
                self.updateprofile.destroy()

            else:
                messagebox.showerror("LC SECURITY System","Error")

        update_btn_image = customtkinter.CTkImage(light_image=Image.open('/Users/lvc/PycharmProjects/pythonProject6/app/image/edit-alt-regular-24.png'))
        update_btn = customtkinter.CTkButton(master=centerFrame,command=updateperson, text="Update Details",font=font720,image=update_btn_image)
        update_btn.place(x=300, y=320)

        # +++++++++++++++++++++++++++++++++++++Image Label+++++++++++++++++++++++++++++++++++++++
        user_image = ImageTk.PhotoImage(Image.open("/Users/lvc/PycharmProjects/pythonProject6/app/image/user-solid-120.png"))
        user_image_label = Label(self.updateprofile, image=user_image, bg="#212325")
        user_image_label.image = user_image
        user_image_label.place(x=200, y=0)


if __name__=='__main__':
    updateprofile=customtkinter.CTk()
    UpdatePersonProfile(updateprofile)
    updateprofile.mainloop()