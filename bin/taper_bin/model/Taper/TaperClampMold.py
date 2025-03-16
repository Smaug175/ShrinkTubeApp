from datetime import date
from bin.taper_bin.model.Taper_Base_Mold import BaseMoldClass


class J000(BaseMoldClass):
    def __init__(self,machine_type):
        """夹模"""
        super().__init__()
        self.English_name = 'TaperClampMold'
        self.Chinese_name = '夹模'
        self.parameters = {}
        self.change = False
        self.machine_type = machine_type


    def set_params(self, tube_df_params, external_params):
        BL,D,TL,m_D,B_D = self._get_taper_params_from_tube(tube_df_params)

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]
        self.parameters['图号'] = external_params['图号']
        self.parameters['A'] = str(B_D)
        if self.machine_type == 'EC0120':
            self.parameters['件数'] = '1'
        else:
            self.parameters['件数'] = '2'
        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())
        self.change = True


