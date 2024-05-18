import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import customtkinter
from time import strftime
from tkinter import messagebox, Menu
import cv2
from PIL import Image, ImageTk

from app.admin.view_person_gui import ViewPersonProfile
from app.dbms.admin_management import get_total_person_count
from app.dbms.admin_management import get_total_timekeeping_count
from app.admin.department_report import DepartmentReport
from app.admin.person_report import PersonReport
from app.admin.search_department import SearchDepartment
from app.admin.search_person import SearchPerson
from app.dbms.connection import get_timekeeping_data, get_person_data, get_attendance_status
from app.dbms.person_management import createPerson
from app.libs.person_lib import Person_Libs as Person
from train import train_face_recognizer
from app.admin.timekeeping import Timekeeping


face_detector = cv2.CascadeClassifier('/Users/lvc/PycharmProjects/pythonProject6/haarcascade_frontalface_default.xml')

class Admin_Dashboard(customtkinter.CTk):
    def __init__(self, main):
        self.main = main
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme('blue')
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()
        self.main.minsize(screen_width, screen_height)
        self.main.title("LC Security Admin Dashboard")
        self.main.state('zoomed')

        # Lấy dữ liệu từ cơ sở dữ liệu
        total_person = get_total_person_count()
        total_timekeeping = get_total_timekeeping_count()
        # ++++++++++++++++++++++++++++++++Font Collection+++++++++++++++++++++++++++++++++++++++++++
        titlefont = customtkinter.CTkFont(family='Times New Roman', size=35, weight='normal')
        font720 = customtkinter.CTkFont(family='Times New Roman', size=20, weight='normal')
        labelfont = customtkinter.CTkFont(family='Times New Roman', size=25, weight='normal')
        sidemenufont = customtkinter.CTkFont(family='Times New Roman', size=20, weight='normal')



        # ++++++++++++++++++++++++++++++++++++++Top Frame+++++++++++++++++++++++++++++++++++++++++++
        north_frame = customtkinter.CTkFrame(master=self.main, height=80, corner_radius=0)
        north_frame.pack(side=TOP, fill=BOTH)

        # +++++++++++++++++++++++++++++++++++Welcome Label++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        welcomelabel = customtkinter.CTkLabel(master=north_frame, text="Welcome {}".format("Admin"),
                                              font=('Times New Roman', 20, 'bold'), text_color="white",
                                              fg_color="#2b2b2b")
        welcomelabel.place(x=1390, y=25)

        # +++++++++++++++++++++++++++++Title Label++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        title_lbl = customtkinter.CTkLabel(master=north_frame, text="Admin Dashboard", font=titlefont)
        title_lbl.place(x=50, y=25)

        # +++++++++++++++++++++++++++++++Left Frame+++++++++++++++++++++++++++++++++++++++
        left_frame = customtkinter.CTkFrame(master=self.main, width=300)
        left_frame.pack(side=LEFT, fill=BOTH, padx=10, pady=10)

        def my_time():
            time_string = strftime('%I:%M:%S %p')  # time format
            l1.configure(text=time_string)
            l1.after(1000, my_time)  # time delay of 1000 milliseconds

        l1 = customtkinter.CTkLabel(master=left_frame, font=sidemenufont)
        l1.place(x=90, y=150)
        my_time()

        def add_person():

            # Tạo cửa sổ mới
            root = customtkinter.CTkToplevel()
            root.title("LC Security Admin Dashboard")
            width = 1200
            height = 900
            myscreenwidth = root.winfo_screenwidth()
            myscreenheight = root.winfo_screenheight()
            xCordinate = int((myscreenwidth / 2) - (width / 2))
            yCordinate = int((myscreenheight / 2) - (height / 2))
            root.geometry('{}x{}+{}+{}'.format(width, height, xCordinate, yCordinate))

            root.resizable(0, 0)


            # Tích hợp webcam
            cap = cv2.VideoCapture(0)  # Webcam mặc định

            add_personFrame = customtkinter.CTkFrame(root, width=400, corner_radius=20)
            add_personFrame.pack(side="left", fill="both", padx=10, pady=10)

            title11lbl = customtkinter.CTkLabel(master=add_personFrame, text="ADD PERSON", font=("Arial", 16))
            title11lbl.place(x=110, y=20)

            # Ô nhập liệu
            name_lbl = customtkinter.CTkLabel(add_personFrame, text="NAME:", font=("Arial", 12))
            name_lbl.place(x=30, y=100)

            nametxt = customtkinter.CTkEntry(add_personFrame, font=("Arial", 12), width=200)
            nametxt.place(x=140, y=100)

            id_lbl = customtkinter.CTkLabel(add_personFrame, text="ID:", font=("Arial", 12))
            id_lbl.place(x=30, y=150)

            id_txt = customtkinter.CTkEntry(add_personFrame, font=("Arial", 12), width=200)
            id_txt.place(x=140, y=150)

            position_lbl = customtkinter.CTkLabel(add_personFrame, text="POSITION:", font=("Arial", 12))
            position_lbl.place(x=30, y=200)

            positiontxt = customtkinter.CTkEntry(add_personFrame, font=("Arial", 12), width=200)
            positiontxt.place(x=140, y=200)

            address_lbl = customtkinter.CTkLabel(add_personFrame, text="ADDRESS:", font=("Arial", 12))
            address_lbl.place(x=30, y=250)

            address_txt = customtkinter.CTkEntry(add_personFrame, font=("Arial", 12), width=200)
            address_txt.place(x=140, y=250)

            phone_lbl = customtkinter.CTkLabel(add_personFrame, text="PHONE:", font=("Arial", 12))
            phone_lbl.place(x=30, y=300)

            phone_txt = customtkinter.CTkEntry(add_personFrame, font=("Arial", 12), width=200)
            phone_txt.place(x=140, y=300)

            def save_person():
                person_info = {
                    'id': id_txt.get(),
                    'name': nametxt.get(),
                    'position': positiontxt.get(),
                    'phone': phone_txt.get(),
                    'address': address_txt.get()
                }
                # Tạo một đối tượng Person từ thông tin trong từ điển person_info
                new_person = Person(id=person_info['id'],
                                    name=person_info['name'],
                                    position=person_info['position'],
                                    mobile=person_info['phone'],
                                    address=person_info['address'])
                # Tạo một người mới trong cơ sở dữ liệu
                createPerson(new_person)
                messagebox.showinfo("Thành công", "Đã thêm người mới vào cơ sở dữ liệu.")


            def trainning_face():
                dataset_path = '/Users/lvc/PycharmProjects/pythonProject6/dataset'
                output_path = '/Users/lvc/PycharmProjects/pythonProject6/trainer'
                train_face_recognizer(dataset_path, output_path)
                messagebox.showinfo("Đã huấn luyện thành công.")

            save_person_btn = customtkinter.CTkButton(master=add_personFrame, text="LƯU NGƯỜI", font=("Arial", 12),
                                                      command=lambda: [save_person(), trainning_face()],
                                                      width=350)
            save_person_btn.place(x=20, y=450)

            # Thêm khung để hiển thị video từ webcam
            canvas = customtkinter.CTkCanvas(root, width=640, height=480)
            canvas.pack(side="right", padx=20, pady=20)
            def update_frame(cap, canvas):
                ret, frame = cap.read()  # Đọc khung hình từ webcam
                if ret:
                    # Face detection
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển sang RGB để hiển thị trên Tkinter
                    frame_resized = cv2.resize(frame, (
                    canvas.winfo_width(), canvas.winfo_height()))  # Đảm bảo kích thước phù hợp
                    img = Image.fromarray(frame_resized)  # Chuyển đổi sang định dạng PIL
                    imgtk = ImageTk.PhotoImage(image=img)

                    # Hiển thị trên `Canvas`
                    canvas.create_image(0, 0, anchor="nw", image=imgtk)
                    canvas.imgtk = imgtk  # Giữ tham chiếu để tránh bị xóa

                # Cập nhật mỗi 30ms
                root.after(100, lambda: update_frame(cap, canvas))

            # Bắt đầu cập nhật khung hình từ webcam
            update_frame(cap, canvas)  # Truyền đúng tham số


            def capture_30_images():
                global face_id
                global count
                person_id = id_txt.get()  # Lấy ID từ ô nhập liệu

                if not person_id:  # Kiểm tra xem ID có được nhập vào hay không
                    messagebox.showerror("Lỗi", "Vui lòng nhập ID trước khi chụp ảnh.")
                    return

                face_id = int(person_id)

                count = 0
                while count < 30:
                    ret, img = cap.read()
                    img = cv2.flip(img, 1)  # Lật ảnh video theo chiều dọc
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        count += 1
                        cv2.imwrite("/Users/lvc/PycharmProjects/pythonProject6/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

                    # Hiển thị ảnh đã chụp lên canvas
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (canvas.winfo_width(), canvas.winfo_height()))
                    img = Image.fromarray(img)
                    imgtk = ImageTk.PhotoImage(image=img)
                    canvas.create_image(0, 0, anchor="nw", image=imgtk)
                    canvas.imgtk = imgtk



                messagebox.showinfo("Thành công", f"Đã chụp 30 ảnh cho ID: {person_id}.")




            # Bắt đầu cập nhật khung hình từ webcam
            capture_button = customtkinter.CTkButton(root, text="Chụp 30 Ảnh", command=capture_30_images)
            capture_button.place(x=30, y=350)

            def on_closing():
                cap.release()  # Giải phóng webcam
                root.destroy()

            root.protocol("WM_DELETE_WINDOW", on_closing)  # Đóng cửa sổ đúng cách
            root.mainloop()


        add_person_btn = customtkinter.CTkButton(master=left_frame, text="ADD PERSON  ", command=add_person,
                                                   hover_color='black', font=sidemenufont, width=200,
                                                    fg_color='#2b2b2b')
        add_person_btn.place(x=40, y=300)

        def logout():
            self.main.destroy()
            root = customtkinter.CTk()

            root.mainloop()
        logout_btn = customtkinter.CTkButton(master=left_frame, command=logout, text="Logout              ",
                                             fg_color='#2b2b2b', hover_color='black', font=sidemenufont, width=200
                                             )
        logout_btn.place(x=40, y=850)

        def timekeeping_gui():
            root = customtkinter.CTkToplevel()
            Timekeeping(root)
            root.mainloop()

        timekeeping_btn = customtkinter.CTkButton(master=left_frame, command=timekeeping_gui, text="TIME KEEPING",
                                                      hover_color='black', font=sidemenufont, width=200,
                                                      fg_color='#2b2b2b')
        timekeeping_btn.place(x=40, y=350)



        # +++++++++++++++++++++++++++++Center Frame+++++++++++++++++++++++++++++++++++++++
        frameCenter = customtkinter.CTkFrame(master=self.main, width=1400, height=650, corner_radius=20)
        frameCenter.place(x=320, y=100)

        parent_tab = customtkinter.CTkTabview(frameCenter, width=1370)
        parent_tab.place(x=15, y=10)

        parent_tab.add('Home')
        parent_tab.add('Search')
        parent_tab.add('Records')

        # +++++++++++++++++++++++++++++++++++Home Tab 1 Frame++++++++++++++++++++++++++++++++++++
        frame1 = customtkinter.CTkFrame(master=parent_tab.tab('Home'), width=250, height=150, corner_radius=20)
        frame1.place(x=250, y=20)

        frame1_label2 = customtkinter.CTkLabel(master=frame1, text="Total \nPerson \n\n{}".format(total_person),
                                               font=labelfont)
        frame1_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

        # +++++++++++++++++++++++++++++++++++Home Tab 2 Frame++++++++++++++++++++++++++++++++++++
        frame2 = customtkinter.CTkFrame(master=parent_tab.tab('Home'), width=250, height=150, corner_radius=20)
        frame2.place(x=580, y=20)

        frame2_label2 = customtkinter.CTkLabel(master=frame2, text="Total \nDepartment \n\n5",
                                               font=labelfont)
        frame2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

        # +++++++++++++++++++++++++++++++++++Home Tab 3 Frame++++++++++++++++++++++++++++++++++++
        frame3 = customtkinter.CTkFrame(master=parent_tab.tab('Home'), width=250, height=150, corner_radius=20)
        frame3.place(x=900, y=20)

        frame3_label2 = customtkinter.CTkLabel(master=frame3,
                                               text="Total \nTimeKeeping \n\n{}".format(total_timekeeping),
                                               font=labelfont)
        frame3_label2.place(relx=0.5, rely=0.5, anchor=CENTER)




        # +++++++++++++++++++++++++++++++++++Service Tab 1 Frame++++++++++++++++++++++++++++++++++++
        tab2frame1 = customtkinter.CTkFrame(master=parent_tab.tab('Search'), width=250, height=150, corner_radius=20)
        tab2frame1.place(x=270, y=20)

        def search_person11():
            root = customtkinter.CTkToplevel()
            SearchPerson(root)
            root.mainloop()

        frame1_label1 = customtkinter.CTkButton(master=tab2frame1, text="Search \nPerson", command=search_person11,
                                                font=labelfont, fg_color='#2b2b2b', )
        frame1_label1.place(relx=0.5, rely=0.5, anchor=CENTER)

        # +++++++++++++++++++++++++++++++++++Service Tab 2 Frame++++++++++++++++++++++++++++++++++++
        tab2frame2 = customtkinter.CTkFrame(master=parent_tab.tab('Search'), width=250, height=150, corner_radius=20)
        tab2frame2.place(x=670, y=20)

        def search_department11():
            root = customtkinter.CTkToplevel()
            SearchDepartment(root)
            root.mainloop()

        frame2_label2 = customtkinter.CTkButton(master=tab2frame2, text="Search \nDepartment", command=search_department11,
                                                font=labelfont, fg_color='#2b2b2b', )
        frame2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)




        # +++++++++++++++++++++++++++++++++++Report Tab 3 Frame++++++++++++++++++++++++++++++++++++
        tab3frame3 = customtkinter.CTkFrame(master=parent_tab.tab('Records'), width=250, height=150, corner_radius=20)
        tab3frame3.place(x=290, y=20)

        def department_report720():
            root = customtkinter.CTkToplevel()
            DepartmentReport(root)
            root.mainloop()

        tab3_label3 = customtkinter.CTkButton(master=tab3frame3, text="Department \nReports", command=department_report720,
                                              font=labelfont, fg_color='#2b2b2b', )
        tab3_label3.place(relx=0.5, rely=0.5, anchor=CENTER)

        # +++++++++++++++++++++++++++++++++++Report Tab 4 Frame++++++++++++++++++++++++++++++++++++
        tab4frame4 = customtkinter.CTkFrame(master=parent_tab.tab('Records'), width=250, height=150, corner_radius=20)
        tab4frame4.place(x=670, y=20)

        def person_report720():
            root = customtkinter.CTkToplevel()
            PersonReport(root)
            root.mainloop()

        tab4_label4 = customtkinter.CTkButton(master=tab4frame4, command=person_report720, text="Person \nReports",
                                              font=labelfont,
                                              fg_color='#2b2b2b', )
        tab4_label4.place(relx=0.5, rely=0.5, anchor=CENTER)
        # Tạo Treeview
        AdminTable2 = ttk.Treeview(frameCenter)
        AdminTable2['columns'] = ('ID', 'Name', 'Mobile', 'Address', 'Position', 'Status', 'Timestamp','Count')
        AdminTable2.column('#0', width=0, stretch=0)
        AdminTable2.column('ID', width=180, anchor=tk.CENTER)
        AdminTable2.column('Name', width=240, anchor=tk.CENTER)
        AdminTable2.column('Address', width=150, anchor=tk.CENTER)
        AdminTable2.column('Mobile', width=150, anchor=tk.CENTER)
        AdminTable2.column('Position', width=150, anchor=tk.CENTER)
        AdminTable2.column('Status', width=220, anchor=tk.CENTER)
        AdminTable2.column('Timestamp', width=220, anchor=tk.CENTER)
        AdminTable2.column('Count', width=100, anchor=tk.CENTER)

        AdminTable2.heading('#0', text='', anchor=tk.CENTER)
        AdminTable2.heading('ID', text="ID", anchor=tk.CENTER)
        AdminTable2.heading('Name', text="Name", anchor=tk.CENTER)
        AdminTable2.heading('Address', text="Address", anchor=tk.CENTER)
        AdminTable2.heading('Mobile', text="Mobile", anchor=tk.CENTER)
        AdminTable2.heading('Position', text="Position", anchor=tk.CENTER)
        AdminTable2.heading('Status', text="Status", anchor=tk.CENTER)
        AdminTable2.heading('Timestamp', text="Timestamp", anchor=tk.CENTER)
        AdminTable2.heading('Count', text="Count", anchor=tk.CENTER)


        def populate_AdminTable():
            # Lấy dữ liệu từ ba bảng Person, Timekeeping và Attendance
            person_data = get_person_data()
            timekeeping_data = get_timekeeping_data()
            attendance_data = get_attendance_status()

            # Nếu dữ liệu được trả về từ cả ba bảng
            if person_data and timekeeping_data and attendance_data:
                for person_entry, timekeeping_entry, attendance_entry in zip(person_data, timekeeping_data,
                                                                             attendance_data):
                    # Lấy thông tin từ mỗi hàng dữ liệu
                    person_id, name, mobile, address, position = person_entry
                    timekeeping_id, timestamp, count = timekeeping_entry
                    attendance_status = "timed" if attendance_entry == 1 else "not yet scored"

                    # Hiển thị thông tin trong Treeview
                    AdminTable2.insert(parent='', index='end',
                                       values=(
                                           person_id, name, mobile, address, position, attendance_status, timestamp,count))
            else:
                print("Không có dữ liệu để hiển thị.")

        def show_detail(event):
            # Kiểm tra xem có hàng được chọn không
            if AdminTable2.selection():
                # Lấy id của hàng được chọn
                selected_item = AdminTable2.selection()[0]

                # Lấy thông tin từ hàng được chọn
                person_id, name, mobile, address, position, attendance_status, timestamp,count = AdminTable2.item(
                    selected_item, 'values')

                # Tạo cửa sổ mới để hiển thị chi tiết và truyền dữ liệu vào
                main = customtkinter.CTkToplevel()
                ViewPersonProfile(main, person_id, name, mobile, address, position, attendance_status, timestamp,count)
                main.mainloop()
            else:
                print("Vui lòng chọn một hàng để xem chi tiết.")

        # Gắn sự kiện click chuột vào mỗi hàng
        AdminTable2.bind("<Double-1>", show_detail)

        populate_AdminTable()
        AdminTable2.place(x=20, y=360)




if __name__=='__main__':
    main=customtkinter.CTk()
    Admin_Dashboard(main)
    main.mainloop()