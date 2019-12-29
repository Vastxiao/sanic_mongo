# sanic_mongo

sanic的mongodb异步工具，这个是基于[sanic-mongo](https://github.com/Sanic-Extensions/sanic-mongo)代码修改的。

## 用法：

```python
from sanic import Sanic
from sanic_mongo import MongoClient

app = Sanic()

# 1.初始化mongodb客户端：
#   第一个参数为 app实例
#   从第二个参数开始，可以跟多个键值（Mongo数据库标识名=Mongodb_URI）
MongoClient.SetConfig(
    app,
    name_1="mongodb://127.0.0.1:27017/db1",
    db_name2="mongodb://root:pass@192.168.62.195:27017/db_name2?authSource=admin"
)
MongoClient(app)
# 经过 MongoClient() 初始化后的 app 实例会生成一些属性:
#   app.config.MONGO_URIS 为一个字典 {"Mongo数据库标识名": "Mongodb_URI"}
#   app.MONGO_URIS = app.config.MONGO_URIS
#   app.extensions['SanicMongo'] 内容为 MongoClient实例化的对象
#   app.mongo 为一个字典 {'Mongo数据库标识名': MongoConnection客户端实例}


# 2.mongodb数据库的使用：
# 对于 app.mongo 中的每个MongoConnection都有以下属性
#   app.mongo['Mongo数据库标识名'].uri
#   app.mongo['Mongo数据库标识名'].client 这个是 AsyncIOMotorClient 创建的mongo客户端链接实例
#   app.mongo['Mongo数据库标识名'].db 这个是连上数据库时的db名称
# 所有的数据crud用法，都是使用motor的用法
#   https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html
cursor = app.mongo['name_1'].db.collection_name.find({'id': 123}).limit(50)
result_list = await cursor.to_list(length=50)
```