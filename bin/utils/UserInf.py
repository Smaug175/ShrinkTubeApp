import json
import os
import re
import shutil

from cryptography.fernet import Fernet


def _is_passport_valid_(passport: str) -> bool:
    """判断密码是否符合要求，不对外调用

    密码需要至少3个字符，包含至少一个数字和一个字母
    """
    return re.match(r'^(?=.*[0-9])(?=.*[a-zA-Z]).{3,}$', passport) is not None


class UserManager:
    """用户管理

    用于用户的增删改查，以及用户的认证

    Methods
    -------
    create_user(user_ID, name, passport) -> str
        创建新用户
    delete_user(user_ID, name, passport)
        删除用户
    query_user(user_ID) -> dict
        查询用户信息
    authenticate_user(user_ID, passport)
        用户认证
    change_user_passport(user_ID, old_passport, new_passport) -> str
        修改用户密码
    """

    def __init__(self, logger):
        """用户管理初始化

        创建数据保存路径，读取密钥，移动数据路径
        """

        self.logger = logger

        # 读取密钥
        with open('bin/keys/user_key.txt', 'rb') as file:
            self.key = file.read()

        # 数据库文件夹，初次使用时创建
        if not os.path.exists('bin/local/'):
            os.makedirs('bin/local/')
        if not os.path.exists('bin/local/user/'):
            os.makedirs('bin/local/user/')

        # 新的数据路径，方便后续的数据迁移
        self.data_path = 'bin/local/user/user_db.enc'

        if not os.path.exists(self.data_path):
            # 新的数据路径也不存在，创建新的数据路径
            self.logger.warning(self.data_path + ' 加密文件不存在')
            self._auto_save_({})
            self.logger.info(self.data_path + ' 加密文件创建成功')
        # elif os.path.exists(self.data_path) and not os.path.exists(self.new_data_path):
        #     # 如果旧的数据路径存在，新的数据路径不存在，移动旧的数据路径到新的数据路径
        #     shutil.move(self.data_path, self.new_data_path)
        #     self.logger.info(self.data_path + ' 加密文件移动成功')

    def _read_data_(self):
        """读取数据，不对外调用"""

        if not os.path.exists(self.data_path):
            self.logger.error(self.data_path + ' 加密文件不存在')
            return None

        with open(self.data_path, 'rb') as f:
            encrypted_data = f.read()

        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        salt = os.urandom(16)
        salted_data = decrypted_data[len(salt):]
        deserialized_dict = json.loads(salted_data.decode())

        return deserialized_dict

    def _auto_save_(self, data_dict: dict):
        """自动保存数据，不对外调用"""

        # 将字典序列化为字符串
        serialized_dict = json.dumps(data_dict)
        salt = os.urandom(16)
        cipher_suite = Fernet(self.key)
        salted_data = salt + serialized_dict.encode()
        encrypted_data = cipher_suite.encrypt(salted_data)
        with open(self.data_path, 'wb') as f:
            f.write(encrypted_data)

        self.logger.info(self.data_path + ' 数据加密成功')

    def create_user(self, user_ID: str, name: str, passport: str) -> str:
        """增加新的用户"""

        all_users = self._read_data_()

        # 如果数据为空，初始化为空字典
        if all_users is None:
            all_users = {}

        if user_ID in all_users:
            self.logger.error("用户ID已存在")
            return "用户ID已存在。"
        if not _is_passport_valid_(passport):
            self.logger.error("密码不符合要求,密码需要至少3个字符，包含至少一个数字和一个字母")
            return "密码不符合要求。\n密码需要至少3个字符，包含至少一个数字和一个字母"

        all_users[user_ID] = {'name': name, 'passport': passport}

        self._auto_save_(all_users)

        self.logger.info(f"用户 {name} 创建成功。")

        return "True"

    def delete_user(self, user_ID: str, name: str, passport: str):
        """删除用户"""
        self._confirm_and_delete_(user_ID, name, passport)

    def _confirm_and_delete_(self, user_ID: str, name: str, passport: str) -> str:
        """确认用户信息并删除"""

        all_users = self._read_data_()

        if user_ID not in all_users:
            self.logger.error("用户ID不存在")
            return "用户ID不存在"

        user = all_users[user_ID]

        if user['name'] != name or user['passport'] != passport:
            self.logger.error("姓名或密码不匹配")
            return "姓名或密码不匹配"

        del all_users[user_ID]

        self.logger.info(f"用户 {name} 已删除。")

        # 保存余下的用户信息
        self._auto_save_(all_users)

        return "True"

    def query_user(self, user_ID: str) -> dict:
        """查询用户信息"""

        all_users = self._read_data_()

        if user_ID not in all_users:
            self.logger.error("用户{}不存在".format(user_ID))
            return {'ID': 'None', '姓名': 'None'}

        user = all_users[user_ID]

        self.logger.info("查询到：用户ID: {}, 姓名: {}".format(user_ID, user['name']))

        return {'ID': user_ID, '姓名': user['name']}

    def authenticate_user(self, user_ID: str, passport: str):
        """用户认证"""
        try:
            all_users = self._read_data_()
            if user_ID not in all_users:
                self.logger.error("用户ID不存在")
                return None

            user = all_users[user_ID]

            if user['passport'] == passport:
                self.logger.info(f"用户 {user['name']} 认证成功。")
                # print(f"用户 {user['name']} 认证成功。")
                return True
            else:
                self.logger.error(f"用户 {user['name']} 认证失败。密码错误！")
                # print(f"用户 {user['name']} 认证失败。密码错误！")
                return False
        except Exception as e:
            temp_str = ('用户认证失败！错误位置：\n'
                        ' UserManager -> authenticate_user(user_ID, passport) \n'
                        '错误信息：\n') + str(e)
            self.logger.error(temp_str)
            print(temp_str)

    def change_user_passport(self, user_ID, old_passport, new_passport) -> str:
        """修改用户密码"""
        # TODO: 还没有完善该功能
        users = self._read_data_()

        if user_ID not in users:
            self.logger.error("用户ID不存在")
            return "用户ID不存在"
        user = users[user_ID]
        if user['passport'] != old_passport:
            self.logger.error("旧密码不匹配")
            return "旧密码不匹配"
        if not _is_passport_valid_(new_passport):
            self.logger.error("新密码不符合要求")
            return "新密码不符合要求"

        user['passport'] = new_passport

        self._auto_save_(users)

        self.logger.info(f"用户 {user['name']} 的密码已成功修改。")

        return "True"
