from tkinter import *
import customtkinter
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
from app.dbms.search_management import search_person

class SearchPerson():
    def __init__(self, main):
        self.main = main
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.main.title("LC Security Admin Dashboard")
        self.main.resizable(0, 0)
        frame_width = 1000
        frame_height = 500
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (frame_width / 2))
        y_cordinate = int((screen_height / 2) - (frame_height / 2))
        self.main.geometry("{}x{}+{}+{}".format(frame_width, frame_height, x_cordinate + 200, y_cordinate))

        font1 = customtkinter.CTkFont(family='Times New Roman', size=30, weight='bold')
        font720 = customtkinter.CTkFont(family='Times New Roman', size=20, weight='bold')

        topFrame = customtkinter.CTkFrame(self.main, height=80)
        topFrame.pack(side=TOP, fill=BOTH)

        # ++++++++++++++++++++++++++++ID Label+++++++++++++++++++++++++++++++++++++
        idlbl = customtkinter.CTkLabel(master=topFrame, text="Search: ", font=font720)
        idlbl.place(x=20, y=20)

        # ++++++++++++++++++++++++++++++ID TextField++++++++++++++++++++++++++++++++++++++++++++++++++
        self.search_text = StringVar()
        idtxt = customtkinter.CTkEntry(master=topFrame, font=font720, textvariable=self.search_text, placeholder_text="Person Name", width=200)
        idtxt.place(x=100, y=20)

        style1 = ttk.Style()
        style1.theme_use("default")
        style1.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b", bordercolor="#343638", borderwidth=0, font=('Times New Roman', 16))
        style1.map('Treeview', background=[('selected', '#22559b')])

        style1.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Times New Roman', 17))
        style1.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.person_treeview = ttk.Treeview(self.main)
        self.person_treeview.pack(side=BOTTOM, fill=BOTH, expand=TRUE)

        self.person_treeview['columns'] = ('id', 'name', 'mobile', 'address', 'position')
        self.person_treeview.column('#0', width=0, stretch=0)
        self.person_treeview.column('id', width=100, anchor=CENTER)
        self.person_treeview.column('name', width=150, anchor=CENTER)
        self.person_treeview.column('mobile', width=100, anchor=CENTER)
        self.person_treeview.column('address', width=100, anchor=CENTER)
        self.person_treeview.column('position', width=100, anchor=CENTER)


        self.person_treeview.heading('#0', text='', anchor=CENTER)
        self.person_treeview.heading('id', text='Person ID', anchor=CENTER)
        self.person_treeview.heading('name', text='Name', anchor=CENTER)
        self.person_treeview.heading('mobile', text='Mobile', anchor=CENTER)
        self.person_treeview.heading('address', text='Address', anchor=CENTER)
        self.person_treeview.heading('position', text='Position', anchor=CENTER)


        search_image = customtkinter.CTkImage(light_image=Image.open("/Users/lvc/PycharmProjects/pythonProject6/app/image/search-alt-2-regular-24.png"))
        searchbtn = customtkinter.CTkButton(master=topFrame, image=search_image, text="Search", font=font720, width=180, command=self.search_person)
        searchbtn.place(x=320, y=20)

    def search_person(self):
        search_criteria = {
            'name': self.search_text.get()
        }
        result = search_person(search_criteria)
        if result:
            self.person_treeview.delete(*self.person_treeview.get_children())
            for person in result:
                self.person_treeview.insert("", "end", values=(person.getId(), person.getName(), person.getMobile(), person.getAddress(), person.getPosition()))
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy kết quả nào.")



if __name__ == '__main__':
    main = customtkinter.CTk()
    SearchPerson(main)
    main.mainloop()
