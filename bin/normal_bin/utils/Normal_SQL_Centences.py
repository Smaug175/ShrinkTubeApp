# "管件参数": {"Belta1 (radians)": "/",
# "Belta2 (radians)": "/",
# "D": "/",
# "L": "/",
# "L1": "/",
# "L2": "/",
# "L3": "/",
# "M1": "/",
# "M2": "/",
# "T1": "/",
# "T2": "/",
# "T3": "/",
# "车种规格": "/"},

# INFO %%Cd 和 %%CD 重复，将 %%Cd 改为 %%Cd0，之后读取和加载需要进行匹配
# DIEO 不区分机床型号
create_DIEO = """
CREATE TABLE IF NOT EXISTS DIEO (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    '%%Cd0' TEXT NOT NULL,
    '%%Cd1' TEXT NOT NULL,
    '%%Cd2' TEXT NOT NULL,
    件数 TEXT NOT NULL,
    成品直径 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DIEO = 'INSERT INTO DIEO ("图号", "%%CD", "%%Cd0", "%%Cd1", "%%Cd2", "件数", "成品直径", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?)'
insert_DIEO_list = [('图号', '%%CD', '%%Cd0', '%%Cd1', '%%Cd2', '件数', '成品直径', '日期', '模具名称', '设计者', '车种规格'),insert_DIEO]

# SS01 DC0125 多 L1 参数 DC0121 and DC0124 is the same
create_SS01 = """
CREATE TABLE IF NOT EXISTS SS01 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CA' TEXT NOT NULL,
    '%%CD' TEXT NOT NULL,
    BXB TEXT NOT NULL,
    L TEXT NOT NULL,
    LT TEXT NOT NULL,
    M螺纹 TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0125_SS01 = """
CREATE TABLE IF NOT EXISTS SS01 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CA' TEXT NOT NULL,
    '%%CD' TEXT NOT NULL,
    BXB TEXT NOT NULL,
    L1 TEXT NOT NULL,
    L TEXT NOT NULL,
    LT TEXT NOT NULL,
    M螺纹 TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_SS01 = 'INSERT INTO SS01 ("图号", "%%CA", "%%CD", "BXB", "L", "LT", "M螺纹", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
insert_DC0125_SS01 = 'INSERT INTO SS01 ("图号", "%%CA", "%%CD", "BXB", "L1", "L", "LT", "M螺纹", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'
insert_SS01_list = [('图号', '%%CA', '%%CD', 'BXB', 'L', 'LT', 'M螺纹', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_SS01]
insert_DC0125_SS01_list = [('图号', '%%CA', '%%CD', 'BXB', 'L1', 'L', 'LT', 'M螺纹', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0125_SS01]

# AD02 区分机床型号
create_DC0124_AD02 = """
CREATE TABLE IF NOT EXISTS AD02 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CA' TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0121_AD02 = """
CREATE TABLE IF NOT EXISTS AD02 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0124_AD02 = 'INSERT INTO AD02 ("图号", "%%CA", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_DC0121_AD02 = 'INSERT INTO AD02 ("图号", "%%CD", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_DC0124_AD02_list = [('图号', '%%CA', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0124_AD02]
insert_DC0121_AD02_list = [('图号', '%%CD', 'A', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0121_AD02]

# ADBT 不区分机床型号
create_ADBT = """
CREATE TABLE IF NOT EXISTS ADBT (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CA' TEXT NOT NULL,
    '%%Cd1' TEXT NOT NULL,
    '%%Cd2' TEXT NOT NULL,
    '%%Cd3' TEXT NOT NULL,
    '%%Cd4' TEXT NOT NULL,
    '%%Cd5' TEXT NOT NULL,
    '(L6)' TEXT NOT NULL,
    C TEXT NOT NULL,
    L TEXT NOT NULL,
    L1 TEXT NOT NULL,
    L2 TEXT NOT NULL,
    L3 TEXT NOT NULL,
    L4 TEXT NOT NULL,
    L5 TEXT NOT NULL,
    LT TEXT NOT NULL,
    T TEXT NOT NULL,
    抽管尺寸 TEXT NOT NULL,
    缩管模直径 TEXT NOT NULL,
    件数 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    M螺纹 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_ADBT_sql = 'INSERT INTO ADBT ("图号", "%%CA", "%%Cd1", "%%Cd2", "%%Cd3", "%%Cd4", "%%Cd5", "(L6)", "C", "L", "L1", "L2", "L3", "L4", "L5", "LT", "T", "抽管尺寸", "缩管模直径", "件数", "模具名称", "日期", "设计者", "M螺纹", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
insert_ADBT_sql_list = [('图号', '%%CA', '%%Cd1', '%%Cd2', '%%Cd3', '%%Cd4', '%%Cd5', '(L6)', 'C', 'L', 'L1', 'L2', 'L3', 'L4', 'L5', 'LT', 'T', '抽管尺寸', '缩管模直径', '件数', '模具名称', '日期', '设计者', 'M螺纹', '车种规格'),insert_ADBT_sql]

# INFO %%Cd 和 %%CD 重复，将 %%Cd 改为 %%Cd0，之后读取和加载需要进行匹配
# ADIE 不区分机床型号
create_ADIE = """
CREATE TABLE IF NOT EXISTS ADIE (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    '%%Cd0' TEXT NOT NULL,
    '%%Cd1' TEXT NOT NULL,
    '%%Cd2' TEXT NOT NULL,
    件数 TEXT NOT NULL,
    成品直径 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_ADIE = 'INSERT INTO ADIE ("图号", "%%CD", "%%Cd0", "%%Cd1", "%%Cd2", "件数", "成品直径", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?)'
insert_ADIE_list = [('图号', '%%CD', '%%Cd0', '%%Cd1', '%%Cd2', '件数', '成品直径', '日期', '模具名称', '设计者', '车种规格'),insert_ADIE]

# AD01 different machine is different
create_DC0124_AD01 = """
CREATE TABLE IF NOT EXISTS AD01 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0121_AD01 = """
CREATE TABLE IF NOT EXISTS AD01 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0124_AD01 = 'INSERT INTO AD01 ("图号", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_DC0121_AD01 = 'INSERT INTO AD01 ("图号", "%%CD", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_DC0124_AD01_list = [('图号', 'A', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0124_AD01]
insert_DC0121_AD01_list = [('图号', '%%CD', 'A', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0121_AD01]

# AD06 需要区分表头
create_DC0125_AD06_F = """
CREATE TABLE IF NOT EXISTS AD06_F (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    成品直径 TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0125_AD06_S = """
CREATE TABLE IF NOT EXISTS AD06_S (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    成品直径 TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0125_AD06_F = 'INSERT INTO AD06_F ("图号", "%%CD", "成品直径", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_DC0125_AD06_S = 'INSERT INTO AD06_S ("图号", "%%CD", "成品直径", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_DC0125_AD06_F_list = [('图号', '%%CD', '成品直径', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0125_AD06_F]
insert_DC0125_AD06_S_list = [('图号', '%%CD', '成品直径', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0125_AD06_S]

# AD03
create_DC0124_AD03 = """
CREATE TABLE IF NOT EXISTS AD03 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0121_AD03 = """
CREATE TABLE IF NOT EXISTS AD03 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0124_AD03 = 'INSERT INTO AD03 ("图号", "%%CD", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_DC0121_AD03 = 'INSERT INTO AD03 ("图号", "%%CD", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_DC0124_AD03_list = [('图号', '%%CD', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0124_AD03]
insert_DC0121_AD03_list = [('图号', '%%CD', 'A', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0121_AD03]

# AD04
create_DC0121_AD04 = """
CREATE TABLE IF NOT EXISTS AD04 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0121_AD04 = 'INSERT INTO AD04 ("图号", "%%CD", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_DC0121_AD04_list = [('图号', '%%CD', 'A', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0121_AD04]

# AD07
create_DC0125_AD07 = """
CREATE TABLE IF NOT EXISTS AD07 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0125_AD07 = 'INSERT INTO AD07 ("图号", "%%CD", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_DC0125_AD07_list = [('图号', '%%CD', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0125_AD07]

# 不同机床型号的表的创建语句
create_sentences = {
    "DC0124": {
        'AD03': create_DC0124_AD03,
        'DIEO': create_DIEO,
        'SS01': create_SS01,
        'AD02': create_DC0124_AD02,
        'ADIE': create_ADIE,
        'ADBT': create_ADBT,
        'AD01': create_DC0124_AD01
    },
    "DC0121": {
        'AD03': create_DC0121_AD03,
        'AD04': create_DC0121_AD04,
        'DIEO': create_DIEO,
        'SS01': create_SS01,
        'AD02': create_DC0121_AD02,
        'ADIE': create_ADIE,
        'ADBT': create_ADBT,
        'AD01': create_DC0121_AD01
    },
    "DC0125": {
        'AD06_F': create_DC0125_AD06_F,
        'AD06_S': create_DC0125_AD06_S,
        'DIEO': create_DIEO,
        'SS01': create_DC0125_SS01,
        'AD07': create_DC0125_AD07,
        'ADIE': create_ADIE,
        'ADBT': create_ADBT
    }
}

# 不同机床型号的插入：[key的顺序, 插入语句]
insert_sentences_list = {
    "DC0124": {
        'DIEO': insert_DIEO_list,
        'SS01': insert_SS01_list,
        'AD02': insert_DC0124_AD02_list,
        'ADIE': insert_ADIE_list,
        'ADBT': insert_ADBT_sql_list,
        'AD01': insert_DC0124_AD01_list,
        'AD03': insert_DC0124_AD03_list
    },
    "DC0121": {
        'AD03': insert_DC0121_AD03_list,
        'AD04': insert_DC0121_AD04_list,
        'DIEO': insert_DIEO_list,
        'SS01': insert_SS01_list,
        'AD02': insert_DC0121_AD02_list,
        'ADIE': insert_ADIE_list,
        'ADBT': insert_ADBT_sql_list,
        'AD01': insert_DC0121_AD01_list
    },
    "DC0125": {
        'AD06_F': insert_DC0125_AD06_F_list,
        'AD06_S': insert_DC0125_AD06_S_list,
        'DIEO': insert_DIEO_list,
        'SS01': insert_DC0125_SS01_list,
        'AD07': insert_DC0125_AD07_list,
        'ADIE': insert_ADIE_list,
        'ADBT': insert_ADBT_sql_list
    }
}
