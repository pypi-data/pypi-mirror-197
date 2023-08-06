import asyncio

async def 文档代码():
    from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
    import asymongo as mg
    from asymongo import mc, mup
    mkconn = lambda: MongoClient(host='localhost', port=27017)

    orm = mg.ORM(mkconn=mkconn)  # 账户ORM
    db = orm['泉州市']  # 库ORM
    sheet = db['希望小学']  # 表ORM
    line1 = {'姓名': '小一', '年龄':11, '幸运数字':[1, 2, 3], '成绩':{'语文':81, '数学':82}}
    line2 = {'姓名': '小二', '年龄':12, '幸运数字':[2, 3, 4], '成绩':{'语文':82, '数学':83}}
    line3 = {'姓名': '小三', '年龄':13, '幸运数字':[3, 4, 5], '成绩':{'语文':83, '数学':84}}
    line4 = {'姓名': '小四', '年龄':14, '幸运数字':[4, 5, 6], '成绩':{'语文':84, '数学':85}}
    line5 = {'姓名': '小五', '年龄':15, '幸运数字':[5, 6, 7], '成绩':{'语文':85, '数学':86}}
    line6 = {'姓名': '小六', '年龄':16, '幸运数字':[6, 7, 8], '成绩':{'语文':86, '数学':87}}

    r1 = await sheet.insert(line1)  # 单条添加
    r2 = await sheet.insert([ line2, line3, line4, line5, line6 ])  # 批量添加
    r1.inserted_id
    r2.inserted_ids
    await sheet[:]  # 查询所有数据

    await sheet[3]  # 查询第3条数据

    await sheet[mc.成绩.语文 == 85][:]  # 查询语文成绩为85分的数据

    await sheet[mc.年龄>13][mc.姓名=='小五'][1]  # 查询年龄大于13、且姓名叫'小五'的第1条数据
    data = {
        '视力': 5.0,
        '性别': '男',
        '爱好': ['足球','篮球','画画','跳绳'],
        '幸运数字': mup.push(15,16,17),  # 添加到列表
        '年龄': mup.inc(2)  # 自增
    }

    # 删除年龄>=15的数据
    r1 = await sheet[mc.年龄>=15].delete()[:]
    # 删除年龄大于10、且姓名包含'小'的第2条数据
    r2 = await sheet[mc.年龄>10][mc.姓名 == mg.re('小')].delete()[2]
    # 删除所有数据
    r3 = await sheet.delete()[:]
    # 查看删除详情
    r1.raw_result
    r2.raw_result
    r3.raw_result

    await sheet[mc.成绩.语文 > 80][:]
    await sheet[mc.年龄>11][mc.年龄<30]['姓名','年龄'][:]
    await sheet[mc.年龄>11]['姓名']['年龄'][:]
    await sheet[mc.年龄>11]['姓名'][mg.allColumns][:]
    _ = sheet
    _ = _[mc.年龄>=12]  # 比较
    _ = _[mc.姓名 == mg.isin('小三','小四')]  # 被包含
    _ = _[mc.姓名 == mg.notin('十三','十四')]  # 不被包含
    _ = _[(mc.年龄==15) | (mc.年龄>15) | (mc.年龄<15)]  # 并集
    _ = _[mc.年龄>=3][mc.年龄<100]  # 交集
    _ = _[(mc.年龄>=3) - (mc.年龄>100)]  # 差集
    _ = _[~ (mc.年龄>100)]  # 补集
    _ = _[mc.姓名 == mg.re('小')]  # 正则表达式
    _ = _[mc.幸运数字 == mg.containAll(4, 5, 6)]  # 包含所有值
    _ = _[mc.幸运数字 == mg.containAny(4, 5, 6)]  # 包含至少1个值
    _ = _[mc.幸运数字 == mg.containNo(1, 2, 3)]  # 1个都不包含
    await _[:]  # 切片
    await sheet[mc.年龄>12].order(年龄=False, 姓名=True)[2:4]
    await sheet[mc.年龄>12].order(年龄=True)[1:-1]

    await sheet[mc.年龄>12].order(年龄=False)[-1:1]
    await sheet.order(年龄=True, 姓名=False).order(年龄=False)[:]
    await sheet.order(年龄=True, 姓名=False).order()[:]
    r = await sheet.update({'性别':'女'})[2:5]

    r.raw_result  # 查看修改详情
    data = {'年龄':mup.inc(1.5)}

    await sheet[mc.年龄>10].update(data)[6:1:4]
    data = {
        '姓名': 'xiaoliu',
        '年龄': mup.inc(6),
        '幸运数字': mup.push(666),
        '视力': mup.rename('眼力'),
        '籍贯': mup.delete,
        '成绩.语文': 60,
        '成绩.数学': mup.inc(-10)
    }

    await sheet[mc.姓名=='小六'].update(data)[:]
    from asymongo import MongoColumn

    class MC2(MongoColumn):
        姓名 = 年龄 = 幸运数字 = None
        class 成绩:
            语文 = 数学 = None

    mc2 = MC2()

    await sheet[mc2.年龄 > 10][:]
    await sheet[mc.年龄 > 5]['姓名','年龄'][mc.姓名 == mg.re('小')].order(_id=False)[:]
    d1 = sheet
    d2 = d1[mc.年龄 > 5]
    d3 = d2['姓名','年龄']
    d4 = d3[mc.姓名 == mg.re('小')]
    d5 = d4.order(_id=False)
    await d5[:]
