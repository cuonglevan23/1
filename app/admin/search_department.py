#search department
from tkinter import *
import customtkinter
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox

class SearchDepartment():
    def __init__(self, main):
        self.main = main
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.main.title("Tìm kiếm Phòng ban")
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

        # ++++++++++++++++++++++++++++Label+++++++++++++++++++++++++++++++++++++
        department_lbl = customtkinter.CTkLabel(master=topFrame, text="Tìm kiếm phòng ban: ", font=font720)
        department_lbl.place(x=20, y=20)

        # ++++++++++++++++++++++++++++++TextField++++++++++++++++++++++++++++++++++++++++++++++++++
        self.search_text = StringVar()
        department_txt = customtkinter.CTkEntry(master=topFrame, font=font720, textvariable=self.search_text, placeholder_text="Tên phòng ban", width=200)
        department_txt.place(x=320, y=20)

        # Dữ liệu phòng ban
        self.data = {
            'Department': ['HR', 'IT', 'Finance', 'Marketing', 'Sales'],
            'EmployeeCount': [15, 30, 12, 25, 20]
        }

        style1 = ttk.Style()
        style1.theme_use("default")
        style1.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b", bordercolor="#343638", borderwidth=0, font=('Times New Roman', 16))
        style1.map('Treeview', background=[('selected', '#22559b')])

        style1.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Times New Roman', 17))
        style1.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.department_treeview = ttk.Treeview(self.main)
        self.department_treeview.pack(side=BOTTOM, fill=BOTH, expand=TRUE)

        self.department_treeview['columns'] = ('department', 'employee_count')
        self.department_treeview.column('#0', width=0, stretch=0)
        self.department_treeview.column('department', width=150, anchor=CENTER)
        self.department_treeview.column('employee_count', width=150, anchor=CENTER)

        self.department_treeview.heading('#0', text='', anchor=CENTER)
        self.department_treeview.heading('department', text='Phòng ban', anchor=CENTER)
        self.department_treeview.heading('employee_count', text='Số lượng nhân viên', anchor=CENTER)


        search_image = customtkinter.CTkImage(light_image=Image.open("/Users/lvc/PycharmProjects/pythonProject6/app/image/search-alt-2-regular-24.png"))
        searchbtn = customtkinter.CTkButton(master=topFrame, image=search_image, text="Search", font=font720, width=180, command=self.search_department)
        searchbtn.place(x=550, y=20)

    def show_department_data(self, data):
        for i in range(len(data['Department'])):
            self.department_treeview.insert("", "end", values=(data['Department'][i], data['EmployeeCount'][i]))

    def search_department(self):
        search_criteria = self.search_text.get().lower()
        if search_criteria:
            filtered_data = {
                'Department': [],
                'EmployeeCount': []
            }
            for i in range(len(self.data['Department'])):
                if search_criteria in self.data['Department'][i].lower():
                    filtered_data['Department'].append(self.data['Department'][i])
                    filtered_data['EmployeeCount'].append(self.data['EmployeeCount'][i])
            self.department_treeview.delete(*self.department_treeview.get_children())
            self.show_department_data(filtered_data)
        else:
            self.department_treeview.delete(*self.department_treeview.get_children())
            self.show_department_data(self.data)

if __name__ == '__main__':
    main = customtkinter.CTk()
    SearchDepartment(main)
    main.mainloop()
