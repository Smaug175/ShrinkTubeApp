import sys
import os

from datetime import date
from bin.tp_bin.model.TP_Base_Mold import BaseMoldClass

class DC0128_ADBT_(BaseMoldClass):
    def __init__(self):
        """成型抽管芯轴"""
        super().__init__()
        self.English_name = 'TPFormingMold'
        self.Chinese_name = '成型抽管芯轴'

        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):
        L, D, Lx, Mx, Tx, T_D, T_L, T_LR = self._get_tp_params_from_tube(tube_df_params)

        # 将提取的参数转换为浮点数类型
        L = float(L) if isinstance(L, str) else L
        D = float(D) if isinstance(D, str) else D
        Lx = {k: float(v) if isinstance(v, str) else v for k, v in Lx.items()}
        Mx = {k: float(v) if isinstance(v, str) else v for k, v in Mx.items()}
        Tx = {k: float(v) if isinstance(v, str) else v for k, v in Tx.items()}
        T_D = float(T_D) if isinstance(T_D, str) else T_D
        T_L = float(T_L) if isinstance(T_L, str) else T_L
        T_LR = float(T_LR) if isinstance(T_LR, str) else T_LR

        self.parameters['模具名称'] = self.Chinese_name
        self.parameters['图号'] = 'DC0128-' + external_params['图号']
        self.machine_type = 'DC0128'
        # 计算成型芯轴直径D
        self.parameters['%%CD'] = str(D - 2 * max(Tx['T1'], Tx['T2'], Tx['T3']))

        # 计算成型芯轴总长LT
        total_length = Lx['L1'] + Lx['L2'] + Lx['L3'] + T_L + 320
        if total_length < 1060:
            self.parameters['LT'] = '1060'
        else:
            self.parameters['LT'] = '1140'  # 加连接杆长度

        self.parameters['件数'] = '1'  # 成型芯轴件数

        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())

        self.change = True