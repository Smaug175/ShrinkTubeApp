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
    """该类用于读取DXF文件中的管件参数，并检查参数是否符合规则

    Methods
    _______
    set_params(params: dict) -> tuple
        从参数字典中提取出各个参数
    check_params() -> tuple
        检查参数是否符合规则
    get_params() -> pd.DataFrame
        输出参数，pandas的DataFrame格式
    __len__() -> int
        返回一共有多少段壁厚
    __str__() -> str
        返回文件名
    get_Diameter() -> float
        返回管件的直径
    get_All_Length() -> float
        返回管件的总长度
    get_Section_lengths_and_Wall_Thicknesses(number:int) -> tuple
        返回选定壁厚的长度和壁厚
    get_node() -> list
        返回每个节点的坐标
    """

    def __init__(self, file_name: str, logger):
        """初始化类，读取DXF文件中的参数，并检查参数是否符合规则"""

        self.logger = logger

        # 读取DXF文件
        self.file_name = file_name

        try:
            self.doc = ezdxf.readfile(self.file_name)
            self.logger.info(self.file_name + ': 文件导入成功')
        except IOError:
            temp_str = '文件导入失败!报错位置：TubeModelClass.__init__'
            print(temp_str)

            self.doc = None
            self.logger.error(self.file_name + '文件导入失败!' + '不是 DXF 文件，也不是一般的 I/O 错误。')

        # 识别定义的参数,类型为：TEXT
        text = self.doc.modelspace().query("TEXT")
        for t in text:
            text_value = t.dxf.text
            # print("TEXT",text_value)
            if '车种规格=' in text_value:
                self.vehicle_type_specification = text_value.split('=')[1]

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
        
        # 存储参数
        params = {}

        # 获取模型空间中的所有 DIMENSION 实体
        dimensions = self.doc.modelspace().query("DIMENSION")

        # 遍历所有 DIMENSION 实体并打印参数
        for dim in dimensions:
            name = ''
            value = ''
            for i in range(len(dim.dxf.text)):
                if dim.dxf.text[i] == '=':
                    # print(dim.dxf.text)
                    if name == 'D':
                        if dim.dxf.text[-1] == '}':
                            value = dim.dxf.text[i + 4:][:-1] #这里是为了去掉最后的}后缀
                        else:
                            value = dim.dxf.text[i + 4:] #这里是为了去掉D=的前缀
                    else:
                        if dim.dxf.text[-1] == '}':
                            value = dim.dxf.text[i + 1:][:-1]
                        else:
                            value = dim.dxf.text[i+1:]
                    break
                else:
                    name += dim.dxf.text[i]

            # 去除name中的非必要字符
            if ';' in name:
                name = name.split(';')[1]

            # print(name, value)
            # if float(value) == my_round(float(dim.get_measurement()), 4):
            #     # 将参数保留四位小数，这是储存标注的方式,dim.get_measurement()是获取标注的值
            #     params[name] = my_round(float(dim.get_measurement()), 4)
            # else:
            #     # 当无法使用get_measurement()时，需要考虑使用写上去的值
            #     params[name] = float(value)

            try:
                params[name] = float(value) # 不使用标注值，只使用写上去的值
            except:
                pass

        # 将参数按照字母顺序排列
        self.sorted_params = dict(sorted(params.items()))

        self.logger.info('参数读取成功')

        # 从参数字典中提取出各个参数
        self.L, self.D, self.Lx, self.Mx, self.Tx = self.set_params(params)

        # 检查参数是否符合规则
        self.belta_rad, self.L_LT_RT= self.check_params()

        self.logger.info('参数规则检查成功')

    def set_params(self, params: dict):
        """从参数字典中提取出各个参数"""

        try:
            D = params['D']
        except:
            print('缺少直径参数')
            print('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.logger.error('缺少直径参数')
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.error = ['ERROR IN SET PARAMS', '缺少直径参数']
            return None

        try:
            Tx={}
            for item in params:
                if item.startswith('T'):
                    Tx[item] = params[item]
        except:
            print('缺少T(壁厚)参数')
            print('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.logger.error('缺少T(壁厚)参数')
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.error = ['ERROR IN SET PARAMS', '缺少T(壁厚)参数']
            return None

        try:
            L = params['L']
        except:
            print('缺少L(总长度)参数')
            print('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.logger.error('缺少L(总长度)参数')
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.error = ['ERROR IN SET PARAMS', '缺少L(总长度)参数']
            return None

        try:
            Mx ={}
            for item in params:
                if item.startswith('M'):
                    Mx[item] = params[item]
        except:
            print('缺少M(过渡段)参数')
            print('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.logger.error('缺少M(过渡段)参数')
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.error = ['ERROR IN SET PARAMS', '缺少M(过渡段)参数']
            return None

        try:
            Lx = {}
            for item in params:
                if item.startswith('L') and item != 'L' and item != 'D':
                    Lx[item] = params[item]
        except:
            print('缺少Lx(壁厚段)参数')
            print('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.logger.error('缺少Lx(壁厚段)参数')
            self.logger.error('ERROR IN SET PARAMS: 请检查参数是否正确')
            self.error = ['ERROR IN SET PARAMS', '缺少Lx(壁厚段)参数']
            return None
        
        # print('参数提取成功')
        self.logger.info('参数提取成功')

        return L, D, Lx, Mx, Tx
    
    def check_params(self,):
        """检查参数是否符合规则"""

        # 1.检查L值是否是各个Lx与Mx之和
        try:
            assert self.L == sum(self.Mx.values()) + sum(self.Lx.values())
        except:
            print('ERROR IN CHECK PARAMS: L值不等于各个Mx与Lx之和')
            self.logger.error('ERROR IN CHECK PARAMS: L值不等于各个Mx与Lx之和')
            self.error = ['ERROR IN CHECK PARAMS', 'L值不等于各个Mx与Lx之和']
            return None

        # 2.检查Lx, Mx, Tx的命名是否符合规则
        try:
            for i in range(len(self.Lx)):
                assert 'L'+str(i+1) in self.Lx.keys()
        except:
            print('ERROR IN CHECK PARAMS: Lx的命名不符合规则')
            self.logger.error('ERROR IN CHECK PARAMS: Lx的命名不符合规则')
            self.error = ['ERROR IN CHECK PARAMS', 'Lx的命名不符合规则']
            return None

        try:
            for i in range(len(self.Mx)):
                assert 'M'+str(i+1) in self.Mx.keys()
        except:
            print('ERROR IN CHECK PARAMS: Mx的命名不符合规则')
            self.logger.error('ERROR IN CHECK PARAMS: Mx的命名不符合规则')
            self.error = ['ERROR IN CHECK PARAMS', 'Mx的命名不符合规则']
            return None

        try:
            for i in range(len(self.Tx)):
                assert 'T'+str(i+1) in self.Tx.keys()
        except:
            print('ERROR IN CHECK PARAMS: Tx的命名不符合规则')
            self.logger.error('ERROR IN CHECK PARAMS: Tx的命名不符合规则')
            self.error = ['ERROR IN CHECK PARAMS', 'Tx的命名不符合规则']
            return None

        # 3.检查Lx, Mx, Tx的数量是否符合规则
        try:
            assert len(self.Lx) == len(self.Mx) + 1 == len(self.Tx)
        except:
            print('ERROR IN CHECK PARAMS: Lx, Mx, Tx的数量不符合规则')
            self.logger.error('ERROR IN CHECK PARAMS: Lx, Mx, Tx的数量不符合规则')
            self.error = ['ERROR IN CHECK PARAMS', 'Lx, Mx, Tx的数量不符合规则']
            return None

        # 4.检查过渡段的倾角是否符合规则
        belta_rad = {}
        for i in range(len(self.Mx)):
            try:
                I = i+1
                T1 = self.Tx['T'+str(I)]
                T2 = self.Tx['T'+str(I+1)]
                M = self.Mx['M'+str(I)]
                
                belta_rad['Belta'+str(I)] = np.arctan(abs(T2-T1)/M)
            except:
                print('ERROR IN CHECK PARAMS: 第',i+1,'个过渡段的倾角不符合规则')
                self.logger.error('ERROR IN CHECK PARAMS: 第'+str(i+1)+'个过渡段的倾角不符合规则')
                self.error = ['ERROR IN CHECK PARAMS', '第'+str(i+1)+'个过渡段的倾角不符合规则']
                return None

        # 5.标准化每一段
        L_LT_RT = []
        for i in range(len(self.Lx)):
            L_LT_RT.append((self.Lx['L'+str(i+1)], self.Tx['T'+str(i+1)], self.Tx['T'+str(i+1)]))
            try:
                L_LT_RT.append((self.Mx['M'+str(i+1)], self.Tx['T'+str(i+1)], self.Tx['T'+str(i+2)]))
            except:
                pass

        # print('参数检查成功')
        self.logger.info('参数检查成功')

        return belta_rad, L_LT_RT

    def get_params(self,) -> pd.DataFrame:
        """输出参数，pandas的DataFrame格式"""

        Params = [['车种规格', self.vehicle_type_specification],['D',self.D],['L',self.L]]
        for i in range(len(self.Lx)):
            Params.append(['L'+str(i+1),self.Lx['L'+str(i+1)]])
            Params.append(['T'+str(i+1),self.Tx['T'+str(i+1)]])
            try:
                Params.append(['M'+str(i+1),self.Mx['M'+str(i+1)]])
                Params.append(['Belta'+str(i+1)+' (radians)',self.belta_rad['Belta'+str(i+1)]])
            except:
                temp_str = '第'+str(i+1)+'个过渡段'+': 不存在'+'，报错位置：\nTubeModelClass.get_params()'
                print(temp_str)
                self.logger.warning(temp_str)

        # 将参数列表转换为DataFrame
        df_params = pd.DataFrame(Params, columns=['Parameter', 'Value'])

        self.logger.info('参数输出成功')

        return df_params

    def __len__(self) -> int:
        """返回一共有多少段壁厚"""
        return int(2*len(self.Lx)-1)
    
    def __str__(self) -> str:
        """返回文件名"""
        return self.file_name[:-4]
    
    def get_Diameter(self) -> float:
        """返回管件的直径"""
        return self.D
    
    def get_All_Length(self) -> float:
        """返回管件的总长度"""
        return self.L
    
    def get_Section_lengths_and_Wall_Thicknesses(self,number:int) -> tuple:
        """返回选定壁厚的长度和壁厚"""
        return self.L_LT_RT[number]
    
    def get_node(self) -> list:
        """返回每个节点的坐标"""

        # TODO: 未完成
        #先实现一个简单的，后续再改
        #假设LD=RD
        #将左下角作为模型的原点，最终输出每个节点的坐标
        NODE = []
        node = []
        D = self.D
        T = self.get_Section_lengths_and_Wall_Thicknesses(0)[1]
        
        #原零点上的四个点
        node.append([0,0])
        node.append([0,T])
        node.append([0,D-T])
        node.append([0,D])
        
        NODE.append(node)
        
        for i in range(2*len(self.Lx)-1):
            node = []
            L = self.get_Section_lengths_and_Wall_Thicknesses(i)[0]
            T = self.get_Section_lengths_and_Wall_Thicknesses(i)[2]
            
            node.append([NODE[-1][0][0]+L,0])
            node.append([NODE[-1][0][0]+L,T])
            node.append([NODE[-1][0][0]+L,D-T])
            node.append([NODE[-1][0][0]+L,D])
            
            NODE.append(node)
        
        #for i in NODE:
        #    print(i)
        return NODE