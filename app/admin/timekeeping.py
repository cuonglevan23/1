from tkinter import *
from tkinter import messagebox
import cv2
from PIL import ImageTk, Image
import customtkinter
from app.dbms.person_management import get_person_list, check_last_attendance_time, update_last_attendance_time, \
    insert_into_attendance
from app.dbms.person_management import check_attendance_status
from app.dbms.person_management import timekeeping


class Timekeeping(customtkinter.CTk):

    def __init__(self, main):
        self.main = main
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.main.title("Time Keeping System")

        width = 2000
        height = 1800
        myscreenwidth = self.main.winfo_screenwidth()
        myscreenheight = self.main.winfo_screenheight()
        xCordinate = int((myscreenwidth / 2) - (width / 2))
        yCordinate = int((myscreenheight / 2) - (height / 2))
        self.main.geometry('{}x{}+{}+{}'.format(width, height, xCordinate + 200, yCordinate))
        self.main.maxsize(1800, 1200)

        # font
        font720 = customtkinter.CTkFont(family='Times New Roman', size=20, weight='normal')

        # Center Frame
        topFrame = customtkinter.CTkFrame(master=self.main, height=70)
        topFrame.pack(side=TOP, fill=X, padx=20, pady=(10, 20))

        # Title Label
        titleLabel = customtkinter.CTkLabel(master=topFrame, text="TIMEKEEPING", font=('Times New Roman', 25, 'bold'))
        titleLabel.pack(fill=X)

        # Center Frame
        centerFrame = customtkinter.CTkFrame(master=self.main, height=1000, width=1200)
        centerFrame.pack(side=LEFT, fill=BOTH, expand=True)

        # Left Frame
        self.leftFrame = customtkinter.CTkFrame(master=self.main, height=1000, width=200)
        self.leftFrame.pack(side=LEFT, fill=Y, padx=(20, 0))

        # Title Left Frame
        titleLeftFrame = customtkinter.CTkLabel(master=self.leftFrame, text="Danh sách người chấm công",
                                                font=('Times New Roman', 20, 'bold'))
        titleLeftFrame.pack(side=TOP, fill=X, padx=20, pady=20)

        # Thêm khung để hiển thị webcam
        self.webcam_label = customtkinter.CTkLabel(master=centerFrame)
        self.webcam_label.pack()

        # Nút bắt đầu nhận diện
        self.start_button = customtkinter.CTkButton(master=centerFrame, text="Start", command=self.start_recognition)
        self.start_button.pack(pady=20)

        # Thêm nhãn để hiển thị thông tin nhận diện
        self.recognized_face_label = customtkinter.CTkLabel(master=centerFrame, text="",
                                                            font=('Times New Roman', 20, 'bold'))
        self.recognized_face_label.pack(pady=20)

        # Khởi tạo webcam và các thuộc tính khác nhưng không bật nhận diện ngay lập tức
        self.cap = cv2.VideoCapture(0)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('/Users/lvc/PycharmProjects/pythonProject6/trainer/trainer.yml')
        self.faceCascade = cv2.CascadeClassifier(
            '/Users/lvc/PycharmProjects/pythonProject6/haarcascade_frontalface_default.xml')

        # Lấy danh sách tên từ cơ sở dữ liệu
        self.person_list = self.get_person_list()

    def get_person_list(self):
        person_list = get_person_list()
        return {person.getId(): person.getName() for person in person_list}

    def start_recognition(self):
        self.show_webcam()

    def show_webcam(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Lật ảnh ngang
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
        )

        recognized_faces = []  # Danh sách các khuôn mặt đã nhận diện được

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

            if (confidence < 100):
                name = self.person_list.get(id, "unknown")
                if name != "unknown":
                    self.mark_attendance(id)
                confidence_text = "  {0}%".format(round(100 - confidence))
            else:
                name = "unknown"
                confidence_text = "  {0}%".format(round(100 - confidence))

            cv2.putText(
                frame,
                str(name),
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )
            cv2.putText(
                frame,
                str(confidence_text),
                (x + 5, y + h - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                1
            )

            recognized_faces.append(f"Tên: {name}, ID: {id}")

        if recognized_faces:
            self.recognized_face_label.configure(text="\n".join(recognized_faces))

        frame = cv2.resize(frame, (1300, 800))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.webcam_label.imgtk = imgtk
        self.webcam_label.configure(image=imgtk)
        self.webcam_label.after(50, self.show_webcam)

    def getAttendanceStatus(self, person_id):
        return check_attendance_status(person_id)

    def display_attendance_list(self):
        # Lấy danh sách người chấm công từ cơ sở dữ liệu
        person_list = get_person_list()

        # Xóa nội dung hiện tại của leftFrame trước khi hiển thị danh sách mới
        for widget in self.leftFrame.winfo_children():
            widget.destroy()

        # Title Left Frame
        title_left_frame = customtkinter.CTkLabel(master=self.leftFrame, text="Danh sách người chấm công",
                                                  font=('Times New Roman', 20, 'bold'))
        title_left_frame.pack(side=TOP, fill=X, padx=20, pady=20)

        # Hiển thị danh sách người chấm công
        for person in person_list:
            person_frame = customtkinter.CTkFrame(master=self.leftFrame)
            person_frame.pack(anchor=W, padx=10, pady=10, fill=X)

            # Nhãn cho ID
            personID_label = customtkinter.CTkLabel(master=person_frame, text="ID: " + str(person.getId()),
                                                    width=20, height=20,
                                                    font=('Times New Roman', 16))
            personID_label.pack(side=LEFT, padx=(0, 10))

            # Nhãn cho Name
            person_label = customtkinter.CTkLabel(master=person_frame, text="Name: " + str(person.getName()),
                                                  width=20, height=20,
                                                  font=('Times New Roman', 16))
            person_label.pack(side=LEFT, padx=(10, 10))

            # Lấy trạng thái chấm công và hiển thị
            attendance_status = self.getAttendanceStatus(person.getId())
            status_text = "Đã chấm công" if attendance_status else "Chưa chấm công"
            status_label = customtkinter.CTkLabel(master=person_frame, text=status_text,
                                                  width=20, height=20,
                                                  font=('Times New Roman', 16))
            status_label.pack(side=LEFT, padx=(10, 0))

    def mark_attendance(self, person_id):
        # Kiểm tra thời gian điểm danh gần nhất
        allow_attendance = check_last_attendance_time(person_id)

        if allow_attendance:
            success = timekeeping(person_id)
            insert_into_attendance(person_id, 1)
            if success:
                # Cập nhật thời gian điểm danh mới nhất
                update_last_attendance_time(person_id)
                messagebox.showinfo("Success", "Điểm danh thành công!")

                # Cập nhật lại danh sách người chấm công
                self.display_attendance_list()
            else:
                messagebox.showerror("Error", "Điểm danh không thành công!")
        else:
            messagebox.showinfo("Info", "ID đã được điểm danh trong vòng 24 giờ.")


if __name__ == '__main__':
    main = customtkinter.CTk()
    timekeeping_instance = Timekeeping(main)

    timekeeping_instance.display_attendance_list()
    main.mainloop()
