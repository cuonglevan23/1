from tkinter import *
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class DepartmentReport:
    def __init__(self, main):
        self.main = main
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.main.title("Department Report")
        self.main.resizable(0, 0)
        frame_width = 900
        frame_height = 500
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (frame_width / 2))
        y_cordinate = int((screen_height / 2) - (frame_height / 2))
        self.main.geometry("{}x{}+{}+{}".format(frame_width, frame_height, x_cordinate + 200, y_cordinate))

        font1 = customtkinter.CTkFont(family='Times New Roman', size=30, weight='bold')

        topFrame = customtkinter.CTkFrame(self.main, height=100)
        topFrame.pack(side=TOP, fill=BOTH)

        titlelabel = customtkinter.CTkLabel(topFrame, text='REPORT', font=font1)
        titlelabel.place(relx=0.5, rely=0.5, anchor=CENTER)

        frame = Frame(self.main, bg="white")
        frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)

        # Tạo dữ liệu mẫu
        self.create_sample_data()

        # Hiển thị biểu đồ
        self.show_chart(frame)

    def create_sample_data(self):
        # Tạo dữ liệu mẫu với số nhân viên trong mỗi phòng ban
        data = {
            'Department': ['HR', 'IT', 'Finance', 'Marketing', 'Sales'],
            'EmployeeCount': [15, 30, 12, 25, 20]
        }
        self.df = pd.DataFrame(data)

    def show_chart(self, frame):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(self.df['Department'], self.df['EmployeeCount'], color='blue')
        ax.set_xlabel('Phòng ban')
        ax.set_ylabel('Số lượng nhân viên')
        ax.set_title('Số lượng nhân viên theo từng phòng ban')

        # Tạo FigureCanvasTkAgg và nhúng biểu đồ vào frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)

if __name__ == '__main__':
    main = customtkinter.CTk()
    DepartmentReport(main)
    main.mainloop()
