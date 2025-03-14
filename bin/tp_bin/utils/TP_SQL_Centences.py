# DC0128机床模具定义
# mold_definitions = {
#     '裁剪夹模1': 'AD01',
#     '裁剪夹模2': 'AD01_',
#     '抽套模': 'ADIE',
#     '成型抽套模': 'ADIE_',
#     '抽管芯轴': 'ADBT',
#     '成型抽管芯轴': 'ADBT',
#     '抽管退料模': 'AD04',
# }

create_DC0128_AD01 = """
CREATE TABLE IF NOT EXISTS AD01 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0128_AD01_ = """
CREATE TABLE IF NOT EXISTS AD01_ (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0128_AD01 = 'INSERT INTO AD01 ("图号",  "%%CD", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_DC0128_AD01_ = 'INSERT INTO AD01_ ("图号", "%%CD", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_DC0128_AD01_list = [('图号', '%%CD', '件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0128_AD01]
insert_DC0128_AD01__list = [('图号', '%%CD','件数', '日期', '模具名称', '设计者', '车种规格'),insert_DC0128_AD01_]


#抽套膜
create_DC0128_ADIE = """
CREATE TABLE IF NOT EXISTS ADIE(
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    s_bore TEXT NOT NULL,
    b_bore TEXT NOT NULL,
    length TEXT NOT NULL,
    L TEXT NOT NULL,
    line TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0128_ADIE_ = """
CREATE TABLE IF NOT EXISTS ADIE_ (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    s_bore TEXT NOT NULL,
    b_bore TEXT NOT NULL,
    length TEXT NOT NULL,
    line TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0128_ADIE = 'INSERT INTO ADIE ("图号", "s_bore", "b_bore","length", "L","line","件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?)'
insert_DC0128_ADIE_ = 'INSERT INTO ADIE_ ("图号", "s_bore", "b_bore","length","line","件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?)'
insert_DC0128_ADIE_list = [('图号',"s_bore", "b_bore","length", "L","line","件数", "日期", "模具名称", "设计者", "车种规格"),insert_DC0128_ADIE]
insert_DC0128_ADIE__list = [('图号',"s_bore", "b_bore","length","line","件数", "日期", "模具名称", "设计者", "车种规格"),insert_DC0128_ADIE_]



create_DC0128_ADBT = """
CREATE TABLE IF NOT EXISTS ADBT (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    L1 TEXT NOT NULL,
    M1 TEXT NOT NULL,
    L2 TEXT NOT NULL,
    M2 TEXT NOT NULL,
    L3 TEXT NOT NULL,
    IL TEXT NOT NULL,
    L4 TEXT NOT NULL,
    '%%Cd1' TEXT NOT NULL,
    '%%Cd2' TEXT NOT NULL,
    '%%Cd3' TEXT NOT NULL,
    '%%Cd4' TEXT NOT NULL,
    M TEXT NOT NULL,
    LT TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
create_DC0128_ADBT_ = """
CREATE TABLE IF NOT EXISTS ADBT_ (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    LT TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0128_ADBT = 'INSERT INTO ADBT ("图号", "L1", "M1","L2","M2","L3","IL","L4","%%Cd1","%%Cd2","%%Cd3","%%Cd4","M","LT","件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
insert_DC0128_ADBT_ = 'INSERT INTO ADBT_ ("图号", "%%CD", "LT","件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_DC0128_ADBT_list = [('图号',"L1", "M1","L2","M2","L3","IL","L4","%%Cd1","%%Cd2","%%Cd3","%%Cd4","M","LT","件数", "日期", "模具名称", "设计者", "车种规格"),insert_DC0128_ADBT]
insert_DC0128_ADBT__list = [('图号',"%%CD", "LT","件数", "日期", "模具名称", "设计者", "车种规格"),insert_DC0128_ADBT_]


create_DC0128_AD04 = """
CREATE TABLE IF NOT EXISTS AD04 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_DC0128_AD04 = 'INSERT INTO AD04 ("图号", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_DC0128_AD04_list = [('图号', "A", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_DC0128_AD04]

create_sentences = {
    "DC0128": {
        'AD01': create_DC0128_AD01,
        'AD01_': create_DC0128_AD01_,
        'ADIE': create_DC0128_ADIE,
        'ADIE_': create_DC0128_ADIE_,
        'ADBT': create_DC0128_ADBT,
        'ADBT_': create_DC0128_ADBT_,
        'AD04': create_DC0128_AD04
    },
}

insert_sentences_list = {
    "DC0128": {
        'AD01': insert_DC0128_AD01_list,
        'AD01_': insert_DC0128_AD01__list,
        'ADIE': insert_DC0128_ADIE_list,
        'ADIE_': insert_DC0128_ADIE__list,
        'ADBT': insert_DC0128_ADBT_list,
        'ADBT_': insert_DC0128_ADBT__list,
        'AD04': insert_DC0128_AD04_list
    },
}

