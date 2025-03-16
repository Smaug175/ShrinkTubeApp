import os
from bin.taper_bin.utils.Taper_SQL_Centences  import create_sentencesEC, insert_sentences_listEC
import sqlite3
import pandas as pd

class MoldControl:
    def __init__(self):
        # 按照不同的机床设置不同的数据文件
        self.database_path = {
            "EC0120": "database/taper-mold/EC0120.db",
            "EC0121": "database/taper-mold/EC0121.db"
        }

        # 创建数据的保存文件夹
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists('database/taper-mold'):
            os.makedirs('database/taper-mold')

        for key in self.database_path:
            if not os.path.exists(self.database_path[key]):
                conn = sqlite3.connect(self.database_path[key])
                cursor = conn.cursor()
                for table_name in create_sentencesEC[key]:
                    cursor.execute(create_sentencesEC[key][table_name])
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
            #print(key_data)
            machine_table_tuple = insert_sentences_listEC[machine][table_name][0]
            machine_table_insert_sentences = insert_sentences_listEC[machine][table_name][1]
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
            #print(machine_table_insert_sentences)
            #print(machine_table_insert_sentences, input)
            #print(input)
            cursor.execute(machine_table_insert_sentences, input)
            conn.commit()
            conn.close()
            #self.logger.info(key + ' 数据插入成功!')

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

        keys = insert_sentences_listEC[machine][big_graph_number][0]
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
        print(results)
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
