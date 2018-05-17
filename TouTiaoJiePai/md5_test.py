from hashlib import md5

user = 'jointwisdom'
pwd = 'zhonghui123'

m2 = md5()
m2.update(pwd.encode("utf-8"))#参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
print(m2.hexdigest())