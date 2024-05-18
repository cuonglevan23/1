from tkinter import *
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from app.dbms.person_management import get_attendance_report

class PersonReport:
    def __init__(self, main):
        self.main = main
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.main.title("Person Report")
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

        # Hiển thị biểu đồ
        self.show_chart(frame)

    def show_chart(self, frame):
        attended_count, not_attended_count = get_attendance_report()
        if attended_count is not None and not_attended_count is not None:
            labels = ['Đã chấm công', 'Chưa chấm công']
            sizes = [attended_count, not_attended_count]
            colors = ['#66b3ff', '#ff9999']
            explode = (0.1, 0)  # tách phần đã chấm công ra một chút

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=140)
            ax.axis('equal')
            ax.set_title('Tỷ lệ nhân viên đã chấm công so với chưa chấm công')

            # Tạo FigureCanvasTkAgg và nhúng biểu đồ vào frame
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
        else:
            print("Không thể lấy báo cáo chấm công.")


if __name__ == '__main__':
    main = customtkinter.CTk()
    PersonReport(main)
    main.mainloop()
