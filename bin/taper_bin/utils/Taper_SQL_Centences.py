#taper模
create_EC0120_B000 = """
CREATE TABLE IF NOT EXISTS B000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    '%%CA' TEXT NOT NULL,
    '%%CB' TEXT NOT NULL,
    L TEXT NOT NULL,
    L_m TEXT NOT NULL,
    line1 TEXT NOT NULL,
    line2 TEXT NOT NULL,
    line3 TEXT NOT NULL,
    line4 TEXT NOT NULL,
    line5 TEXT NOT NULL,
    line6 TEXT NOT NULL,
    line7 TEXT NOT NULL,
    line8 TEXT NOT NULL,
    line9 TEXT NOT NULL,
    line10 TEXT NOT NULL,
    line11 TEXT NOT NULL,
    line12 TEXT NOT NULL,
    line13 TEXT NOT NULL,
    line14 TEXT NOT NULL,
    line15 TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_EC0120_B000 = ('INSERT INTO B000 ("图号", "%%CD","%%CA","%%CB","L","L_m","line1","line2",'
                      '"line3","line4","line5","line6","line7","line8",'
                      '"line9","line10","line11","line12","line13","line14","line15",'
                      ' "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
insert_EC0120_B000_list = [('图号', "%%CD","%%CA","%%CB","L","L_m","line1","line2","line3","line4","line5","line6","line7","line8",
                            "line9","line10","line11","line12","line13","line14","line15",
                            "件数", "日期", "模具名称", "设计者", "车种规格"),insert_EC0120_B000]

create_EC0121_B000 = """
CREATE TABLE IF NOT EXISTS B000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    '%%CD' TEXT NOT NULL,
    '%%CA' TEXT NOT NULL,
    '%%CB' TEXT NOT NULL,
    L TEXT NOT NULL,
    L_m TEXT NOT NULL,
    line1 TEXT NOT NULL,
    line2 TEXT NOT NULL,
    line3 TEXT NOT NULL,
    line4 TEXT NOT NULL,
    line5 TEXT NOT NULL,
    line6 TEXT NOT NULL,
    line7 TEXT NOT NULL,
    line8 TEXT NOT NULL,
    line9 TEXT NOT NULL,
    line10 TEXT NOT NULL,
    line11 TEXT NOT NULL,
    line12 TEXT NOT NULL,
    line13 TEXT NOT NULL,
    line14 TEXT NOT NULL,
    line15 TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_EC0121_B000 = ('INSERT INTO B000 ("图号", "%%CD","%%CA","%%CB","L","L_m","line1","line2",'
                      '"line3","line4","line5","line6","line7","line8",'
                      '"line9","line10","line11","line12","line13","line14","line15",'
                      ' "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
insert_EC0121_B000_list = [('图号', "%%CD","%%CA","%%CB","L","L_m","line1","line2","line3","line4","line5","line6","line7","line8",
                            "line9","line10","line11","line12","line13","line14","line15",
                            "件数", "日期", "模具名称", "设计者", "车种规格"),insert_EC0121_B000]

#定位杆
create_EC0120_C000 = """
CREATE TABLE IF NOT EXISTS C000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_EC0120_C000 = 'INSERT INTO C000 ("图号", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_EC0120_C000_list = [('图号', "A", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_EC0120_C000]

create_EC0121_C000 = """
CREATE TABLE IF NOT EXISTS C000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_EC0121_C000 = 'INSERT INTO C000 ("图号", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_EC0121_C000_list = [('图号', "A", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_EC0121_C000]

#夹模
create_EC0120_J000 = """
CREATE TABLE IF NOT EXISTS J000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_EC0120_J000 = 'INSERT INTO J000 ("图号", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_EC0120_J000_list = [('图号', "A", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_EC0120_J000]

create_EC0121_J000 = """
CREATE TABLE IF NOT EXISTS J000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    A TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_EC0121_J000 = 'INSERT INTO J000 ("图号", "A", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_EC0121_J000_list = [('图号', "A", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_EC0121_J000]

#后定位模
create_E000 = """
CREATE TABLE IF NOT EXISTS E000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    B TEXT NOT NULL,
    D TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_E000 = 'INSERT INTO E000 ("图号", "B","D", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?,?)'
insert_E000_list = [('图号', "B","D", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_E000]

#内定位模
create_I000 = """
CREATE TABLE IF NOT EXISTS I000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    B TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_I000 = 'INSERT INTO I000 ("图号", "B", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_I000_list = [('图号', "B", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_I000]

#拉杆
create_H000 = """
CREATE TABLE IF NOT EXISTS H000 (
    图号 INTEGER PRIMARY KEY AUTOINCREMENT,
    B TEXT NOT NULL,
    件数 TEXT NOT NULL,
    日期 TEXT NOT NULL,
    模具名称 TEXT NOT NULL,
    设计者 TEXT NOT NULL,
    车种规格 TEXT NOT NULL
)"""
insert_H000 = 'INSERT INTO H000 ("图号", "B", "件数", "日期", "模具名称", "设计者", "车种规格") VALUES (?,?,?,?,?,?,?)'
insert_H000_list = [('图号', "B", "件数", "日期", "模具名称", "设计者", "车种规格"),insert_H000]


create_sentencesEC = {
    "EC0120": {
        'B000': create_EC0120_B000,
        'C000': create_EC0120_C000,
        'J000': create_EC0120_J000,
        'E000': create_E000,
        'I000': create_I000,
        'H000': create_H000
    },
    "EC0121": {
        'B000': create_EC0121_B000,
        'C000': create_EC0121_C000,
        'J000': create_EC0121_J000
    },
}

insert_sentences_listEC = {
    "EC0120": {
        'B000': insert_EC0120_B000_list,
        'C000': insert_EC0120_C000_list,
        'J000': insert_EC0120_J000_list,
        'E000': insert_E000_list,
        'I000': insert_I000_list,
        'H000': insert_H000_list
    },
    "EC0121": {
        'B000': insert_EC0121_B000_list,
        'C000': insert_EC0121_C000_list,
        'J000': insert_EC0121_J000_list
    },
}