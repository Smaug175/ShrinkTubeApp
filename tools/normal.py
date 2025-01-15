from bin.utils.AutoLogger import AutoLoggerClass

from bin.utils.ConfigSetting import ConfigSettingClass

logger = AutoLoggerClass()
# 加密数据的实例
# crypto_data_instance = CryptoDataClass(logger)

# 配置文件的路径，初始化为默认配置文件
config_path = 'config/default.json'
config_setting_instance = ConfigSettingClass(logger, config_path)

# 不同机床，是否成型操作，导致模具的选择有所不同
MOLDS = {
        'DC0124': ['裁剪夹模', '缩管模', '抽管芯轴', '抽管退料模'],
        'DC0124 forming': ['裁剪夹模', '成型模', '成型芯轴', '成型退料模', '缩管模', '抽管芯轴', '抽管退料模'],
        'DC0121': ['裁剪夹模1', '裁剪夹模2', '缩管模', '抽管芯轴', '抽管退料模'],
        'DC0121 forming': ['裁剪夹模1', '裁剪夹模2', '成型模', '成型芯轴', '成型退料模', '缩管模', '抽管芯轴', '抽管退料模'],
        'DC0125': ['裁剪夹模', '缩管模', '抽管芯轴', '抽管退料模'],
        'DC0125 forming': ['裁剪夹模', '成型模', '成型芯轴', '成型退料模', '缩管模', '抽管芯轴', '抽管退料模']
    }