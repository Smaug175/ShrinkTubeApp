from datetime import date
from bin.tp_bin.model.TP_Base_Mold import BaseMoldClass

class DC0128_AD04(BaseMoldClass):
    def __init__(self):
        """抽管退料模"""
        super().__init__()
        self.English_name = 'TPUnloadingMold'
        self.Chinese_name = '抽管退料模'

        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):
        L, D, Lx, Mx, Tx, T_D, T_L, T_LR = self._get_tp_params_from_tube(tube_df_params)

        # 无论参数提取是否成功，都设置基本参数
        self.parameters['模具名称'] = self.Chinese_name
        self.parameters['图号'] = 'DC0128-' + external_params['图号']
        self.machine_type = 'DC0128'

        # 只有在成功提取参数时才设置依赖于提取参数的值
        if T_D > 0:
            # 使用my_round函数对数值进行四舍五入
            self.parameters['A'] = str(T_D)  # 抽管退料模直径
        else:
            # 使用默认值或从外部参数中直接获取
            if 'T_D' in tube_df_params:
                self.parameters['A'] = str(float(tube_df_params['T_D']))
            else:
                self.parameters['A'] = '0'  # 默认值

        self.parameters['件数'] = '2'  # 抽管退料模件数
        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())

        self.change = True
