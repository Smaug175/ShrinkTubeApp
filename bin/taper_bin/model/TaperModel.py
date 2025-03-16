import numpy as np
import ezdxf
import pandas as pd


def my_round(number: float, ndigits: int) -> float:
    """保留小数点后的位数
    在图中，可能有些四舍五入的情况，所以需要递归调用
    """
    if ndigits == 1:
        return round(number, 1)
    else:
        number = round(number, ndigits)
        return my_round(number, ndigits - 1)


class TaperModelClass():
    """该类用于读取DXF文件中的Taper管件参数，并检查参数是否符合规则
    """

    def __init__(self, file_name: str):
        """初始化类，读取DXF文件中的Taper参数"""
        self.file_name = file_name  # 添加文件名属性
        try:
            self.doc = ezdxf.readfile(file_name)
        except IOError:
            self.doc = None
            print('文件导入失败!报错位置：TaperModel.__init__')
            return

        # 1.查找车种规格
        # 识别定义的参数,类型为：TEXT 查找车种规格
        text = self.doc.modelspace().query("TEXT")
        for t in text:
            text_value = t.dxf.text
            #print("TEXT",text_value)
            if '车种规格=' in text_value:
                self.vehicle_type_specification = text_value.split('=')[1]
                #print(self.vehicle_type_specification)

        # 识别定义的参数,类型为：MTEXT
        text = self.doc.modelspace().query("MTEXT")
        for t in text:
            text_value = t.dxf.text
            #print("MTEXT",text_value)
            if '车种规格' in text_value:
                index_1 = text_value.index('=')
                index_2 = text_value.index('}')
                if index_1 < index_2:
                    if index_1 + 1 == index_2:
                        self.vehicle_type_specification = text_value.split('}')[1]
                    else:
                        first_part = text_value.split('=')[1]
                        self.vehicle_type_specification = first_part.split('}')[0]
                else:
                    self.vehicle_type_specification = text_value.split('=')[1]


        params = {}
        params['车种规格'] = self.vehicle_type_specification

        # 获取模型空间中的所有 DIMENSION 实体
        dimensions = self.doc.modelspace().query("DIMENSION")
        # 遍历所有 DIMENSION 实体并打印参数
        for dim in dimensions:
            name = ''
            value = ''
            if '=' in dim.dxf.text:
                name = dim.dxf.text.split('=')[0]
                value = dim.dxf.text.split('=')[1]
                if '%%C' in value:
                    # print(name,' 是直径。')
                    value = value.replace('%%C', '')

            try:
                params[name] = float(value) # 不使用标注值，只使用写上去的值
            except ValueError:
                pass


        # 将参数按照字母顺序排列
        self.params = dict(sorted(params.items()))

        Parameter = []
        Value = []
        for key, value in self.params.items():
            Parameter.append(key)
            Value.append(value)
        df_params = {'参数': Parameter, '值': Value}
        print(df_params)

        self.df_params = pd.DataFrame(df_params, columns=['参数', '值'])


    def get_params(self,) -> pd.DataFrame:
        return self.df_params

    def get_taper_params_df(self):
        """返回管件的参数，DataFrame格式（TP抽专用，列名为'参数'/'值'/'描述'）"""
        rows = []
        # 数值类型参数（需要四舍五入）
        numeric_params = ['BL','D','TL','m_D','B_D']

        # 处理主要参数
        for key in ['BL','D','TL','m_D','B_D']:
            if key in self.params:
                # 对数值参数进行四舍五入
                if isinstance(self.params[key], (int, float)):
                    # 对于接近整数的值，四舍五入到整数；否则保留2位小数
                    value = round(self.params[key]) if abs(
                        self.params[key] - round(self.params[key])) < 0.01 else round(self.params[key], 2)
                else:
                    value = self.params[key]
                rows.append([key, value, self._get_description(key)])


        # 添加其他非数值参数
        for key in ['车种规格', '图号', '管件名称', '设计者', '日期', '件数']:
            if key in self.params:
                rows.append([key, self.params[key], key])

        # 使用列名格式：'参数'/'值'/'描述'
        df = pd.DataFrame(rows, columns=['参数', '值', '描述'])
        return df

    def _get_description(self, param):
        """返回参数的描述"""
        descriptions = {
            'BL': 'TAPER前管长',
            'D': 'TAPER最大直径',
            'TL': '打TAPER操作长度',
            'm_D': 'TAPER模型腔的最小直径',
            'B_D': '打taper前管直径'
        }
        return descriptions.get(param, '参数描述')



    def set_params(self, params: dict):
        """从参数字典中提取出各个参数"""

        try:
            BL = params.get('BL')
            D = params.get('D')
            TL = params.get('TL')
            m_D = params.get('m_D')
            B_D = params.get('B_D')

            return BL, D, TL, m_D, B_D
        except KeyError as e:
            return None





