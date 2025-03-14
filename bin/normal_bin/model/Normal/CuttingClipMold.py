from datetime import date

from bin.normal_bin.model.Normal_Base_Mold import BaseMoldClass


class DC0124_AD03(BaseMoldClass):
    def __init__(self):
        """DC0124机器适用的裁剪夹模"""
        super().__init__()

        self.English_name = 'CuttingClipMold'
        self.Chinese_name = '裁剪夹模'

        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            return

        self.parameters['模具名称'] = self.Chinese_name
        # 机器类型
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        self.parameters['%%CD'] = str(D)

        #件数
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True

class DC0124_AD03_(BaseMoldClass):
    def __init__(self):
        """这个裁剪夹模_用于保存DC0124抽管时，额外的重复图纸。因为其图号与裁剪夹模重复，所以单独用一个模型保存。"""
        super().__init__()

        self.English_name = 'CuttingClipMold_'
        self.Chinese_name = '裁剪夹模_'

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

        self.parameters['%%CD'] = str(D + abs(Tx['T2']-Tx['T3']))

        #件数
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True

class DC0121_AD03(BaseMoldClass):
    def __init__(self):
        """DC0121机器适用的裁剪夹模1"""
        super().__init__()
        self.English_name = 'CuttingClipMold1'
        self.Chinese_name = '裁剪夹模1'

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

        self.parameters['%%CD'] = str(D)

        self.parameters['A'] = '70'

        #件数
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True


class DC0121_AD04(BaseMoldClass):
    def __init__(self, ):
        """DC0121机器适用的裁剪夹模2"""
        super().__init__()

        self.English_name = 'CuttingClipMold2'
        self.Chinese_name = '裁剪夹模2'

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


        self.parameters['%%CD'] = str(D)

        self.parameters['A'] = '70'

        #件数
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True


class DC0125_AD07(BaseMoldClass):
    def __init__(self):
        """DC0125机器适用的裁剪夹模"""
        super().__init__()

        self.English_name = 'CuttingClipMold'
        self.Chinese_name = '裁剪夹模'

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

        self.parameters['%%CD'] = str(D)

        #件数
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True