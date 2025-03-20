import os
from bin.tp_bin.utils.TP_SQL_Centences import create_sentences, insert_sentences_list
import sqlite3
import pandas as pd


class MoldControl:
    def __init__(self):
        self.database_path = {
            "DC0128": "../database/tp-mold/DC0128.db",
        }

        # 创建数据的保存文件夹
        if not os.path.exists('../database'):
            os.makedirs('../database')
        if not os.path.exists('../database/tp-mold'):
            os.makedirs('../database/tp-mold')

        for key in self.database_path:
            if not os.path.exists(self.database_path[key]):
                conn = sqlite3.connect(self.database_path[key])
                cursor = conn.cursor()
                for table_name in create_sentences[key]:
                    cursor.execute(create_sentences[key][table_name])
                conn.commit()
                conn.close()

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
                if mtt == '图号':  # 转换为数字保存
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
