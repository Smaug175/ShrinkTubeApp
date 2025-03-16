from datetime import date
from bin.taper_bin.model.Taper_Base_Mold import BaseMoldClass
import numpy as np


class EC0120_B000(BaseMoldClass):
    def __init__(self,tp_length,line_data):
        """EC0120机器适用的taper模"""
        super().__init__()
        self.English_name = 'TaperMold'
        self.Chinese_name = 'Taper模两瓣'
        self.tp_length = tp_length
        self.line_data = line_data
        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):

        BL,D,TL,m_D,B_D = self._get_taper_params_from_tube(tube_df_params)

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]
        self.parameters['图号'] = external_params['图号']
        self.parameters['%%CD'] = str(D)
        self.parameters['L'] = str(TL+self.tp_length)
        self.parameters['%%CA'] = str(round(D+10*(D-m_D)/float(self.parameters['L']),ndigits=1))
        self.parameters['%%CB'] = str(m_D)

        if TL<=300:
            self.parameters['L_m'] = 400
        else:
            self.parameters['L_m'] = 480

        for index,row in self.line_data.iterrows():
            if abs(row[1]-float(self.parameters['%%CA']))<=0.1:
                left_index = index
                break

        np_line = np.array(self.line_data)
        sampled_data = np.linspace(left_index, len(np_line) - 1, 15, dtype=int)  # 生成均匀分布的索引
        #print(sampled_data)
        max_value = np.max(np_line[:, 0])
        line = []
        for i in range(len(sampled_data)):
            line.append(round(max_value-np_line[sampled_data[i]][0],ndigits=2))
        #print(line)
        self.parameters['line1'] = str(round(line[0],ndigits=2))+'/'+str(np_line[sampled_data[0]][1])
        self.parameters['line2'] = str(round(line[1],ndigits=2))+'/'+str(np_line[sampled_data[1]][1])
        self.parameters['line3'] = str(round(line[2],ndigits=2))+'/'+str(np_line[sampled_data[2]][1])
        self.parameters['line4'] = str(round(line[3],ndigits=2))+'/'+str(np_line[sampled_data[3]][1])
        self.parameters['line5'] = str(round(line[4],ndigits=2))+'/'+str(np_line[sampled_data[4]][1])
        self.parameters['line6'] = str(round(line[5],ndigits=2))+'/'+str(np_line[sampled_data[5]][1])
        self.parameters['line7'] = str(round(line[6],ndigits=2))+'/'+str(np_line[sampled_data[6]][1])
        self.parameters['line8'] = str(round(line[7],ndigits=2))+'/'+str(np_line[sampled_data[7]][1])
        self.parameters['line9'] = str(round(line[8],ndigits=2))+'/'+str(np_line[sampled_data[8]][1])
        self.parameters['line10'] = str(round(line[9],ndigits=2))+'/'+str(np_line[sampled_data[9]][1])
        self.parameters['line11'] = str(round(line[10],ndigits=2))+'/'+str(np_line[sampled_data[10]][1])
        self.parameters['line12'] = str(round(line[11],ndigits=2))+'/'+str(np_line[sampled_data[11]][1])
        self.parameters['line13'] = str(round(line[12],ndigits=2))+'/'+str(np_line[sampled_data[12]][1])
        self.parameters['line14'] = str(round(line[13],ndigits=2))+'/'+str(np_line[sampled_data[13]][1])
        self.parameters['line15'] = str(round(line[14],ndigits=2))+'/'+str(np_line[sampled_data[14]][1])

        self.parameters['件数'] = '1'
        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())
        self.change = True


class EC0121_B000(BaseMoldClass):
    def __init__(self,tp_length,line_data):
        """EC0120机器适用的taper模"""
        super().__init__()
        self.English_name = 'TaperMold'
        self.Chinese_name = 'Taper模四瓣'
        self.tp_length = tp_length
        self.line_data = line_data
        self.parameters = {}
        self.change = False

    def set_params(self, tube_df_params, external_params):

        BL,D,TL,m_D,B_D = self._get_taper_params_from_tube(tube_df_params)

        self.parameters['模具名称'] = self.Chinese_name
        self.machine_type = external_params['图号'].split('-')[0]
        self.parameters['图号'] = external_params['图号']
        self.parameters['%%CD'] = str(D)
        self.parameters['L'] = str(TL+self.tp_length)
        self.parameters['%%CA'] = str(round(D+10*(D-m_D)/float(self.parameters['L']),ndigits=1))
        self.parameters['%%CB'] = str(m_D)

        if TL<=400:
            self.parameters['L_m'] = 500
        else:
            self.parameters['L_m'] = 800


        for index,row in self.line_data.iterrows():
            if abs(row[1]-float(self.parameters['%%CA']))<=0.1:
                left_index = index
                break
        np_line = np.array(self.line_data)
        sampled_data = np.linspace(left_index, len(np_line) - 1, 15, dtype=int)  # 生成均匀分布的索引
        #print(sampled_data)
        max_value = np.max(np_line[:, 0])
        line = []
        for i in range(len(sampled_data)):
            line.append(round(max_value-np_line[sampled_data[i]][0],ndigits=2))
        #print(line)
        self.parameters['line1'] = str(round(line[0],ndigits=2))+'/'+str(np_line[sampled_data[0]][1])
        self.parameters['line2'] = str(round(line[1],ndigits=2))+'/'+str(np_line[sampled_data[1]][1])
        self.parameters['line3'] = str(round(line[2],ndigits=2))+'/'+str(np_line[sampled_data[2]][1])
        self.parameters['line4'] = str(round(line[3],ndigits=2))+'/'+str(np_line[sampled_data[3]][1])
        self.parameters['line5'] = str(round(line[4],ndigits=2))+'/'+str(np_line[sampled_data[4]][1])
        self.parameters['line6'] = str(round(line[5],ndigits=2))+'/'+str(np_line[sampled_data[5]][1])
        self.parameters['line7'] = str(round(line[6],ndigits=2))+'/'+str(np_line[sampled_data[6]][1])
        self.parameters['line8'] = str(round(line[7],ndigits=2))+'/'+str(np_line[sampled_data[7]][1])
        self.parameters['line9'] = str(round(line[8],ndigits=2))+'/'+str(np_line[sampled_data[8]][1])
        self.parameters['line10'] = str(round(line[9],ndigits=2))+'/'+str(np_line[sampled_data[9]][1])
        self.parameters['line11'] = str(round(line[10],ndigits=2))+'/'+str(np_line[sampled_data[10]][1])
        self.parameters['line12'] = str(round(line[11],ndigits=2))+'/'+str(np_line[sampled_data[11]][1])
        self.parameters['line13'] = str(round(line[12],ndigits=2))+'/'+str(np_line[sampled_data[12]][1])
        self.parameters['line14'] = str(round(line[13],ndigits=2))+'/'+str(np_line[sampled_data[13]][1])
        self.parameters['line15'] = str(round(line[14],ndigits=2))+'/'+str(np_line[sampled_data[14]][1])

        self.parameters['件数'] = '1'
        self.parameters['车种规格'] = external_params['车种规格']
        self.parameters['设计者'] = external_params['设计者']
        self.parameters['日期'] = str(date.today())
        self.change = True