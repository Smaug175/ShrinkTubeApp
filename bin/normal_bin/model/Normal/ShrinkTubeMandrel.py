from datetime import date

from bin.normal_bin.model.Normal_Base_Mold import BaseMoldClass


class ADBT(BaseMoldClass):
    def __init__(self):
        """不同的机床共用的抽管芯轴"""
        super().__init__()
        self.English_name = 'ShrinkTubeMandrel'
        self.Chinese_name = '抽管芯轴'

        self.parameters = {}

        self.change = False

    def set_params(self, tube_df_params, external_params, Normal_Add):
        try:
            L, D, Lx, Mx, Tx = self._get_params_from_tube(tube_df_params)
        except:
            return
        self.parameters['模具名称'] = self.Chinese_name

        num_T = len(Tx)

        self.machine_type = external_params['图号'].split('-')[0]

        self.parameters['图号'] = external_params['图号']

        #d1:需要判断T的数量，来修改d
        T = []
        for x in range(len(Tx)):
            name = '%%Cd'+str(x+1)

            if Normal_Add:
                self.parameters[name] = round(D - 2 * Tx['T'+str(x+1)] + 0.3,1)
            else:
                self.parameters[name] = round(D - 2 * Tx['T'+str(x+1)],1)
            T.append(Tx['T'+str(x+1)])

        if num_T == 2:
            self.parameters['%%Cd3'] = '/'
            self.parameters['%%Cd4'] = '/'
            self.parameters['%%Cd5'] = '/'

            # M螺纹直径，由最大的d决定
            if self.parameters['%%Cd2'] < 36:
                self.parameters['M螺纹'] = 'M20'
            else:
                self.parameters['M螺纹'] = 'M36'

        elif num_T == 3:
            self.parameters['%%Cd4'] = '/'
            self.parameters['%%Cd5'] = '/'

            # M螺纹直径，由最大的d决定
            if self.parameters['%%Cd3'] < 36:
                self.parameters['M螺纹'] = 'M20'
            else:
                self.parameters['M螺纹'] = 'M36'

        # 初始化
        self.parameters['L1'] = '/'
        self.parameters['L2'] = '/'
        self.parameters['L3'] = '/'
        self.parameters['L4'] = '/'
        #Lx:需要判断Lx的数量，来修改L
        for x in range(len(Mx)):
            name_L = 'L'+str(2*x+1)
            self.parameters[name_L] = Lx['L'+str(x+1)]

            name_L = 'L'+str(2*x+2)
            self.parameters[name_L] = Mx['M'+str(x+1)]

        #C:C不知道是啥
        self.parameters['C'] = '/'

        #L5,(L6):不知道是啥
        self.parameters['L5'] = '/'
        self.parameters['(L6)'] = '/'

        # LT
        Sum_Lx = L #总长度
        # for key in Lx:
        #     Sum_Lx += Lx[key]

        min_L = 1060
        max_L = 1140

        if Sum_Lx + 320 < min_L:
            self.parameters['LT'] = str(min_L)
        else:
            self.parameters['LT'] = str(max_L)

        #缩管模直径:D+0.3
        if Normal_Add:
            self.parameters['缩管模直径'] = D + 0.3
        else:
            self.parameters['缩管模直径'] = D

        #抽管尺寸：%%CD-T1-T2-T3
        if Normal_Add:
            name = '%%C'+str(D+0.3)
            for i in T:
                name += '-'+str(i)
            self.parameters['抽管尺寸'] = name
        else:
            name = '%%C'+str(D)
            for i in T:
                name += '-'+str(i)
            self.parameters['抽管尺寸'] = name

        #件数：1
        self.parameters['件数'] = external_params['件数']

        # T , DC0124有，DC0121没有
        if D<=66:
            T = 0.75 * D
        else:
            T = 50

        self.parameters['T'] = int(T)

        #A,L 不知道是啥
        self.parameters['%%CA'] = '/'
        self.parameters['L'] = '/'

        #车种
        self.parameters['车种规格'] = external_params['车种规格']

        #设计者
        self.parameters['设计者'] = external_params['设计者']

        #Time
        self.parameters['日期'] = str(date.today())

        self.change = True
