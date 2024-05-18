import mysql.connector

def Connect():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='Security_Management_System'
        )
    except mysql.connector.Error as e:
        print("MySQL Connection Error:", str(e))

    finally:
     return conn
def get_timekeeping_data():
    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Truy vấn để lấy dữ liệu từ bảng Timekeeping
        cursor.execute("SELECT id, timestamp, count FROM Timekeeping")
        timekeeping_data = cursor.fetchall()

        return timekeeping_data

    except Exception as e:
        print("Lỗi khi lấy dữ liệu từ bảng Timekeeping:", e)
        return None

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_person_data():
    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Truy vấn để lấy dữ liệu từ bảng Person
        cursor.execute("SELECT id, name, mobile, address, position FROM Person")
        person_data = cursor.fetchall()

        return person_data

    except Exception as e:
        print("Lỗi khi lấy dữ liệu từ bảng Person:", e)
        return None

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def get_attendance_status():
    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Truy vấn để lấy trạng thái chấm công từ bảng Attendance
        cursor.execute("SELECT status FROM attendance")
        results = cursor.fetchall()

        # Trích xuất trạng thái chấm công từ kết quả truy vấn
        attendance_status = [result[0] for result in results]

        return attendance_status

    except mysql.connector.Error as err:
        print("Lỗi khi lấy trạng thái chấm công:", err)
        return None

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()

