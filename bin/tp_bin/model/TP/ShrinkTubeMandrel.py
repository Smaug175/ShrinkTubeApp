import sys
import os

from datetime import date
from bin.tp_bin.model.TP_Base_Mold import BaseMoldClass

class DC0128_ADBT(BaseMoldClass):
    def __init__(self, interference_length):
        """抽管芯轴"""
        super().__init__()
        self.English_name = 'TPShrinkTubeMandrel'
        self.Chinese_name = '抽管芯轴'

        self.interference_length=interference_length
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

        # 计算参数
        self.parameters['L1'] = str(Lx['L1'] + 5)  # 抽管芯轴第一段长度
        self.parameters['M1'] = str(Mx['M1'])  # 抽管芯轴第一过渡段长度
        self.parameters['L2'] = str(Lx['L2'])  # 抽管芯轴第二段长度
        self.parameters['M2'] = str(Mx['M2'])  # 抽管芯轴第二过渡段长度
        self.parameters['L3'] = str(Lx['L3'])  # 抽管芯轴第三段长度
        self.parameters['IL'] = str(self.interference_length)  # 抽管芯轴第干涉段长度
        self.parameters['L4'] = str(T_L)  # 抽管芯轴第四段长度

        self.parameters['%%Cd1'] = str(D - 2 * Tx['T1'])  # 抽管芯轴第一段直径
        self.parameters['%%Cd2'] = str(D - 2 * Tx['T2'])  # 抽管芯轴第二段直径
        self.parameters['%%Cd3'] = str(D - 2 * Tx['T3'])  # 抽管芯轴第三段直径
        self.parameters['%%Cd4'] = str(D - 2 * Tx['T3'] - 0.5)  # 抽管芯轴尾段直径

        # 计算外螺纹直径M
        d4 = float(self.parameters['%%Cd4'])
        if d4 > 36:
            self.parameters['M'] = '36'
        else:
            self.parameters['M'] = '20'

        # 计算总长LT
        total_length = float(self.parameters['L1']) + float(self.parameters['L2']) + float(self.parameters['L3']) + float(self.parameters['L4'])
        if total_length + 320 < 1060:
            self.parameters['LT'] = '1060'
        else:
            self.parameters['LT'] = '1140'

        self.parameters['件数'] = '1'  # 抽管芯轴件数
        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())

        self.change = True
