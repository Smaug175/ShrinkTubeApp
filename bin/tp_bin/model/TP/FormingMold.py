import sys
import os

from datetime import date
from bin.tp_bin.model.TP_Base_Mold import BaseMoldClass

class DC0128_ADIE_(BaseMoldClass):
    def __init__(self):
        """成型抽套模"""
        super().__init__()
        self.English_name = 'TPFormingMold'
        self.Chinese_name = '成型抽套模'

        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):
        L, D, Lx, Mx, Tx, T_D, T_L, T_LR = self._get_tp_params_from_tube(tube_df_params)

        self.parameters['模具名称'] = self.Chinese_name
        self.parameters['图号'] = 'DC0128-' + external_params['图号']
        self.machine_type = 'DC0128'

        self.parameters['s_bore'] = str(tube_df_params.get('D', ''))#成型抽套模小口径，暂时未知T_d先用D代替 
        self.parameters['b_bore'] = str(tube_df_params.get('T_D', ''))#成型抽套模大口径
        self.parameters['length'] = str(tube_df_params.get('T_L', ''))#成型抽套模长度   
        self.parameters['line'] = '正常读取'

        self.parameters['件数'] = '1'
        self.parameters['车种规格'] = external_params.get('车种规格', '')
        self.parameters['设计者'] = external_params.get('设计者', '')
        self.parameters['日期'] = str(date.today())

        self.change = True