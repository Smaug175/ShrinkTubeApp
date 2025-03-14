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

    def _find_value_base_point2(self, texts, insert, value) -> bool:
        """根据插入点找到对应的值,并修改"""
        for text in texts:
            if (int(insert[0]) - 5 <= int(text.dxf.insert[0]) <= int(insert[0]) + 5) and (
                    int(insert[1]) - 5 <= int(text.dxf.insert[1]) <= int(insert[1]) + 5):
                text.dxf.text = value
                return True

        return False

    def _get_params_from_tube(self, params) -> tuple:
        """从管件参数中提取参数
        自身调用"""

        params = params.to_dict(orient='list')

        params = dict(zip(params['Parameter'], params['Value']))

        D = params['D']

        Tx = {}
        for item in params:
            if item.startswith('T'):
                Tx[item] = params[item]

        L = params['L']

        Mx = {}
        for item in params:
            if item.startswith('M'):
                Mx[item] = params[item]

        Lx = {}
        for item in params:
            if item.startswith('L') and item != 'L' and item != 'D':
                Lx[item] = params[item]

        return L, D, Lx, Mx, Tx

    def modify_dxf(self):
        """将参数修改到DXF文件中"""

        if self.machine_type == 'DC0124':
            # 从图号中获取小图号
            path_dxf = self.parameters['图号'].split('-')[1][:-4]
            if path_dxf == 'SS01' or path_dxf == 'ADBT': # 成型芯轴和抽管芯轴，螺纹不同，输出的图纸也不一样
                if self.parameters['M螺纹'] == 'M20':
                    path_dxf = path_dxf + '_M20'
                elif self.parameters['M螺纹'] == 'M36':
                    path_dxf = path_dxf + '_M36'
            self.file_name = 'bin/normal_bin/StandardDXF/Normal/DC0124/' + path_dxf + '.dxf'
        elif self.machine_type == 'DC0121':
            path_dxf = self.parameters['图号'].split('-')[1][:-4]
            if path_dxf == 'SS01' or path_dxf == 'ADBT':
                if self.parameters['M螺纹'] == 'M20':
                    path_dxf = path_dxf + '_M20'
                elif self.parameters['M螺纹'] == 'M36':
                    path_dxf = path_dxf + '_M36'
            self.file_name = 'bin/normal_bin/StandardDXF/Normal/DC0121/' + path_dxf + '.dxf'
        elif self.machine_type == 'DC0125':
            path_dxf = self.parameters['图号'].split('-')[1][:-4]
            if path_dxf == 'SS01' or path_dxf == 'ADBT':
                if self.parameters['M螺纹'] == 'M20':
                    path_dxf = path_dxf + '_M20'
                elif self.parameters['M螺纹'] == 'M36':
                    path_dxf = path_dxf + '_M36'
            self.file_name = 'bin/normal_bin/StandardDXF/Normal/DC0125/' + path_dxf + '.dxf'

        # print(self.file_name)

        try:
            self.doc = ezdxf.readfile(self.file_name)
        except IOError:
            self.doc = None

        # 图纸中，参数之间的高度距离
        Height = 18

        if self.change:
            # 根据self的参数修改文件中的参数，获取模型空间中的所有 TEXT 实体
            texts = self.doc.modelspace().query("TEXT")
            for text in texts:
                if text.dxf.text in self.parameters:
                    # print(text.dxf.text)
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
                        print(self.Chinese_name+' 的参数没有修改，',f"没有找到对应的值：{text.dxf.text}")
                        # DC0121 找到两个A值，并对应了已经修改过的参数
                        continue
        else:
            print(self.Chinese_name+'的参数没有修改，不进行修改标准DXF文件')

    def get_params(self):
        """获取模具的参数,返回一个DataFrame对象"""

        if self.change:
            Params = []
            for key in self.parameters:
                Params.append([key, self.parameters[key]])
            pd_params = pd.DataFrame(Params, columns=['Parameter', 'Value'])
            return pd_params
        else:
            return None

    def save_dxf(self, output_path, output_name):
        """保存文件到指定路径,返回保存的路径"""
        if self.change:
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            today = date.today()
            save_path = output_path + '/'+ output_name + ".dxf" #str(today) + " " + ".dxf"
            self.doc.saveas(save_path)

            # print("已保存至:", save_path)

            return save_path
        else:
            # print(self.Chinese_name+'的参数没有修改，不进行保存DXF文件')
            return None

    def _modify_parameters(self, key, value):
        """修改参数"""
        self.parameters[key] = value