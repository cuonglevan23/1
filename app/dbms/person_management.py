from app.dbms.connection import Connect
import mysql.connector
import pandas as pd
from app.libs.person_lib import Person_Libs
from datetime import datetime
import schedule
import time



def createPerson(person_info):
    # Tạo một đối tượng Person từ thông tin trong từ điển
    person = Person_Libs(id=person_info.getId(),
                         name=person_info.getName(),
                         mobile=person_info.getMobile(),
                         address=person_info.getAddress(),
                         position=person_info.getPosition())

    insert_sql = """
    INSERT INTO Person (id, name, mobile, address, position)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Lấy giá trị từ đối tượng `Person`
    values = (person.getId(), person.getName(), person.getMobile(), person.getAddress(), person.getPosition())

    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Kiểm tra xem `id` đã tồn tại chưa
        cursor.execute("SELECT * FROM Person WHERE id = %s", (person.getId(),))
        result = cursor.fetchone()

        if result is not None:
            # Nếu `id` đã tồn tại, thông báo và không chèn dữ liệu
            print(f"ID {person.getId()} đã tồn tại. Vui lòng nhập ID khác.")
            return

        # Thực thi câu lệnh chèn dữ liệu
        cursor.execute(insert_sql, values)

        # Lưu thay đổi vào cơ sở dữ liệu
        conn.commit()

        print("Đã tạo người mới thành công.")

    except mysql.connector.Error as err:
        print("Lỗi khi tạo người mới:", err)

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def timekeeping(person_id):
    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Kiểm tra xem `person_id` có tồn tại trong bảng Person không
        cursor.execute("SELECT * FROM Person WHERE id = %s", (person_id,))
        result = cursor.fetchone()

        if result is None:
            print(f"ID {person_id} không tồn tại. Vui lòng nhập ID hợp lệ.")
            return

        # Tạo thời gian hiện tại
        timestamp = datetime.now()

        # Kiểm tra số lần chấm công trong ngày của người đó
        cursor.execute("""
        SELECT COUNT(*) FROM Timekeeping 
        WHERE person_id = %s AND DATE(timestamp) = CURDATE()
        """, (person_id,))
        count = cursor.fetchone()[0]

        # Chèn thông tin chấm công mới
        insert_sql = """
        INSERT INTO Timekeeping (person_id, timestamp, count)
        VALUES (%s, %s, %s)
        """
        values = (person_id, timestamp, count + 1)
        cursor.execute(insert_sql, values)

        # Lưu thay đổi vào cơ sở dữ liệu
        conn.commit()

        print("Đã chấm công thành công.")

    except mysql.connector.Error as err:
        print("Lỗi khi chấm công:", err)

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_person_list():
    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Thực hiện truy vấn để lấy danh sách person
        cursor.execute("SELECT * FROM Person")
        results = cursor.fetchall()

        # Khởi tạo danh sách để lưu trữ các đối tượng Person
        person_list = []

        # Duyệt qua kết quả từ truy vấn và tạo các đối tượng Person tương ứng
        for row in results:
            person_info = Person_Libs(id=row[0], name=row[1], mobile=row[2], address=row[3], position=row[4])
            person_list.append(person_info)

        return person_list

    except mysql.connector.Error as err:
        print("Lỗi khi lấy danh sách person:", err)
        return None

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def check_attendance_status(person_id):
    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Thực hiện truy vấn để lấy trạng thái chấm công
        cursor.execute("SELECT status FROM attendance WHERE person_id = %s", (person_id,))
        result = cursor.fetchone()

        # Nếu không tìm thấy, mặc định là chưa chấm công (status = 0)
        if result is None:
            return False
        else:
            return result[0] == 1

    except mysql.connector.Error as err:
        print("Lỗi khi kiểm tra trạng thái chấm công:", err)
        return False

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def perform_timekeeping():
    person_list = get_person_list()
    if person_list:
        for person in person_list:
            timekeeping(person.getId())
    else:
        print("Không có danh sách person.")

def get_attendance_report():
    try:
        conn = Connect()
        cursor = conn.cursor()

        # Truy vấn để lấy số nhân viên đã chấm công trong ngày hiện tại
        query_attended = """
        SELECT COUNT(DISTINCT person_id) FROM Timekeeping WHERE DATE(timestamp) = CURDATE()
        """
        cursor.execute(query_attended)
        attended_count = cursor.fetchone()[0]

        # Truy vấn để lấy tổng số nhân viên
        query_total = """
        SELECT COUNT(*) FROM Person
        """
        cursor.execute(query_total)
        total_count = cursor.fetchone()[0]

        # Tính số nhân viên chưa chấm công
        not_attended_count = total_count - attended_count

        return attended_count, not_attended_count

    except mysql.connector.Error as err:
        print("Lỗi khi lấy báo cáo chấm công:", err)
        return None, None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def update_person_record(person_info):
    # Tạo một đối tượng Person từ thông tin trong từ điển
    person = Person_Libs(id=person_info.getId(),
                         name=person_info.getName(),
                         mobile=person_info.getMobile(),
                         address=person_info.getAddress(),
                         position=person_info.getPosition())

    update_sql = """
    UPDATE Person 
    SET name = %s, mobile = %s, address = %s, position = %s
    WHERE id = %s
    """

    # Lấy giá trị từ đối tượng `Person`
    values = (person.getName(), person.getMobile(), person.getAddress(), person.getPosition(), person.getId())

    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Kiểm tra xem `id` có tồn tại không
        cursor.execute("SELECT * FROM Person WHERE id = %s", (person.getId(),))
        result = cursor.fetchone()

        if result is None:
            # Nếu `id` không tồn tại, thông báo và không cập nhật dữ liệu
            print(f"ID {person.getId()} không tồn tại. Vui lòng nhập ID hợp lệ.")
            return

        # Thực thi câu lệnh cập nhật dữ liệu
        cursor.execute(update_sql, values)

        # Lưu thay đổi vào cơ sở dữ liệu
        conn.commit()

        print("Đã cập nhật thông tin thành công.")

    except mysql.connector.Error as err:
        print("Lỗi khi cập nhật thông tin:", err)

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def check_last_attendance_time(person_id):
    try:
        conn = Connect()
        cursor = conn.cursor()

        # Truy vấn để lấy thời gian điểm danh gần nhất
        cursor.execute("SELECT timestamp FROM Timekeeping WHERE person_id = %s ORDER BY timestamp DESC LIMIT 1", (person_id,))
        result = cursor.fetchone()

        if result:
            last_attendance_time = result[0]
            current_time = datetime.now()

            # Tính khoảng thời gian giữa thời điểm hiện tại và thời điểm điểm danh gần nhất
            time_diff = current_time - last_attendance_time

            # Nếu khoảng thời gian lớn hơn hoặc bằng 24 giờ, cho phép điểm danh
            if time_diff.total_seconds() >= 24 * 60 * 60:
                return True
            else:
                return False
        else:
            # Nếu không có thông tin điểm danh trước đó, cho phép điểm danh
            return True

    except mysql.connector.Error as err:
        print("Lỗi khi kiểm tra thời gian điểm danh gần nhất:", err)
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_last_attendance_time(person_id):
    try:
        conn = Connect()
        cursor = conn.cursor()

        # Lấy thời gian hiện tại
        timestamp = datetime.now()

        # Cập nhật thời gian điểm danh mới nhất cho người dùng
        cursor.execute("INSERT INTO Timekeeping (person_id, timestamp) VALUES (%s, %s)", (person_id, timestamp))
        conn.commit()

        print("Đã cập nhật thời gian điểm danh mới nhất.")

    except mysql.connector.Error as err:
        print("Lỗi khi cập nhật thời gian điểm danh:", err)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_into_attendance(person_id, status):
    try:
        conn = Connect()
        cursor = conn.cursor()

        # Chèn dữ liệu vào bảng Attendance
        cursor.execute("INSERT INTO Attendance (person_id, status) VALUES (%s, %s)", (person_id, status))
        conn.commit()

        print("Đã chèn dữ liệu vào bảng Attendance.")

    except mysql.connector.Error as err:
        print("Lỗi khi chèn dữ liệu vào bảng Attendance:", err)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    # Chạy chức năng chấm công mỗi ngày lúc 8h sáng
    while True:
        schedule.run_pending()
        time.sleep(1)
