from tkinter import *
from PIL import ImageTk, Image
import customtkinter


#+++++++++++++++++++++++++++++++++Main Class++++++++++++++++++++++++++++++
class PersonProfile():
    def __init__(self, main, person_id, name, mobile, address, position, attendance_status, timestamp,count):
        self.main = main
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.main.resizable(0, 0)
        self.main.title("{} Profile".format(name))  # Định dạng tên người dùng vào tiêu đề

        width = 750
        height = 400
        myscreenwidth = self.main.winfo_screenwidth()
        myscreenheight = self.main.winfo_screenheight()
        xCordinate = int((myscreenwidth / 2) - (width / 2))
        yCordinate = int((myscreenheight / 2) - (height / 2))
        self.main.geometry('{}x{}+{}+{}'.format(width, height, xCordinate, yCordinate - 50))
        self.main.maxsize(950, 400)

        #++++++++++++++++++++++++++++My Font++++++++++++++++++++++++++++++++++++++++++
        font720 =customtkinter.CTkFont(family='Times New Roman', size=19, weight='normal')

        #++++++++++++++++++++++++++++++Center Frame+++++++++++++++++++++++++++++++++++
        centerFrame = customtkinter.CTkFrame(master=self.main, width=710, height=320)
        centerFrame.place(x=20, y=60)

        #++++++++++++++++++++++++++++++++++++++Name Label+++++++++++++++++++++++++++++++++++++++
        namelbl = customtkinter.CTkLabel(centerFrame, text="Name: ", font=font720)
        namelbl.place(x=50, y=100)

        namelbl1 = customtkinter.CTkLabel(centerFrame, text="{}".format(name))  # Định dạng tên vào nhãn
        namelbl1.place(x=150, y=100)

        ID = customtkinter.CTkLabel(centerFrame, text="ID: ", font=font720)
        ID.place(x=50, y=150)

        ID1 = customtkinter.CTkLabel(centerFrame, text="{}".format(person_id))  # Định dạng ID vào nhãn
        ID1.place(x=150, y=150)

        Mobile = customtkinter.CTkLabel(centerFrame, text="Mobile: ", font=font720)
        Mobile.place(x=50, y=200)

        Mobile1 = customtkinter.CTkLabel(centerFrame, text="{}".format(mobile))  # Định dạng số điện thoại vào nhãn
        Mobile1.place(x=150, y=200)

        ADDRESS = customtkinter.CTkLabel(centerFrame, text="ADDRESS: ", font=font720)
        ADDRESS.place(x=50, y=250)

        ADDRESS1 = customtkinter.CTkLabel(centerFrame, text="{}".format(address))  # Định dạng địa chỉ vào nhãn
        ADDRESS1.place(x=150, y=250)

        POSITION = customtkinter.CTkLabel(centerFrame, text="POSITION: ", font=font720)
        POSITION.place(x=410, y=100)

        POSITION1 = customtkinter.CTkLabel(centerFrame, text="{}".format(position))  # Định dạng vị trí vào nhãn
        POSITION1.place(x=510, y=100)

        TIMEKEEPING = customtkinter.CTkLabel(centerFrame, text="TIMEKEEPING: ", font=font720)
        TIMEKEEPING.place(x=410, y=150)
        TIMEKEEPING1 = customtkinter.CTkLabel(centerFrame, text=count, font=font720)
        TIMEKEEPING1.place(x=610, y=150)

        # +++++++++++++++++++++++++++++++++++++Image Label+++++++++++++++++++++++++++++++++++++++
        user_image = ImageTk.PhotoImage(Image.open("/Users/lvc/PycharmProjects/pythonProject6/app/image/user-solid-120.png"))
        user_image_label = Label(self.main, image=user_image, bg="#212325")
        user_image_label.image = user_image
        user_image_label.place(x=250, y=10)

if __name__=='__main__':
    main=customtkinter.CTk()
    PersonProfile(main)
    main.mainloop()