
# 文档代码

from pymysql import connect
from coolmysql import ORM, mc, mf
def mkconn():
    return connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = '123456789'
    )

orm = ORM(mkconn=mkconn)  # 账户ORM
db = orm['泉州市']  # 库ORM
sheet = db['希望小学']  # 表ORM
line1 = {'姓名': '小一', '年龄':11, '签到日期':'2023-01-11'}
line2 = {'姓名': '小二', '年龄':12, '签到日期':'2023-01-12'}
line3 = {'姓名': '小三', '年龄':13, '签到日期':'2023-01-13'}
line4 = {'姓名': '小四', '年龄':14, '签到日期':'2023-01-14'}
line5 = {'姓名': '小五', '年龄':15, '签到日期':'2023-01-15'}
line6 = {'姓名': '小六', '年龄':16, '签到日期':'2023-01-16'}

r1 = sheet + line1  # 单条添加
r2 = sheet + [line2, line3, line4, line5, line6]  # 批量添加
r1.lastrowid
r2.lastrowid
sheet[:]  # 查询所有数据

sheet[3]  # 查询第3条数据

sheet[mc.年龄>13][mc.姓名=='小五'][1]  # 查询年龄大于13、且姓名叫'小五'的第1条数据
sheet[mc.年龄>10][2:5] = {
    '视力': 5.0,
    '性别': '男',
    '爱好': '足球,篮球,画画,跳绳'
}
# 删除年龄>=15的所有数据
sheet[mc.年龄>=15][:] = None

# 删除年龄大于10、且喜欢足球的第2条数据
sheet[mc.年龄>10][mc.爱好.re('足球')][2] = None

# 删除所有数据
sheet[:] = None
sheet[mc.年龄>11][mc.年龄<30]['姓名','年龄'][:]
sheet[mc.年龄>11]['姓名']['年龄'][:]
sheet[mc.年龄>11]['姓名']['*'][:]
_ = sheet
_ = _[mc.年龄>=12]  # 比较
_ = _[mc.姓名.isin('小三','小四')]  # 被包含
_ = _[mc.姓名.notin('十三','十四')]  # 不被包含
_ = _[(mc.年龄==15) | (mc.年龄>15) | (mc.年龄<15)]  # 并集
_ = _[mc.年龄>=3][mc.年龄<100]  # 交集
_ = _[(mc.年龄>=3) - (mc.年龄>100)]  # 差集
_ = _[~ (mc.年龄>100)]  # 补集
_ = _[mc.姓名.re('小')]  # 正则表达式
_[:]  # 切片
sheet[mc.年龄>12].order(年龄=False, 姓名=True)[2:4]
sheet[mc.年龄>12].order(年龄=True)[1:-1]

sheet[mc.年龄>12].order(年龄=False)[-1:1]
sheet.order(年龄=True, 姓名=False).order(年龄=False)[:]
sheet.order(年龄=True, 姓名=False).order()[:]
# 修改第2~5条数据
sheet[2:5] = {'性别':'女'}
r = sheet.update({'性别':'女'})[2:5]
r.rowcount
# 删除年龄>13的第2条数据
sheet[mc.年龄>13][2] = None

# 删除年龄>13的第2~4条数据
sheet[mc.年龄>13][2:4] = None
r1 = sheet[mc.年龄>13].delete()[2]
r2 = sheet[mc.年龄>13].delete()[2:4]

r1.rowcount
r2.rowcount
sheet.getPK( )
sheet.getColumns( )
len( sheet )
len( sheet[mc.年龄>10] )
orm.getDbNames( )
'泉州市'  in  orm
len( orm )
db.getSheetNames( )
'希望小学'  in  db
len( db )
# 在查询、删除、修改的条件中使用
sheet[mf.year('签到日期') == 2023][:]
sheet[mf.year('签到日期') == 2029][:] = None
sheet[mf.year('签到日期') == 2023][2:5] = {'性别':'女'}

# 在修改中使用
sheet[:] = {'备注': '签到日期'}  # 修改为'签到日期'这个字符串
sheet[:] = {'备注': mc.签到日期}  # 修改为各自的'签到日期'字段的值
sheet[:] = {'备注': mf.year('签到日期')}  # 修改为各自的'签到日期'字段的值经year处理后的值
data, cursor = sheet.execute('select 姓名 from 希望小学 limit 1')
data
# >>> [{'姓名': '小一'}]

data, cursor = sheet.execute('update 希望小学 set 爱好="编程" limit 3')
cursor.rowcount
# >>> 3

data, cursor = sheet.execute("delete from 希望小学 limit 2")
cursor.rowcount
# >>> 2

sql = 'insert into 希望小学(姓名, 年龄) values (%s, %s)'
students = [('小七', 17), ('小八', 18)]
data, cursor = sheet.executemany(sql, students)
cursor.lastrowid
# >>> 8
orm.close()

