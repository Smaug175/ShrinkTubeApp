import json
import uuid
import requests


class Request_Response():
    """发送请求，获取返回值

    Methods
    _______
    post_request()
        发送请求，获取返回值
    """

    def __init__(self, data):
        """初始化"""
        self.data = data
        self.url = 'http://47.121.209.63/'

    def post_request(self):
        """发送请求，获取返回值"""
        response = requests.post(self.url, json=self.data)
        return response

class AuthorizationClass:
    """服务器请求授权"""
    def __init__(self, logger):
        """初始化"""

        self.logger = logger

        # 初始化，获取license和mac地址，发送请求，获取返回值
        try:
            self.license = self.get_license()
        except:
            self.license = ''
            self.message = 'Error: 没有找到license文件'
            self.pass_ = False
            self.logger.error('Error: 没有找到license文件')
            print('Error: 没有找到license文件，位置：Authorization.__init__')

        self.mac_address = self.get_mac_address()
        self.Instance = {
            'AppID': self.license,
            'MAC': self.mac_address,
        }

        try:
            self.response = Request_Response(self.Instance)

            print(self.Instance)

            response_dict = json.loads(self.response.post_request().text)

            print(response_dict)

            self.message = response_dict['message']
            self.pass_ = response_dict['Pass']

            self.logger.info('Authorization: ' + self.message)
            self.logger.info('Authorization: ' + str(self.pass_))
        except:
            self.message = 'Error：无法连接到服务器'
            self.pass_ = False
            self.logger.error('Error: 无法连接到服务器')
            print('Error: 无法连接到服务器，位置：Authorization.__init__')

    def get_message_and_pass(self) -> tuple:
        """获取返回值"""
        return self.message, self.pass_

    def get_mac_address(self) -> str:
        """获取当前计算机的mac地址"""
        mac_address = uuid.getnode()
        mac_address_str = ':'.join(('%012x' % mac_address)[i:i+2] for i in range(0, 12, 2))
        return mac_address_str

    def get_license(self) -> str:
        """获取license的密钥"""
        path = 'License/license.key'
        with open(path, 'r') as file:
            license = file.read()
        return license