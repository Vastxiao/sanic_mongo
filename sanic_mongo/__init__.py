# 源码来自: https://github.com/Sanic-Extensions/sanic-mongo

# @Author: Huang Sizhe
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
# @License: Apache License 2.0


__all__ = ["MongoClient", "GridFS"]


from .mongo import Core as MongoCore
from .gridfs import Core as GridFSCore


class MongoClient(MongoCore):
    pass

class GridFS(GridFSCore):
    pass

