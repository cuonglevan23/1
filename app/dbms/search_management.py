from app.dbms.connection import Connect
import mysql.connector
from app.libs.person_lib import Person_Libs

def search_person(search_criteria):
    try:
        # Kết nối với cơ sở dữ liệu
        conn = Connect()
        cursor = conn.cursor()

        # Xây dựng câu truy vấn SQL động dựa trên các tiêu chí tìm kiếm
        query = "SELECT * FROM Person WHERE 1=1"
        params = []

        if 'id' in search_criteria:
            query += " AND id = %s"
            params.append(search_criteria['id'])

        if 'name' in search_criteria:
            query += " AND name LIKE %s"
            params.append('%' + search_criteria['name'] + '%')

        if 'mobile' in search_criteria:
            query += " AND mobile LIKE %s"
            params.append('%' + search_criteria['mobile'] + '%')

        if 'address' in search_criteria:
            query += " AND address LIKE %s"
            params.append('%' + search_criteria['address'] + '%')

        if 'position' in search_criteria:
            query += " AND position LIKE %s"
            params.append('%' + search_criteria['position'] + '%')

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        # Khởi tạo danh sách để lưu trữ các đối tượng Person
        person_list = []

        # Duyệt qua kết quả từ truy vấn và tạo các đối tượng Person tương ứng
        for row in results:
            person_info = Person_Libs(id=row[0], name=row[1], mobile=row[2], address=row[3], position=row[4])
            person_list.append(person_info)

        return person_list

    except mysql.connector.Error as err:
        print("Lỗi khi tìm kiếm person:", err)
        return None

    finally:
        # Đóng con trỏ và kết nối
        if cursor:
            cursor.close()
        if conn:
            conn.close()
