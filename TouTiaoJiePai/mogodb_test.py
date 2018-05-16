import pymongo
connection = pymongo.MongoClient()
tdb = connection.jikexueyuan
post_info = tdb.test
jike = {'name':u'极客', 'age':'4', 'skill':'Python'}
gog = {'name':u'天天','age':123, 'skill':'createanything', 'other':u'哈哈'}
godslaver = {'name':u'雨来', 'age':'unknown','other':u'嘻嘻'}
post_info.insert(jike)

print (u'操作数据库完成!')