import os
import ezdxf
import pandas as pd
from datetime import date


class BaseMoldClass:
    """模具基类

    Methods
    _______
    modify_dxf(self)
        将参数修改到DXF文件中
    get_params(self)
        获取模具的参数,返回一个DataFrame对象
    save_dxf(self, output_path, output_name)
        保存文件到指定路径,返回保存的路径
    """
    def __init__(self,):
        """初始化模具基类"""
        pass

    def _find_value_base_point1(self, texts, insert):
        """根据插入点找到对应的值"""

        for text in texts:
            if (int(insert[0]) - 5 <= int(text.dxf.insert[0]) <= int(insert[0]) + 5) and (
                    int(insert[1]) - 5 <= int(text.dxf.insert[1]) <= int(insert[1]) + 5):
                return text.dxf.text

        return None

    def _init_params(self):
        """初始化参数"""

        # 获取模型空间中的所有 TEXT 实体
        texts = self.doc.modelspace().query("TEXT")
        for text in texts:
            if text.dxf.text in self.parameters:
                insert_point = (text.dxf.insert[0], text.dxf.insert[1] + self.Height, 0)
                value = self._find_value_base_point1(texts, insert_point)
                if value is None:
                    # print(insert_point)
                    print(f"参数：{text.dxf.text}, 位置：{text.dxf.insert}，未找到对应的值！")
                self.parameters[text.dxf.text] = value

    def _get_tp_params_from_tube(self, pd_params) -> tuple:
        """从管件参数中提取参数"""
        params = pd_params.to_dict(orient='list')
        params_dict = dict(zip(params['参数'], params['值']))

        # 确保参数存在并尝试转换为浮点数
        D = float(params_dict.get('D', 0))
        L = float(params_dict.get('L', 0))

        # 提取并转换其他参数
        Tx = {}
        Lx = {}
        Mx = {}
        
        # 获取T_D, T_L, T_LR
        try:
            T_D = float(params_dict.get('T_D', 0))
        except (ValueError, TypeError):
            print(f"警告: 无法将T_D转换为浮点数: {params_dict.get('T_D')}")
            T_D = 0
            
        try:
            T_L = float(params_dict.get('T_L', 0))
        except (ValueError, TypeError):
            print(f"警告: 无法将T_L转换为浮点数: {params_dict.get('T_L')}")
            T_L = 0
            
        try:
            T_LR = float(params_dict.get('T_LR', 0))
        except (ValueError, TypeError):
            print(f"警告: 无法将T_LR转换为浮点数: {params_dict.get('T_LR')}")
            T_LR = 0

        # 获取所有T参数
        for item in params_dict:
            if item.startswith('T') and item not in ['T_D', 'T_L', 'T_LR']:
                try:
                    Tx[item] = float(params_dict[item])
                except (ValueError, TypeError):
                    print(f"警告: 无法将{item}转换为浮点数: {params_dict[item]}")
                    Tx[item] = 0
        
        # 获取所有L参数
        for item in params_dict:
            if item.startswith('L') and item not in ['L']:
                try:
                    Lx[item] = float(params_dict[item])
                except (ValueError, TypeError):
                    print(f"警告: 无法将{item}转换为浮点数: {params_dict[item]}")
                    Lx[item] = 0
                    
        # 获取所有M参数
        for item in params_dict:
            if item.startswith('M'):
                try:
                    Mx[item] = float(params_dict[item])
                except (ValueError, TypeError):
                    print(f"警告: 无法将{item}转换为浮点数: {params_dict[item]}")
                    Mx[item] = 0

        return L, D, Lx, Mx, Tx, T_D, T_L, T_LR

    def _find_value_base_point2(self, texts, insert, value) -> bool:
        """根据插入点找到对应的值,并修改"""

        for text in texts:
            if (int(insert[0]) - 5 <= int(text.dxf.insert[0]) <= int(insert[0]) + 5) and (
                    int(insert[1]) - 5 <= int(text.dxf.insert[1]) <= int(insert[1]) + 5):
                text.dxf.text = value
                return True

        return False

    def modify_dxf(self):
        """将参数修改到DXF文件中"""
        # 从图号中获取小图号
        path_dxf = self.parameters['图号'].split('-')[1][:-4]

        self.file_name = 'bin/tp_bin/StandardDXF/TP/DC0128/' + path_dxf + '.dxf'

        try:
            self.doc = ezdxf.readfile(self.file_name)
        except IOError:
            self.doc = None
            print(f"无法读取文件 {self.file_name}")

        # 图纸中，参数之间的高度距离
        Height = 18

        if self.change:
            # 根据self的参数修改文件中的参数，获取模型空间中的所有 TEXT 实体
            texts = self.doc.modelspace().query("TEXT")
            for text in texts:
                if text.dxf.text in self.parameters:
                    insert_point = (text.dxf.insert[0], text.dxf.insert[1] + Height, 0)

                    value = self.parameters[text.dxf.text]
                    if text.dxf.text == '图号':
                        # 图号去掉机器类型
                        value = value.split('-')[1]
                        if len(value) > 8:
                            value = value[:4] + value[-4:]

                    index = self._find_value_base_point2(texts, insert_point, value)

                    if index:
                        continue
                    else:
                        print(f"没有找到对应的值：{text.dxf.text}")
                        continue
            # print(self.Chinese_name+'的参数修改，修改标准DXF文件')
        else:
            print(self.Chinese_name+'的参数没有修改，不进行修改标准DXF文件')

    def get_params(self):
        """获取模具的参数,返回一个DataFrame对象
        列名为'Parameter'和'Value'"""
        if self.change:
            Params = []
            for key in self.parameters:
                Params.append([key, self.parameters[key]])
            pd_params = pd.DataFrame(Params, columns=['参数', '值'])
            return pd_params
        else:
            return None

    def save_dxf(self, output_path, output_name):
        """保存文件到指定路径,返回保存的路径"""
        if self.change:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            # today = date.today()
            save_path = output_path + '/'+ output_name + ".dxf" #str(today) + " " + ".dxf"
            self.doc.saveas(save_path)
            print("已保存至:", save_path)
            return save_path
        else:
            print(self.Chinese_name+'的参数没有修改，不进行保存DXF文件')
            return None

    def _modify_parameters(self, key, value):
        """修改参数"""
        self.parameters[key] = value