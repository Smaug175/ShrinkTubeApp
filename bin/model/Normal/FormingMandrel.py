from datetime import date

from bin.model._BaseMold import BaseMoldClass

class DC0124_SS01(BaseMoldClass):
    def __init__(self, logger, CSC):
        """124成型芯轴"""
        super().__init__()
        self.logger = logger
        self.English_name = 'FormingMandrel'
        self.Chinese_name = '成型芯轴'

        self.global_config = CSC.get_config('全局参数')  # 读取全局配置
        self.global_twice_add = float(self.global_config['Global_Twice_add'])  # 读取全局配置的加0.3值
        self.config_dict = CSC.get_config(self.Chinese_name)  # 读取当前名字的配置

        self.parameters = {}

        self.change = False

        self.logger.info(self.Chinese_name+'初始化完成')

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            return

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        # D
        Tx_v = list(Tx.values())

        if Normal_Add:
            _D = float(D) - 2 * max(Tx_v) - float(self.config_dict['D_min'])
        else:
            self.logger.error('ERROR IN SET PARAMS: 成型退料模参数A必须是两抽。当前情况为一抽。')
            return

        self.parameters['%%CD'] = str(round(_D, 1))

        if float(self.parameters['%%CD']) < 36:
            self.parameters['M螺纹'] = 'M20'
        else:
            self.parameters['M螺纹'] = 'M36'

        # A, 减重孔直径
        self.parameters['%%CA'] = '/'

        # L， 减重孔深度
        self.parameters['L'] = '/'

        #LT
        Sum_Lx = L #总长度?

        min_L = float(self.config_dict['total_length_min'])
        max_L = float(self.config_dict['total_length_max'])

        if Sum_Lx +320 < min_L:
            self.parameters['LT'] = str(min_L)
        else:
            self.parameters['LT'] = str(max_L)

        #BXB,不明确
        self.parameters['BXB'] = '35X35'

        #件数：1
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True
        self.logger.info(self.Chinese_name+'参数设置成功')

class DC0121_SS01(BaseMoldClass):
    def __init__(self, logger, CSC):
        """121成型芯轴"""
        super().__init__()
        self.logger = logger
        self.English_name = 'FormingMandrel'
        self.Chinese_name = '成型芯轴'

        self.global_config = CSC.get_config('全局参数')  # 读取全局配置
        self.global_twice_add = float(self.global_config['Global_Twice_add'])  # 读取全局配置的加0.3值
        self.config_dict = CSC.get_config(self.Chinese_name)  # 读取当前名字的配置

        self.parameters = {}

        self.change = False

        self.logger.info(self.Chinese_name+'初始化完成')

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            return

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        # D
        Tx_v = list(Tx.values())

        if Normal_Add:
            _D = float(D) - 2 * max(Tx_v) - float(self.config_dict['D_min'])
        else:
            self.logger.error('ERROR IN SET PARAMS: 成型退料模参数A必须是两抽。当前情况为一抽。')
            return

        self.parameters['%%CD'] = str(round(_D, 1))

        if float(self.parameters['%%CD']) < 36:
            self.parameters['M螺纹'] = 'M20'
        else:
            self.parameters['M螺纹'] = 'M36'

        # A, 减重孔直径
        self.parameters['%%CA'] = '/'

        # L， 减重孔深度
        self.parameters['L'] = '/'

        #LT
        Sum_Lx = L #总长度?

        min_L = float(self.config_dict['total_length_min'])
        max_L = float(self.config_dict['total_length_max'])

        if Sum_Lx +320 < min_L:
            self.parameters['LT'] = str(min_L)
        else:
            self.parameters['LT'] = str(max_L)

        #BXB,不明确
        self.parameters['BXB'] = '25X25'

        #件数：1
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True
        self.logger.info(self.Chinese_name+'参数设置成功')


class DC0125_SS01(BaseMoldClass):
    def __init__(self, logger, CSC):
        """125成型芯轴"""
        super().__init__()
        self.logger = logger
        self.English_name = 'FormingMandrel'
        self.Chinese_name = '成型芯轴'

        self.global_config = CSC.get_config('全局参数')  # 读取全局配置
        self.global_twice_add = float(self.global_config['Global_Twice_add'])  # 读取全局配置的加0.3值
        self.config_dict = CSC.get_config(self.Chinese_name)  # 读取当前名字的配置

        self.parameters = {}

        self.change = False

        self.logger.info(self.Chinese_name+'初始化完成')

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            return

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        # D
        Tx_v = list(Tx.values())

        if Normal_Add:
            _D = float(D) - 2 * max(Tx_v) - float(self.config_dict['D_min'])
        else:
            self.logger.error('ERROR IN SET PARAMS: 成型退料模参数A必须是两抽。当前情况为一抽。')
            return

        self.parameters['%%CD'] = str(round(_D, 1))

        if float(self.parameters['%%CD']) < 36:
            self.parameters['M螺纹'] = 'M20'
        else:
            self.parameters['M螺纹'] = 'M36'

        # A, 减重孔直径
        self.parameters['%%CA'] = '/'

        # L， 减重孔深度
        self.parameters['L'] = '/'

        #LT
        Sum_Lx = L #总长度?

        min_L = float(self.config_dict['total_length_min'])
        max_L = float(self.config_dict['total_length_max'])

        if Sum_Lx +320 < min_L:
            self.parameters['LT'] = str(min_L)
        else:
            self.parameters['LT'] = str(max_L)

        #BXB,不明确
        self.parameters['BXB'] = '25X25'

        self.parameters['L1'] = L + 10

        #件数：1
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True
        self.logger.info(self.Chinese_name+'参数设置成功')