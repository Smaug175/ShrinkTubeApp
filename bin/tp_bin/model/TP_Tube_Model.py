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


class TubeModelClass():
    """该类用于读取DXF文件中的管件参数，并检查参数是否符合规则"""

    def __init__(self, file_name: str):
        """初始化类，读取DXF文件中的参数，并检查参数是否符合规则"""
        # 读取DXF文件
        self.file_name = file_name

        try:
            self.doc = ezdxf.readfile(self.file_name)
        except IOError:
            temp_str = '文件导入失败!报错位置：TubeModelClass.__init__'
            print(temp_str)
            self.doc = None

        # 1.查找车种规格
        # 识别定义的参数,类型为：TEXT 查找车种规格
        text = self.doc.modelspace().query("TEXT")
        for t in text:
            text_value = t.dxf.text
            # print("TEXT",text_value)
            if '车种规格=' in text_value:
                self.vehicle_type_specification = text_value.split('=')[1]
        # 查找车种规格
        # 识别定义的参数,类型为：MTEXT
        text = self.doc.modelspace().query("MTEXT")
        for t in text:
            text_value = t.dxf.text
            # print("MTEXT",text_value)
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
        
        # 2.存储参数
        params = {}
        params['车种规格'] = self.vehicle_type_specification

        # 查找参数
        # 获取模型空间中的所有 DIMENSION 实体
        dimensions = self.doc.modelspace().query("DIMENSION")

        # 遍历所有 DIMENSION 实体并打印参数
        for dim in dimensions:
            # 占位用的，不起作用
            name = ''
            value = ''
            # print(dim.dxf.text)
            if '=' in dim.dxf.text:
                name = dim.dxf.text.split('=')[0]
                value = dim.dxf.text.split('=')[1]
                if '%%C' in value:
                    # print(name,' 是直径。')
                    value = value.replace('%%C', '')

            # print(name,value)
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

        self.df_params = pd.DataFrame(df_params, columns=['参数', '值'])
        # print(df_params)

    def get_params(self,) -> pd.DataFrame:
        return self.df_params

    def get_tp_params_df(self):
        """返回管件的参数，DataFrame格式（TP抽专用，列名为'参数'/'值'/'描述'）"""
        rows = []
        # 数值类型参数（需要四舍五入）
        numeric_params = ['D', 'L', 'T_L', 'T_D', 'T_LR', 'L1', 'L2', 'L3', 'T1', 'T2', 'T3', 'M1', 'M2']

        # 处理主要参数
        for key in ['D', 'L', 'T_L', 'T_D', 'T_LR']:
            if key in self.params:
                # 对数值参数进行四舍五入
                if isinstance(self.params[key], (int, float)):
                    # 对于接近整数的值，四舍五入到整数；否则保留2位小数
                    value = round(self.params[key]) if abs(
                        self.params[key] - round(self.params[key])) < 0.01 else round(self.params[key], 2)
                else:
                    value = self.params[key]
                rows.append([key, value, self._get_description(key)])

        # 添加其他Lx, Tx, Mx参数
        for i in range(1, 4):  # 假设最多3组
            l_key = f'L{i}'
            t_key = f'T{i}'
            m_key = f'M{i}'

            if l_key in self.params:
                # 对数值参数进行四舍五入
                if isinstance(self.params[l_key], (int, float)):
                    value = round(self.params[l_key]) if abs(
                        self.params[l_key] - round(self.params[l_key])) < 0.01 else round(self.params[l_key], 2)
                else:
                    value = self.params[l_key]
                rows.append([l_key, value, self._get_description(l_key)])

            if t_key in self.params:
                # 对数值参数进行四舍五入
                if isinstance(self.params[t_key], (int, float)):
                    value = round(self.params[t_key]) if abs(
                        self.params[t_key] - round(self.params[t_key])) < 0.01 else round(self.params[t_key], 2)
                else:
                    value = self.params[t_key]
                rows.append([t_key, value, self._get_description(t_key)])

            if m_key in self.params:
                # 对数值参数进行四舍五入
                if isinstance(self.params[m_key], (int, float)):
                    value = round(self.params[m_key]) if abs(
                        self.params[m_key] - round(self.params[m_key])) < 0.01 else round(self.params[m_key], 2)
                else:
                    value = self.params[m_key]
                rows.append([m_key, value, self._get_description(m_key)])

        # 添加其他非数值参数
        for key in ['车种规格', '图号', '管件名称', '设计者', '日期', '件数']:
            if key in self.params:
                rows.append([key, self.params[key], key])

        # 使用TP抽的列名格式：'参数'/'值'/'描述'
        df = pd.DataFrame(rows, columns=['参数', '值', '描述'])
        return df

    def _get_description(self, param):
        """返回参数的描述"""
        descriptions = {
            'D': '普通抽直径',
            'L': '抽管总长',
            'T_D': 'TP抽最大直径',
            'T_L': 'TP抽长度',
            'T_LR': '抽管留存长度',
            'L1': '普通抽第一段长度',
            'T1': '普通抽第一段壁厚',
            'M1': '普通抽第一过渡段长',
            'L2': '普通抽第二段长度',
            'T2': '普通抽第二段壁厚',
            'M2': '普通抽第二过渡段长',
            'L3': '普通抽第三段长度',
            'T3': '普通抽第三段壁厚'
        }
        return descriptions.get(param, '参数描述')

    def set_params(self, params):
        """从参数字典中提取出各个参数"""
        try:
            L = params['L']
            D = params['D']
            Lx = {item: params[item] for item in params if item.startswith('L') and item != 'L' and item != 'D'}
            Mx = {item: params[item] for item in params if item.startswith('M')}
            Tx = {item: params[item] for item in params if item.startswith('T') and item not in {'T_D', 'T_L', 'T_LR'}}
            T_D = params.get('T_D')
            T_L = params.get('T_L')
            T_LR = params.get('T_LR')

            return L, D, Lx, Mx, Tx, T_D, T_L, T_LR
        except KeyError as e:
            return None

if __name__ == '__main__':
    tmc = TubeModelClass('D:/GIANT/0阶段性开发/example/tp/TCR-TT-1122-4_standard.dxf')