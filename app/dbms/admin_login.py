from app.dbms.connection import Connect
import mysql.connector
import sys
from app.libs.admin_libs import Admin_Libs


def adminLogin(adminInfo):

    sql="""SELECT * FROM admin WHERE email=%s and password=%s"""
    values=(adminInfo.getEmail(), adminInfo.getPassword())
    adminresult=None

    try:
        conn=Connect()
        cursor=conn.cursor()
        cursor.execute(sql, values)
        adminresult=cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print("Error", sys.exc_info())

    finally:
        del values, sql
        return adminresult




def createAdmin(adminInfo):
    # Xác định SQL để chèn bản ghi mới
    sql = """
        INSERT INTO admin (name, gender, mobile, email, address, password, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        adminInfo.getName(),
        adminInfo.getGender(),
        adminInfo.getMobile(),
        adminInfo.getEmail(),
        adminInfo.getAddress(),
        adminInfo.getPassword(),
        adminInfo.getStatus()
    )

    try:
        conn = Connect()
        cursor = conn.cursor()

        # Kiểm tra xem người dùng đã tồn tại chưa
        check_sql = "SELECT * FROM admin WHERE email = %s"
        cursor.execute(check_sql, (adminInfo.getEmail(),))
        existing_admin = cursor.fetchone()

        if existing_admin:
            print(f"Admin với email '{adminInfo.getEmail()}' đã tồn tại.")
            return None

        # Thêm người dùng mới vào cơ sở dữ liệu
        cursor.execute(sql, values)
        conn.commit()

        print(f"Admin '{adminInfo.getEmail()}' đã được tạo thành công.")

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()
def updateAdmin(adminInfo):
    # Xác định SQL để cập nhật thông tin người dùng
    sql = """
        UPDATE admin
        SET name = %s, gender = %s, mobile = %s, email = %s, address = %s, password = %s, status = %s
        WHERE email = %s
    """
    values = (
        adminInfo.getName(),
        adminInfo.getGender(),
        adminInfo.getMobile(),
        adminInfo.getEmail(),
        adminInfo.getAddress(),
        adminInfo.getPassword(),
        adminInfo.getStatus(),
        adminInfo.getEmail()  # Dùng email để tìm người dùng
    )

    try:
        conn = Connect()
        cursor = conn.cursor()

        # Cập nhật thông tin người dùng
        cursor.execute(sql, values)
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Admin '{adminInfo.getEmail()}' đã được cập nhật thành công.")
        else:
            print(f"Admin '{adminInfo.getEmail()}' không tồn tại.")

    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()