# 或者：
db.close()

# 或者:
sheet.close()
from coolmysql import MysqlColumn

class MC2(MysqlColumn):
    姓名 = 年龄 = 签到日期 = 年级 = 爱好 = None

mc2 = MC2()

sheet[mc2.年龄 > 10][:]
from coolmysql import MysqlFunc

class MF2(MysqlFunc):
    reverse = length = lower = upper = None

mf2 = MF2()

sheet[mf2.reverse('姓名') == '二小'][:]
sheet[mc.年龄 > 5]['姓名','年龄'][mc.姓名.re('小')].order(id=False)[:]
d1 = sheet
d2 = d1[mc.年龄 > 5]
d3 = d2['姓名','年龄']
d4 = d3[mc.姓名.re('小')]
d5 = d4.order(id=False)
d5[:]

# 严格测试

from pymysql import connect
from coolmysql import ORM, mc, mf
try:
    from coolmysql._coolmysql import dbORM, sheetORM
except:
    from coolmysql.coolmysql._coolmysql import dbORM, sheetORM

def mkconn():
    return connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = '123456789'
    )

orm = ORM(mkconn=mkconn)  # 账户ORM
db, _ = orm['泉州市', '漳州市']  # 库ORM
assert type(db) is type(_) is dbORM
sheet, _ = db['希望小学', '天乐小学']  # 表ORM
assert type(sheet) is type(_) is sheetORM

def 重置数据():
    sheet[:] = None
    assert len(sheet) == 0
    line1 = {'姓名': '小一', '年龄':11, '签到日期':'2023-01-11'}
    line2 = {'姓名': '小二', '年龄':12, '签到日期':'2023-01-12'}
    line3 = {'姓名': '小三', '年龄':13, '签到日期':'2023-01-13'}
    line4 = {'姓名': '小四', '年龄':14, '签到日期':'2023-01-14'}
    line5 = {'姓名': '小五', '年龄':15, '签到日期':'2023-01-15'}
    line6 = {'姓名': '小六', '年龄':16, '签到日期':'2023-01-16'}
    line7 = {'姓名': '小七', '年龄':17, '签到日期':'2023-01-17'}
    line8 = {'姓名': '小八', '年龄':18, '签到日期':'2023-01-18'}
    line9 = {'姓名': '小九', '年龄':19, '签到日期':'2023-01-19'}
    r1 = sheet + line1  # 单条添加
    assert len(sheet) == 1
    r2 = sheet + [line2, line3, line4, line5, line6, line7, line8, line9]  # 批量添加
    assert len(sheet) == 9
    r1.lastrowid
    r2.lastrowid


重置数据()

# 查询
r = sheet[:]  # 查询所有数据
assert len(r) == 9
assert r[0]['年龄'] == 11
r = sheet[3]  # 查询第3条数据
assert r['年龄'] == 13
r = sheet[mc.年龄>13][mc.姓名=='小五'][1]  # 查询年龄大于13、且姓名叫'小五'的第1条数据
assert r['年龄'] == 15

# 修改

sheet[mc.年龄>10][2:5] = {
    '视力': 5.0,
    '性别': '男',
    '爱好': '足球,篮球,画画,跳绳'
}
r = sheet[mc.视力==5.0][:]
assert len(r) == 4
assert r[0]['年龄'] == 12
assert r[-1]['年龄'] == 15

# 删除年龄>=15的所有数据
sheet[mc.年龄>=15][:] = None
assert len(sheet) == 4
assert sheet[-1]['年龄'] == 14

# 删除年龄大于10、且喜欢足球和篮球的第2条数据
sheet[mc.年龄>10][mc.爱好.re('足球')][mc.爱好.re('篮球')][2] = None
assert len(sheet) == 3
assert [x['年龄'] for x in sheet[:]] == [11, 12, 14]

# 删除所有数据
sheet[:] = None
assert len(sheet) == 0

重置数据()


# 切片

assert sheet[1]['年龄'] == 11
assert sheet[-1]['年龄'] == 19
assert sheet[2]['年龄'] == 12
assert sheet[-2]['年龄'] == 18
assert [x['年龄'] for x in sheet[3:5]] == [13, 14, 15]

# 限定字段
assert frozenset(sheet['姓名','年龄'][1]) == frozenset(['姓名', '年龄'])
assert frozenset(sheet['姓名']['年龄'][1]) == frozenset(['年龄'])
assert len(sheet[mc.年龄>11]['姓名']['*'][:]) > 1

# 排序
r = sheet[mc.年龄>12].order(年龄=False, 姓名=True)[2:4]
assert [x['年龄'] for x in r] == [18, 17, 16]
r1 = sheet[mc.年龄>12].order(年龄=True)[1:-1]
r2 = sheet[mc.年龄>12].order(年龄=False)[-1:1]
assert [x['年龄'] for x in r1] == [x['年龄'] for x in r2]
r = sheet.order(年龄=True, 姓名=False).order(年龄=False)[:]
assert r[0]['年龄'] == 19
r = sheet.order(年龄=True, 姓名=False).order()[:]
assert r[0]['年龄'] == 11

