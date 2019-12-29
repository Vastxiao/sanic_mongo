# -*- coding: utf-8 -*-

"""
@Author: Huang Sizhe <huangsizhe>
@Date:   08-Apr-2017
@Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
@License: Apache License 2.0
@Description:
"""

__all__ = ["Core"]

from sanic.log import logger as log

from .standalone import MongoConnection


class Core:

    @staticmethod
    def SetConfig(app, **confs):
        """
        初始化设置Mongodb配置

        :param app: sanic的app实例
        :param confs:  键值对为  Mongo数据库标识名=Mongodb_URI
        :return:  返回app
        """
        app.config.MONGO_URIS = confs
        return app

    def __init__(self, app=None):
        self.mongodbs = {}
        if app:
            self.init_app(app)
        else:
            pass

    def init_app(self, app):
        """绑定app
        为Mongo客户端初始化绑定sanic app

        初始化后:
            添加 app.extensions['SanicMongo'] = self
            添加 app.mongo 为 {'自定义的motor_client名称标识': MongoConnection客户端实例}

        返回 self
        """
        if app.config.MONGO_URIS and isinstance(app.config.MONGO_URIS, dict):
            self.MONGO_URIS = app.config.MONGO_URIS
            self.app = app

        else:
            raise ValueError(
                "nonstandard sanic config MONGO_URIS,MONGO_URIS must be a Dict[dbname,dburl]")


        @app.listener("before_server_start")
        async def init_mongo_connection(app, loop):
            for motor_name, dburl in app.config.MONGO_URIS.items():
                if isinstance(dburl, str):
                    #db = MongoConnection(dburl, ioloop=loop).db
                    mongo_connection = MongoConnection(dburl, ioloop=loop)
                else:
                    #db = MongoConnection(ioloop=loop, **dburl).db
                    mongo_connection = MongoConnection(ioloop=loop, **dburl)
                #self.mongodbs[motor_name] = db
                self.mongodbs[motor_name] = mongo_connection
            log.info("初始化 mongo connection {numbr}".format(numbr=len(self.mongodbs)))

        @app.listener("before_server_stop")
        async def sub_close(app, loop):
            log.info("mongo connection {numbr}".format(numbr=len(self.mongodbs)))
            for motor_name, mongo_connection in self.mongodbs.items():
                mongo_connection.client.close
                log.info("{motor_name} connection closed".format(motor_name=motor_name))

        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicMongo'] = self

        app.mongo = self.mongodbs
        return self
