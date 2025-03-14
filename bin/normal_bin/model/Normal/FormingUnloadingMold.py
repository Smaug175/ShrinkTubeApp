from datetime import date

from bin.normal_bin.model.Normal_Base_Mold import BaseMoldClass


class DC0124_AD02(BaseMoldClass):
    def __init__(self):
        """DC0124机器适用的成型退料模"""
        super().__init__()
        self.English_name = 'FormingUnloadingMold'
        self.Chinese_name = '成型退料模'

        self.parameters = {}

        self.change = False

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            #将df_params中的参数提取出来
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            return

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        Tx_v = list(Tx.values())

        if Normal_Add:
            A = float(D) - 2 * max(Tx_v) - 0.1
        else:
            return

        self.parameters['%%CA'] = str(round(A, 1))

        #件数：1
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True

class DC0121_AD02(BaseMoldClass):
    def __init__(self):
        """DC0121机器适用的成型退料模"""
        super().__init__()
        self.English_name = 'FormingUnloadingMold'
        self.Chinese_name = '成型退料模'

        self.parameters = {}

        self.change = False

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            #将df_params中的参数提取出来
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            return
        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        Tx_v = list(Tx.values())

        self.parameters['%%CD'] = str(round(D - 2 * max(Tx_v),1))

        self.parameters['A'] = str(15) # 固定值

        #件数：1
        self.parameters['件数'] = external_params['件数']

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True


class DC0125_AD06_F(BaseMoldClass):
    def __init__(self):
        """DC0125机器适用的抽管退料模"""
        super().__init__()
        self.English_name = 'FormingUnloadingMold'
        self.Chinese_name = '成型退料模'

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

        dx = []
        for x in range(len(Tx)):
            if Normal_Add:
                dx.append(D - 2 * Tx['T' + str(x + 1)] + 0.3)
            else:
                dx.append(D - 2 * Tx['T' + str(x + 1)])
        # print(dx)
        # print('here')

        new_D = max(dx) + 0.2 + 0.3  # 抽管芯轴最大直径 + 0.2 + 0.3

        self.parameters['%%CD'] = str(round(new_D, 1))

        #件数：1
        self.parameters['件数'] = external_params['件数']

        # 成品直径，专有参数
        self.parameters['成品直径'] = D

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True