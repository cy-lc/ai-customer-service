import hashlib
text='学习ai应用开发'
hash_value=hashlib.md5(text.encode('utf-8'))#生成md5对象
print(hash_value)
hash_value1=hashlib.md5(text.encode('utf-8')).hexdigest()  
print(hash_value1)
