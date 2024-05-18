from app.dbms.connection import Connect

def passwordChange(adminInfo):
    # Câu lệnh SQL để thay đổi mật khẩu
    sql = """UPDATE admin SET password = %s WHERE email = %s"""
    values = (adminInfo.getPassword(), adminInfo.getEmail())

    try:
        conn = Connect()
        cursor = conn.cursor()

        # Thực hiện cập nhật
        cursor.execute(sql, values)
        conn.commit()

        if cursor.rowcount == 0:
            print("Không tìm thấy người dùng với email:", adminInfo.getEmail())
        else:
            print("Mật khẩu của người dùng với email '{}' đã được thay đổi.".format(adminInfo.getEmail()))

    except mysql.connector.Error as e:
        print("Lỗi khi thay đổi mật khẩu:", str(e))
    finally:
        # Đảm bảo đóng kết nối và giải phóng tài nguyên
        if cursor:
            cursor.close()
        if conn:
            conn.close()


