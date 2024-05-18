from app.dbms.connection import Connect
import mysql.connector
import pandas as pd
import time
def get_total_person_count():
    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Person")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print("Lỗi khi lấy số lượng tổng cộng của người:", e)
        return 0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def get_total_timekeeping_count():
    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Timekeeping")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print("Lỗi khi lấy số lượng tổng cộng của thời gian chấm công:", e)
        return 0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
