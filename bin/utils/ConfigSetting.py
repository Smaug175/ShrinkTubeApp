import copy
import json
import os


class ConfigSettingClass:
    """配置文件设置类

    在这个类中设定了几个可修改的参数，用于计算时自定义计算结果。

    Methods
    _______
    _load_config() -> dict:
        加载配置文件
    save_config(customer_config_path, config_dict):
        保存配置文件
    get_config(key):
        获取配置文件
    set_config(key, value):
        设置配置文件
    get_all_config() -> dict:
        获取所有配置文件
    init_config():
        初始化设置数据,防止之后的操作出现错误，需要修复
    """
    def __init__(self, logger, config_path: str):
        """初始化配置文件"""

        self.logger = logger
        self.config_path = config_path

        self.config_dict = self._load_config()

        # TODO:有机会的话，这些都应当是使用完整图号来区分。
        # 设置
        self.initial_config = {
            '全局参数': {
                'Global_Twice_add': 0.3,
            },
            '缩管模': {
                'd_add': 5.55,
                'd1_add': 11.25,
            },
            '成型模': {
                'd_add': 5.55,
                'd1_add': 11.25,
            },
            '成型芯轴': {
                'D_min': 0.3,
                'total_length_min': 1060,
                'total_length_max': 1140,
            },
            '抽管芯轴': {
                'total_length_min': 1060,
                'total_length_max': 1140,
            },
            '抽管退料模': {
                'A_add': 0.2,
            },
            '成型退料模': {
                'A_min': 0.1,
            },
        }
        # 描述
        self.config_description = {
            '全局参数': {
                'Global_Twice_add': '二抽多加的数值',
            },
            '缩管模': {
                'd_add': '缩管模孔径d的额外加值',
                'd1_add': '缩管模孔径d1的额外加值',
            },
            '成型模': {
                'd_add': '成型模孔径d的额外加值',
                'd1_add': '成型模孔径d1的额外加值',
            },
            '成型芯轴': {
                'D_min': '成型芯轴直径D的额外减值',
                'total_length_min': '成型芯轴总长的最小值',
                'total_length_max': '成型芯轴总长的最大值',
            },
            '抽管芯轴': {
                'total_length_min': '抽管芯轴总长的最小值',
                'total_length_max': '抽管芯轴总长的最大值',
            },
            '抽管退料模': {
                'A_add': '抽管退料模孔径A的额外加值',
            },
            '成型退料模': {
                'A_min': '成型退料模孔径A的额外减值',
            },
        }

    def _load_config(self) -> dict:
        """加载配置文件"""

        try:
            with open(self.config_path, 'r') as f:
                config_dict = json.load(f)
            self.logger.info('配置文件加载成功')
        except FileNotFoundError:
            config_dict = {}
            self.logger.error('配置文件加载失败, 请检查路径是否正确，未找到该文件。')
            print('配置文件加载失败, 请检查路径是否正确，未找到该文件。报错位置：ConfigSettingClass._load_config')

        return config_dict

    def save_config(self, customer_config_path: str, config_dict: dict):
        '''保存配置文件'''

        new_data = copy.deepcopy(self.initial_config)

        for key in config_dict:
            dict1 = config_dict[key]
            for key1 in dict1:
                new_data[key][key1] = float(dict1[key1])

        with open(customer_config_path, 'w') as f:
            json.dump(new_data, f, indent=4)

        self.logger.info('保存配置文件成功')

    def get_config(self, key):
        '''获取配置文件'''

        self.logger.info('获取配置文件, key: {}'.format(key))
        return self.config_dict.get(key, None)

    def set_config(self, key, value):
        '''设置配置文件'''

        self.config_dict[key] = value
        self.save_config()
        self.logger.info('设置配置文件成功, key: {}, value: {}'.format(key, value))

    # def delete_config(self, key):
    #     '''删除配置文件'''
    #     if key in self.config_dict:
    #         del self.config_dict[key]
    #         self.save_config()

    def get_all_config(self) -> dict:
        '''获取所有配置文件'''

        self.logger.info('获取所有配置文件')
        return self.config_dict

    # def clear_all_config(self):
    #     self.config_dict = {}
    #     self.save_config()

    def init_config(self):
        """初始化设置数据,防止之后的操作出现错误，需要修复"""

        # 删除现有的配置文件
        try:
            os.remove('config/default.json')
            self.logger.info('删除配置文件成功')
        except FileNotFoundError:
            self.logger.error('删除配置文件失败，未找到该文件')
            print('删除配置文件失败，未找到该文件,报错位置：ConfigSettingClass.init_config')

        # 将JSON字符串写入文件
        with open('config/default.json', 'w') as json_file:
            json.dump(self.initial_config, json_file, indent=4)

        self.logger.info('配置文件初始化成功，已经生成默认配置文件，路径为：config/default.json')

        self.config_path = 'config/default.json'
        self.config_dict = self._load_config()
