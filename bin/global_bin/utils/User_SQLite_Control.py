import os
import sqlite3

class UserControl:
    def __init__(self):
        create_user_table = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            license TEXT NOT NULL,
            authority TEXT NOT NULL
        )"""
        # "user", "admin"

        # 创建数据的保存文件夹
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists('database/user'):
            os.makedirs('database/user')

        self.database_path = 'database/user/user.db'

        if not os.path.exists(self.database_path):
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            cursor.execute(create_user_table)
            conn.commit()
            conn.close()
            print('用户数据库创建成功')

    def insert_data(self, data: dict):
        """注册：插入新的用户数据"""
        insert_user = """
        INSERT INTO user (id, name, password, license, authority) VALUES (?, ?, ?, ?, ?)
        """
        input = []
        for i in ('id', 'name', 'password', 'license', 'authority'):
            if i == 'id':
                input.append(int(data[i]))
            else:
                input.append(data[i])
        
        id = int(data['id'])
        select_sql = "SELECT * FROM user WHERE id = {}".format(id)
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute(select_sql)
        results = cursor.fetchall()
        conn.close()
        
        if len(results) != 0:
            print('用户已存在')
            return (False, '用户已存在')
        else:
            try:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                cursor.execute(insert_user, input)
                conn.commit()
                conn.close()
                print('用户注册成功')
                return (True, input[4])
            except Exception as e:
                print(e)
                return (False, '用户注册失败')
        
    def query(self, data):
        """登录：查询用户数据"""
        id = int(data['id'])
        password = data['password']
        select_sql = "SELECT * FROM user WHERE id = {}".format(id)

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute(select_sql)
        results = cursor.fetchall()
        conn.close()

        # ('id', 'name', 'password', 'license', 'authority')
        if len(results) == 0:
            print('用户不存在')
            return (False, '用户不存在')
        else:
            if password == results[0][2]:
                print('登录成功')
                return (True, results[0])
            else:
                print('密码错误')
                return (False, '密码错误')

    def delete(self, delete):
        pass

    def update(self, update):
        pass