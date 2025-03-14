import sys
import os

from datetime import date
from bin.tp_bin.model.TP_Base_Mold import BaseMoldClass

class DC0128_AD01_(BaseMoldClass):
    def __init__(self):
        """TP裁剪夹模2"""
        super().__init__()
        self.English_name = 'TPCuttingClipMold2'
        self.Chinese_name = '裁剪夹模2'


        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):
        L, D, Lx, Mx, Tx, T_D, T_L, T_LR = self._get_tp_params_from_tube(tube_df_params)

        self.parameters['模具名称'] = self.Chinese_name
        self.parameters['图号'] = 'DC0128-' + external_params['图号']
        self.machine_type = 'DC0128'
        self.parameters['%%CD'] = str(D)  # 大直径裁剪夹模直径
        self.parameters['件数'] = '2'  # 裁剪夹模件数
        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())

        self.change = True