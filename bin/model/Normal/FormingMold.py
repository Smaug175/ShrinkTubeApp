from datetime import date

from bin.model._BaseMold import BaseMoldClass


class DIEO(BaseMoldClass):
    def __init__(self, logger):
        """三个机器适用的成型模"""
        super().__init__()
        self.logger = logger
        self.English_name = 'FormingMold'
        self.Chinese_name = '成型模'

        self.parameters = {}

        self.change = False

        self.logger.info(self.Chinese_name+'初始化完成')

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            return

        self.parameters['模具名称'] = self.Chinese_name

        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        #成型模，不加0.03
        self.parameters['%%CD'] = str(round(D,2))

        self.parameters['%%Cd'] = str(round(D+5.55,2))

        self.parameters['%%Cd1'] = str(round(D+11.25,2))

        #材质对应表：
        D_d2 = {
            (12,15): 25,
            (15,20): 30,
            (20,25): 35,
            (25,30): 50,
            (30,38): 60,
            (38,45): 70,
            (45,52): 80,
            (52,60): 90,
            (60,69): 100,
            (69,75): 110,
            (75,85): 120,
            (85,95): 130,
            (95,105): 140,
            (105,115): 150,
        }
        for key in D_d2:
            if key[0] <= float(self.parameters['%%CD']) < key[1]:
                self.parameters['%%Cd2'] = D_d2[key]
                break

        #件数：1
        self.parameters['件数'] = external_params['件数']

        self.parameters['成品直径'] = '实抽' + str(D)

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True
        self.logger.info(self.Chinese_name+'参数设置成功')