asyncio.run(文档代码())


# 严格测试

async def 严格测试():
    from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
    import asymongo as mg
    from asymongo import mc, mup
    from asymongo import MongoColumn
    try:
        from asymongo._asymongo import dbORM, sheetORM
    except:
        from asymongo.asymongo._asymongo import dbORM, sheetORM

    mkconn = lambda: MongoClient(host='localhost', port=27017)
    orm = mg.ORM(mkconn=mkconn)
    db, db2 = orm['_test_test_test_', '_test_test_test_2']
    assert type(db) is type(db2) is dbORM
    await orm.delete_dbs('_test_test_test_2')
    sheet, sheet2 = db['学生', '学生2']
    assert type(sheet) is type(sheet2) is sheetORM
    await db.delete_sheets('学生2')

    async def 重置数据():
        await sheet.delete()[:]
        assert await sheet.len() == 0
        line1 = {'姓名': '小一', '序号':1, '幸运数字':[1, 2, 3], '成绩':{'语文':81, '数学':82}}
        line2 = {'姓名': '小二', '序号':2, '幸运数字':[2, 3, 4], '成绩':{'语文':82, '数学':83}}
        line3 = {'姓名': '小三', '序号':3, '幸运数字':[3, 4, 5], '成绩':{'语文':83, '数学':84}}
        line4 = {'姓名': '小四', '序号':4, '幸运数字':[4, 5, 6], '成绩':{'语文':84, '数学':85}}
        line5 = {'姓名': '小五', '序号':5, '幸运数字':[5, 6, 7], '成绩':{'语文':85, '数学':86}}
        line6 = {'姓名': '小六', '序号':6, '幸运数字':[6, 7, 8], '成绩':{'语文':86, '数学':87}}
        line7 = {'姓名': '小七', '序号':7, '幸运数字':[7, 8, 9], '成绩':{'语文':87, '数学':88}}
        line8 = {'姓名': '小八', '序号':8, '幸运数字':[8, 9, 10], '成绩':{'语文':88, '数学':89}}
        line9 = {'姓名': '小九', '序号':9, '幸运数字':[9, 10, 11], '成绩':{'语文':89, '数学':90}}
        r1 = await sheet.insert(line1)
        assert await sheet.len() == 1
        r2 = await sheet.insert([line2, line3, line4, line5, line6, line7, line8, line9])
        assert await sheet.len() == 9
        r1.inserted_id
        r2.inserted_ids

    # 单条添加, 批量添加
    await 重置数据()

    # 查询
    assert len(await sheet[:]) == 9

    x = await sheet[3]
    assert type(x) is dict
    assert x['序号'] == 3

    r = await sheet[mc.成绩.语文 >= 87][:]
    assert len(r) == 3
    assert r[0]['成绩']['语文'] == 87

    r = await sheet[mc.序号>=2][mc.姓名=='小五'][1]
    assert r['序号'] == 5

    # 修改

    await sheet.update({
        '视力': 5.0,
        '爱好': ['足球', '篮球', '画画', '跳绳'],
        '性别': '男'
    })[:]
    r = await sheet[mc.视力==5][:]
    assert len(r) == 9

    await sheet.update({'性别':'女'})[2:5]
    r = await sheet[mc.性别=='女'][:]
    assert len(r) == 4
    assert r[0]['序号'] == 2


    await sheet[mc.性别=='男'].update({
        '爱好': mup.push('编程', '跑步'),
        '视力': mup.inc(-0.5),
        '身高': 172
    })[:]
    r = await sheet[mc.性别=='男'][mc.爱好==mg.containAll('编程','跑步')][:]
    assert r
    for x in r:
        assert x['视力'] == 4.5
        assert x['身高'] == 172


    # 删除

    await sheet[mc.序号>=6].delete()[:]
    assert await sheet.len() == len(await sheet[:]) == 5
    await sheet.delete()[:]
    assert await sheet.len() == len(await sheet[:]) == 0


    # 成员运算
    await 重置数据()

    r = await sheet[mc.幸运数字==mg.containAll(2,3,4)][:]
    assert len(r) == 1
    assert r[0]['序号'] == 2
    assert len(await sheet[mc.幸运数字==mg.containAll()][:]) == 9

    r = await sheet[mc.幸运数字==mg.containAny(2)][:]
    assert len(r) == 2
    assert r[0]['序号'] == 1
    assert not await sheet[mc.幸运数字==mg.containAny()][:]

    r = await sheet[mc.幸运数字==mg.containNo(1,2,3)][:]
    assert len(r) == 6
    assert r[0]['序号'] == 4
    assert len(await sheet[mc.幸运数字==mg.containNo()][:]) == 9

    r = await sheet[mc.序号==mg.isin(4,5,6)][:]
    assert len(r) == 3
    assert r[0]['序号'] == 4
    assert r[-1]['序号'] == 6
    assert len(await sheet[mc.序号==mg.isin()][:]) == 0

    r = await sheet[mc.序号==mg.notin(4,5,6)][:]
    assert len(r) == 6
    assert len(await sheet[mc.序号==mg.notin()][:]) == 9

    assert len(await sheet[mc.姓名==mg.re('小')][:]) == 9

    # 集合运算

    r = await sheet[ mc.序号>=3 ][ mc.序号<=7 ][:]
    assert len(r) == 5
    assert r[0]['序号'] == 3

    r = await sheet[ (mc.序号<=3) | (mc.序号>=7) ][:]
    assert len(r) == 6
    assert r[3]['序号'] == 7

    r = await sheet[ (mc.序号>3) - (mc.序号>=7) ][:]
    assert len(r) == 3
    assert r[-1]['序号'] == 6

    r = await sheet[ ~(mc.序号>3)][:]
    assert len(r) == 3
    assert r[-1]['序号'] == 3

    # 根据子元素过滤
    r = await sheet[mc.成绩.语文 <= 85][:]
    assert len(r) == 5
    assert r[-1]['序号'] == 5

    # 切片
    r = await sheet[:]
    assert len(r) == 9

    r = await sheet[::2]
    assert len(r) == 5
    assert r[0]['序号'] == 1

    r = await sheet[9:1:2]
    assert len(r) == 5
    assert r[0]['序号'] == 9

    assert len(await sheet[2:8]) == len(await sheet[8:2]) == len(await sheet[2:-2]) == len(await sheet[-2:2]) == len(await sheet[-8:8]) == len(await sheet[8:-8]) == 7
    assert len(await sheet[-2:-8]) == len(await sheet[-8:-2]) == 7

    assert len(await sheet[1:9]) == len(await sheet[9:1]) == len(await sheet[1:-1]) == len(await sheet[-1:1]) == len(await sheet[-9:9]) == len(await sheet[9:-9]) == 9
    assert len(await sheet[-1:-9]) == len(await sheet[-9:-1]) == 9
    assert len(await sheet[:]) == len(await sheet[:9]) == len(await sheet[:-1]) == 9

    # 限定字段
    r = await sheet['序号'][:]
    assert list(r[0]) == ['序号']

    r = await sheet['姓名', '成绩']['序号'][:]
    assert list(r[0]) == ['序号']

    r = await sheet['姓名', '成绩']['序号'][mg.allColumns][:]
    assert list(r[0]) == ['_id', '姓名', '序号', '幸运数字', '成绩']

    # 复杂查询
    _ = sheet[mc.年龄>=12]  # 比较
    _ = _[mc.姓名 == mg.isin('小三', '小四')]  # 被包含
    _ = _[mc.姓名 == mg.notin('十三', '十四')]  # 不被包含
    _ = _[(mc.年龄==15) | (mc.年龄>15) | (mc.年龄<15)]  # 并集
    _ = _[mc.年龄>=3][mc.年龄<100]  # 交集
    _ = _[(mc.年龄>=3) - (mc.年龄>100)]  # 差集
    _ = _[~ (mc.年龄>100)]  # 补集
    _ = _[mc.姓名 == mg.re('小')]  # 正则表达式
    _ = _[mc.幸运数字 == mg.containAll(4, 5, 6)]  # 包含所有值
    _ = _[mc.幸运数字 == mg.containAny(4, 5, 6)]  # 包含至少1个值
    _ = _[mc.幸运数字 == mg.containNo(1, 2, 3)]  # 1个都不包含
    await _[:]

    # 排序
    r = await sheet.order(序号=False)[:]
    assert len(r) == 9
    assert r[0]['序号'] == 9

    r = await sheet.order(序号=False)[9:1:2]
    assert len(r) == 5
    assert r[0]['序号'] == 1

    # 修改

    await sheet.update({'性别':'女'})[2:5]
    r = await sheet[mc.性别=='女'][:]
    assert len(r) == 4
    assert r[0]['序号'] == 2

    r = await sheet[mc.性别!='女'][:]
    assert len(r) == 5
    assert r[0]['序号'] == 1
    assert r[1]['序号'] == 6

    r = await sheet.update({'性别':'女'})[2:5]
    r.raw_result

    await sheet[mc.姓名=='小六'].update({
        '姓名': 'xiaoliu',
        '年龄': mup.inc(6),
        '幸运数字': mup.push(666),
        '视力': mup.rename('眼力'),
        '籍贯': mup.delete,
        '成绩.语文': 60,
        '成绩.数学': mup.inc(-10)
    })[:]
    r = await sheet[mc.姓名=='xiaoliu'][1]
    assert r['姓名'] == 'xiaoliu' and r['序号']==6 and 666 in r['幸运数字'] and r['成绩']['语文']==60 and r['成绩']['数学']==77
    assert r['年龄'] == 6

    # 删除
    r1 = await sheet[mc.序号>=1].delete()[2]
    r2 = await sheet[mc.序号>=1].delete()[2:4]
    r1.raw_result
    r2.raw_result

    # 统计

    await 重置数据()
    assert await sheet.len() == 9
    assert await sheet[mc.序号<=4].len() == 4
    assert await db.len() == 1
    await orm.getDbNames()
    assert await db.getSheetNames() == ['学生']

    #################################################### 字段提示
    class MC2(MongoColumn):
        姓名 = 序号 = 幸运数字 = None
        class 成绩:
            语文 = 数学 = None
    mc2 = MC2()
    mc2.成绩.语文

    r = await sheet[mc2.序号<=7][:]
    assert len(r) == 7
    assert r[-1]['序号'] == 7

    r = await sheet[mc2.成绩.语文 == 88][:]
    assert len(r) == 1
    assert r[0]['序号'] == 8

    # 清理测试数据

    await orm.delete_dbs('_test_test_test_')

asyncio.run(严格测试())

print('测试通过')