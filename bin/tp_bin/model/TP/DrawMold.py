import sys
import os


from datetime import date
from bin.tp_bin.model.TP_Base_Mold import BaseMoldClass

class DC0128_ADIE(BaseMoldClass):
    def __init__(self):
        """抽套模"""
        super().__init__()
        self.English_name = 'TPDrawMold'
        self.Chinese_name = '抽套模'

        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):
        L, D, Lx, Mx, Tx, T_D, T_L, T_LR = self._get_tp_params_from_tube(tube_df_params)


        self.parameters['模具名称'] = self.Chinese_name
        self.parameters['图号'] = 'DC0128-' + external_params['图号']
        self.machine_type = 'DC0128'
        self.parameters['s_bore'] = str(D)  # 抽套模小口径
        self.parameters['b_bore'] = str(T_D)  # 抽套模大口径
        self.parameters['length'] = str(T_L)
        self.parameters['L'] = str(float(T_L) + 10)
        self.parameters['line'] = str(float(T_D) + 1) + 'mm'  # 成型TP抽形线，读取直径加1mm
        self.parameters['件数'] = '1'  # 成型抽套模件数

        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())

        self.change = True