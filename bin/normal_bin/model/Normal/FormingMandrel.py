from datetime import date

from bin.normal_bin.model.Normal_Base_Mold import BaseMoldClass

class DC0124_SS01(BaseMoldClass):
    def __init__(self):
        """124成型芯轴"""
        super().__init__()
        self.English_name = 'FormingMandrel'
        self.Chinese_name = '成型芯轴'

        self.parameters = {}

        self.change = False

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            return

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        # D
        Tx_v = list(Tx.values())

        if Normal_Add:
            _D = float(D) - 2 * max(Tx_v) - 0.3
        else:
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

        min_L = 1060
        max_L = 1140

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

class DC0121_SS01(BaseMoldClass):
    def __init__(self):
        """121成型芯轴"""
        super().__init__()
        self.English_name = 'FormingMandrel'
        self.Chinese_name = '成型芯轴'

        self.parameters = {}

        self.change = False

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            return

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        # D
        Tx_v = list(Tx.values())

        if Normal_Add:
            _D = float(D) - 2 * max(Tx_v) - 0.3
        else:
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

        min_L = 1060
        max_L = 1140

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


class DC0125_SS01(BaseMoldClass):
    def __init__(self):
        """125成型芯轴"""
        super().__init__()
        self.English_name = 'FormingMandrel'
        self.Chinese_name = '成型芯轴'

        self.parameters = {}

        self.change = False

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            return

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        # D
        Tx_v = list(Tx.values())

        if Normal_Add:
            _D = float(D) - 2 * max(Tx_v) - 0.3
        else:
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

        min_L = 1060
        max_L = 1140

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