重置数据()
sheet[2:5] = {'性别':'女'}
r = sheet[mc.性别=='女'][:]
assert [x['年龄'] for x in r] == [12, 13, 14, 15]
r = sheet.update({'性别':'男'})[2:5]
assert [x['年龄'] for x in sheet[mc.性别=='男'][:]] == [12, 13, 14, 15]

# 删除
sheet[mc.年龄>13][2] = None
assert len(sheet) == 8
assert [x['年龄'] for x in sheet[:]] == [11, 12, 13, 14, 16, 17, 18, 19]
sheet[mc.年龄>13][2:4] = None
assert len(sheet) == 5
assert [x['年龄'] for x in sheet[:]] == [11, 12, 13, 14, 19]
r1 = sheet[mc.年龄>13].delete()[2]
assert [x['年龄'] for x in sheet[:]] == [11, 12, 13, 14]
r2 = sheet[mc.年龄>13].delete()[2:4]
assert [x['年龄'] for x in sheet[:]] == [11, 12, 13, 14]
r1.rowcount
r2.rowcount

重置数据()

# 统计
assert sheet.getPK( ) == 'id'
len( sheet[mc.年龄>10] ) == 9
len( sheet[mc.年龄>15] ) == 4
assert '泉州市'  in  orm
assert db.getSheetNames( ) == ['希望小学']
assert '希望小学'  in  db
assert len( db ) == 1

# 调用mysql函数
# 在查询、删除、修改的条件中使用
assert len(sheet[mf.year('签到日期') == 2023][:]) == 9
sheet[mf.year('签到日期') == 2029][:] = None
assert len(sheet) == 9
sheet[mf.year('签到日期') == 2023][2:5] = {'性别':'女'}
assert [x['年龄'] for x in sheet[mc.性别=='女'][:]] == [12, 13, 14, 15]
# 在修改中使用
sheet[:] = {'备注': '签到日期'}  # 修改为'签到日期'这个字符串
assert len(sheet[mc.备注 == '签到日期']) == 9
sheet[:] = {'备注': mc.签到日期}  # 修改为各自的'签到日期'字段的值
assert sheet[1]['备注'] == '2023-01-11'
assert sheet[-1]['备注'] == '2023-01-19'
sheet[:] = {'备注': mf.year('签到日期')}  # 修改为各自的'签到日期'字段的值经year处理后的值
assert sheet[1]['备注'] == '2023'
assert sheet[-1]['备注'] == '2023'

重置数据()

# 执行原生sql
data, cursor = sheet.execute('select 姓名 from 希望小学 limit 1')
assert len(data) == 1
assert data[0]['姓名'] == '小一'
data, cursor = sheet.execute('update 希望小学 set 爱好="编程" limit 3')
assert cursor.rowcount == 3
assert [x['年龄'] for x in sheet[mc.爱好=='编程'][:]] == [11, 12, 13]
data, cursor = sheet.execute("delete from 希望小学 limit 2")
assert cursor.rowcount == 2
assert [x['年龄'] for x in sheet[:]] == [13, 14, 15, 16, 17, 18, 19]
sql = 'insert into 希望小学(姓名, 年龄) values (%s, %s)'
students = [('小七', 17), ('小八', 18)]
data, cursor = sheet.executemany(sql, students)
cursor.lastrowid
assert [x['年龄'] for x in sheet[:]] == [13, 14, 15, 16, 17, 18, 19, 17, 18]

# 关闭连接
orm.close()
db.close()
sheet.close()

重置数据()

# 字段提示
from coolmysql import MysqlColumn
class MC2(MysqlColumn):
    姓名 = 年龄 = 签到日期 = 年级 = 爱好 = None
mc2 = MC2()
assert [x['年龄'] for x in sheet[mc2.年龄 > 15][:]] == [16, 17, 18, 19]

# 函数名提示
from coolmysql import MysqlFunc
class MF2(MysqlFunc):
    reverse = length = lower = upper = None
mf2 = MF2()
r = sheet[mf2.reverse('姓名') == '二小'][:]
assert len(r) == 1
assert r[0]['年龄'] == 12

sheet[mc.年龄 > 5]['姓名','年龄'][mc.姓名.re('小')].order(id=False)[:]
d1 = sheet
d2 = d1[mc.年龄 > 5]
d3 = d2['姓名','年龄']
d4 = d3[mc.姓名.re('小')]
d5 = d4.order(id=False)
d5[:]

# 清理测试数据
sheet[:] = None
assert len(sheet) == 0

print('测试通过')