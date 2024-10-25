import json
import os
from cryptography.fernet import Fernet


class CryptoDataClass:
    """数据加密类

    该类用于对数据进行加密和解密，对数据进行加密后，将数据保存到对应的数据库中

    Methods
    _______
    encrypt_data(data: dict) -> None:
        加密数据，将数据保存到对应的数据库中
    decrypt_file_by_path(data_path: str) -> dict:
        根据文件路径，解密文件，返回字典
    decrypt_file_by_big_graph_number(big_graph_number: str) -> dict:
        根据大图号，解密文件，返回字典
    decrypt_all_project() -> dict:
        获得所有的项目数据
    query_data_by_Bicycle_Frame_Information(Bicycle_Frame_Information: str) -> dict:
        通过车架的信息查询数据
    query_data_by_graph_number(graph_number: str) -> dict:
        通过图号的信息查询数据
    delete_Bicycle_Frame_Information(Bicycle_Frame_Information: str) -> None:
        删除给定车架信息的数据
    delete_graph_number(graph_number: str) -> None:
        只删除图号对应的数据，项目数据库中的数据将删除编号
    save_by_key_and_graph_number(project_name: str, mold_name: str, mold_data: dict) -> None:
        根据项目名字保存数据，将新的数据写入到对应的数据库中
    query_all_mold_by_mold_name(mold_name: str) -> dict:
        通过模具的名字查询数据
    """
    def __init__(self, logger):
        """初始化数据加密类"""
        
        # 读取密钥
        self.key = open('bin/keys/db_key.txt', 'rb').read()
        
        self.logger = logger
        
        # TODO: 修改路径
        # 不同的机器的图号不同，需要根据机器的名称来获取
        # 唯一指定存放位置，不要轻易更改（十分重要）
        self.Project_db = 'bin/local/database/Project.enc'
        self.database_path = {
            # DC0124
            "DC0124-AD03": "bin/local/database/mold/DC0124-AD03.enc",
            "DC0124-DIEO": "bin/local/database/mold/DC0124-DIEO.enc",
            "DC0124-SS01": "bin/local/database/mold/DC0124-SS01.enc",
            "DC0124-AD02": "bin/local/database/mold/DC0124-AD02.enc",
            "DC0124-ADIE": "bin/local/database/mold/DC0124-ADIE.enc",
            "DC0124-ADBT": "bin/local/database/mold/DC0124-ADBT.enc",
            "DC0124-AD01": "bin/local/database/mold/DC0124-AD01.enc",
            # DC0121
            "DC0121-AD03": "bin/local/database/mold/DC0121-AD03.enc",
            "DC0121-AD04": "bin/local/database/mold/DC0121-AD04.enc",
            "DC0121-DIEO": "bin/local/database/mold/DC0121-DIEO.enc",
            "DC0121-SS01": "bin/local/database/mold/DC0121-SS01.enc",
            "DC0121-AD02": "bin/local/database/mold/DC0121-AD02.enc",
            "DC0121-ADIE": "bin/local/database/mold/DC0121-ADIE.enc",
            "DC0121-ADBT": "bin/local/database/mold/DC0121-ADBT.enc",
            "DC0121-AD01": "bin/local/database/mold/DC0121-AD01.enc",
            # DC0125
            "DC0125-AD06_F": "bin/local/database/mold/DC0125-AD06.enc",
            "DC0125-AD06_S": "bin/local/database/mold/DC0125-AD06.enc",
            "DC0125-AD07": "bin/local/database/mold/DC0125-AD07.enc",
            "DC0125-DIEO": "bin/local/database/mold/DC0125-DIEO.enc",
            "DC0125-SS01": "bin/local/database/mold/DC0125-SS01.enc",
            "DC0125-ADIE": "bin/local/database/mold/DC0125-ADIE.enc",
            "DC0125-ADBT": "bin/local/database/mold/DC0125-ADBT.enc",
        }

        if not os.path.exists('bin/local/database'):
            os.makedirs('bin/local/database')# 创建数据库文件夹
        if not os.path.exists('bin/local/database/mold'):
            os.makedirs('bin/local/database/mold')# 创建模具数据库文件夹

        # 检查是否存在加密文件，不存在则创建
        for key in self.database_path:
            if not os.path.exists(self.database_path[key]):
                self.logger.error(self.database_path[key] + ' 加密文件不存在')
                with open(self.database_path[key], 'wb') as f:
                    f.write(b'')
                self.logger.info(self.database_path[key] + ' 加密文件创建成功')

        if not os.path.exists(self.Project_db):
            self.logger.error(self.Project_db + ' 加密文件不存在')
            with open(self.Project_db, 'wb') as f:
                f.write(b'')
            self.logger.info(self.Project_db + ' 加密文件创建成功')

    def _save(self, data_dict: dict, data_path: str):
        """自动保存数据，不对外调用"""
        
        serialized_dict = json.dumps(data_dict)
        salt = os.urandom(16)
        cipher_suite = Fernet(self.key)
        salted_data = salt + serialized_dict.encode()
        encrypted_data = cipher_suite.encrypt(salted_data)
        with open(data_path, 'wb') as f:
            f.write(encrypted_data)
        self.logger.info(data_path + ' 数据加密成功')

    def encrypt_data(self, data: dict):
        """加密数据，将数据保存到对应的数据库中"""
        
        # 解析数据格式, 不保存管件参数，只保存模具参数和项目的整个数据
        car_spec = data['管件参数']['车种规格']
        project_dict = self.decrypt_file_by_path(self.Project_db)

        if project_dict != {}:
            project_dict[car_spec] = data
        else:
            # print('Info:',self.Project_db + ' 加密文件不存在，将按照新的格式创建')
            self.logger.info(self.Project_db + ' 加密文件不存在，将按照新的格式创建')
            project_dict = {
                car_spec: data,
            }

        self._save(project_dict, self.Project_db)
        self.logger.info('项目数据加密成功')

        data.pop('管件参数')  # 删除管件参数

        # 将模具参数保存到对应的模具数据库中
        # print(data.keys())
        for key in data.keys():
            mold_graph_number = key[:-4]
            data_dict = self.decrypt_file_by_path(self.database_path[mold_graph_number])
            # pprint(data_dict)
            if data_dict != {}:
                data_dict[data[key]['图号']] = data[key]
            else:
                # print('Info:',self.database_path[mold_graph_number] + ' 加密文件不存在，将按照新的格式创建')
                self.logger.info(self.database_path[mold_graph_number] + ' 加密文件不存在，将按照新的格式创建')
                data_dict = {data[key]['图号']: data[key],}
            self._save(data_dict, self.database_path[mold_graph_number])
            self.logger.info(key + ' 数据加密成功')
            print(key + ' 数据加密成功')

    def decrypt_file_by_path(self, data_path: str) -> dict:
        """根据文件路径，解密文件，返回字典"""
        try:
            with open(data_path, 'rb') as f:
                encrypted_data = f.read()

            cipher_suite = Fernet(self.key)
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            salt = os.urandom(16)
            salted_data = decrypted_data[len(salt):]
            deserialized_dict = json.loads(salted_data.decode())
        except:
            self.logger.error(data_path + ' 加密文件没有任何信息！')
            return {}

        self.logger.info(data_path + ' 加密文件解密成功')
        return deserialized_dict

    def decrypt_file_by_big_graph_number(self, big_graph_number: str) -> dict:
        """根据大图号，解密文件，返回字典"""
        
        with open(self.database_path[big_graph_number], 'rb') as f:
            encrypted_data = f.read()

        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        salt = os.urandom(16)
        salted_data = decrypted_data[len(salt):]
        deserialized_dict = json.loads(salted_data.decode())

        self.logger.info(self.database_path[big_graph_number] + ' 加密文件解密成功')
        return deserialized_dict

    def decrypt_all_project(self,) -> dict:
        """获得所有的项目数据"""

        with open(self.Project_db, 'rb') as f:
            encrypted_data = f.read()

        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        salt = os.urandom(16)
        salted_data = decrypted_data[len(salt):]
        deserialized_dict = json.loads(salted_data.decode())

        self.logger.info(self.Project_db + ' 加密文件解密成功')

        return deserialized_dict

    def query_data_by_Bicycle_Frame_Information(self, Bicycle_Frame_Information: str) -> dict:
        """通过车架的信息查询数据"""

        all_data = self.decrypt_all_project()

        if Bicycle_Frame_Information in all_data:
            select_data = {Bicycle_Frame_Information: all_data[Bicycle_Frame_Information]}
        else:
            select_data = {}

        return select_data

    def query_data_by_graph_number(self, graph_number: str) -> dict:
        """通过图号的信息查询数据"""

        all_data = self.decrypt_all_project()
        select_data = {}
        for key in all_data:
            for mold in all_data[key]:
                if mold == '管件参数':
                    continue
                if all_data[key][mold]['图号'] == graph_number:
                    select_data[key] = all_data[key]
                    break
        self.logger.info('按照{}查询到的数据'.format(graph_number))
        return select_data

    def delete_Bicycle_Frame_Information(self, Bicycle_Frame_Information: str):
        """删除给定车架信息的数据"""

        select_data = self.query_data_by_Bicycle_Frame_Information(Bicycle_Frame_Information)

        self.logger.info('准备按照{}删除数据'.format(Bicycle_Frame_Information))

        # 首先删除项目数据库中的数据
        project_dict = self.decrypt_file_by_path(self.Project_db)
        project_dict.pop(Bicycle_Frame_Information)
        self._save(project_dict, self.Project_db)
        # print('删除项目数据库中的数据成功')

        # 删除模具数据库中的数据
        for key in select_data[Bicycle_Frame_Information].keys():
            if key != '管件参数':
                temp = key[:-4]
                data_dict = self.decrypt_file_by_big_graph_number(temp)
                data_dict.pop(key)
                self._save(data_dict, self.database_path[temp])

        self.logger.info('按照{}删除数据成功'.format(Bicycle_Frame_Information))

    def delete_graph_number(self, graph_number: str):
        """只删除图号对应的数据，项目数据库中的数据将删除编号"""

        # 首先删除项目数据库中的数据
        project_dict = self.decrypt_file_by_path(self.Project_db)
        # pprint(project_dict)
        for project in project_dict:
            project_dict[project].pop(graph_number)
        self._save(project_dict, self.Project_db)
        # print('删除项目数据库中的数据成功')

        data_dict = self.decrypt_file_by_big_graph_number(graph_number[:-4])
        data_dict.pop(graph_number)
        self._save(data_dict, self.database_path[graph_number[:-4]])
        # print('删除{}数据库中的数据成功'.format(mold))

        self.logger.info('按照{}删除数据成功'.format(graph_number))

    def save_by_key_and_graph_number(self, project_name: str, mold_name: str, mold_data: dict):
        """根据项目名字保存数据，将新的数据写入到对应的数据库中"""
        # TODO: 改方法已经废弃，不再使用
        # 首先保存到项目数据库中
        project_dict = self.decrypt_file_by_path(self.Project_db)
        # pprint(project_dict)
        project_dict[project_name][mold_name] = mold_data['图号']
        self._save(project_dict, self.Project_db)
        # print('将数据保存到项目数据库中成功')

        data_dict = self.decrypt_file_by_big_graph_number(mold_name)
        data_dict[mold_data['图号']] = mold_data
        self._save(data_dict, self.database_path[mold_name])
        # print('将数据保存到{}数据库中成功'.format(mold_name))

        self.logger.info('按照{}保存数据成功'.format(mold_data['图号']))

    def query_all_mold_by_mold_name(self,mold_name: str) -> dict:
        """通过模具的名字查询数据"""
        data_dict = self.decrypt_file_by_big_graph_number(mold_name)
        self.logger.info('按照{}查询到的数据'.format(mold_name))
        return data_dict