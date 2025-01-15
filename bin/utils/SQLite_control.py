import os
from bin.utils.normal_sql_centences import create_sentences, insert_sentences_list
import sqlite3
import pandas as pd

class MoldControl:
    def __init__(self, logger=None):
        # self.logger = logger

        # 按照不同的机床设置不同的数据文件
        self.database_path = {
            "DC0124": "database/normal-mold/DC0124.db",
            "DC0121": "database/normal-mold/DC0121.db",
            "DC0125": "database/normal-mold/DC0125.db",
        }

        # 创建数据的保存文件夹
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists('database/normal-mold'):
            os.makedirs('database/normal-mold')

        for key in self.database_path:
            if not os.path.exists(self.database_path[key]):
                # self.logger.error(self.database_path[key] + ' 数据库不存在')
                conn = sqlite3.connect(self.database_path[key])
                cursor = conn.cursor()
                for table_name in create_sentences[key]:
                    cursor.execute(create_sentences[key][table_name])
                conn.commit()
                conn.close()
                # self.logger.info(self.database_path[key] + ' 数据库创建成功')

    def insert_data(self, data: dict):
        keys = data.keys()
        for key in keys:
            if key == '管件参数':
                continue
            machine = key[:6]
            table_name = key[7:-4]
            numbers = int(key[-4:])
            key_data = data[key]
            machine_table_tuple = insert_sentences_list[machine][table_name][0]
            machine_table_insert_sentences = insert_sentences_list[machine][table_name][1]
            input = []
            for mtt in machine_table_tuple:
                if mtt == '%%Cd0':
                    # 将符号进行替换
                    mtt = '%%Cd'
                if mtt == '图号': # 转换为数字保存
                    input.append(numbers)
                else:
                    input.append(str(key_data[mtt]))
            # print(machine, table_name, key_data,machine_table_tuple, input)
            conn = sqlite3.connect(self.database_path[machine])
            cursor = conn.cursor()
            # print(machine_table_insert_sentences)
            # print(machine_table_insert_sentences, input)
            cursor.execute(machine_table_insert_sentences, input)
            conn.commit()
            conn.close()
            # self.logger.info(key + ' 数据插入成功!')

    def query(self, machine, big_graph_number):
        select_sql = "SELECT * FROM {}".format(big_graph_number)

        conn = sqlite3.connect(self.database_path[machine])
        cursor = conn.cursor()
        cursor.execute(select_sql)
        results = cursor.fetchall()
        conn.close()

        data = []
        for result in results:
            result_list = list(result)
            str_number = str(result_list[0])

            if len(str_number) != 4:
                new_number = big_graph_number + '0' * (4 - len(str_number)) + str_number
            else:
                new_number = big_graph_number + str_number

            graph_number = machine + '-' + new_number
            result_list[0] = graph_number
            data.append(result_list)

        keys = insert_sentences_list[machine][big_graph_number][0]
        keys_list = list(keys)
        for i in range(len(keys_list)):
            if keys_list[i] == '%%Cd0':
                keys_list[i] = '%%Cd'
                continue

        # 创建DataFrame
        df = pd.DataFrame(data, columns=keys_list)

        return df
    
    def query_max_graph_number(self, machine, big_graph_number):
        select_sql = "SELECT * FROM {}".format(big_graph_number)
        
        conn = sqlite3.connect(self.database_path[machine])
        cursor = conn.cursor()
        cursor.execute(select_sql)
        results = cursor.fetchall()
        conn.close()

        if results == []:
            return 0
        else:
            id_list = []
            for result in results:
                id_list.append(result[0])
            return max(id_list)

    def delete(self, delete):
        # TODO
        pass

    def update(self, update):
        # TODO
        pass


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