from qiniu import Auth, put_file, etag

from config import QINIU_ACCESS_KEY, QINIU_SECRET_KEY

# 构建鉴权对象
q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
# 要上传的空间
bucket_name = 'corley-images'
# 上传后保存的文件名
key = 'logo.png'
# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
# 要上传文件的本地路径
localfile = 'E:\Test\logo.gif'
ret, info = put_file(token, key, localfile)
print('ret :', ret)
print('info:', info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)
