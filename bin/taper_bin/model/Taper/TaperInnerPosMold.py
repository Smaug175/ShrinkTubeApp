from datetime import date
from bin.taper_bin.model.Taper_Base_Mold import BaseMoldClass


class I000(BaseMoldClass):
    def __init__(self):
        """EC0120机器适用"""
        super().__init__()
        self.English_name = 'TaperInnerPosMold'
        self.Chinese_name = '内定位模'
        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):

        BL,D,TL,m_D,B_D = self._get_taper_params_from_tube(tube_df_params)

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]
        self.parameters['图号'] = external_params['图号']
        self.parameters['B'] = str(D)

        self.parameters['件数'] = '1'
        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())
        self.change = True


