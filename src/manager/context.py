# -*- coding: utf-8 -*- 

import json
import nltk
import redis
import logging
import MySQLdb
from DBUtils.PooledDB import PooledDB, SharedDBConnection

# REDIS配置信息
#REDIS_HOST = "10.11.178.43"
#REDIS_HOST = "10.105.58.55"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWD = ""
REDIS_DB = 0

# MYSQL配置信息
#MYSQL_HOST = "10.105.58.55"
#MYSQL_HOST = "10.11.178.43"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
#MYSQL_USER = "useradmin"
#MYSQL_PASSWD = "adminpassword"
MYSQL_USER = "quack"
MYSQL_PASSWD = "sYyxUgeCXxS8@)!^"
MYSQL_DB = "quack"

class Context():
    # 初始化
    def __init__(self):
        # 构建REDIS连接池
        self.rds_pool = redis.ConnectionPool(
                host=REDIS_HOST,
                password=REDIS_PASSWD,
                port=REDIS_PORT,
                db=REDIS_DB);

        # 构建MYSQL连接池
        self.db_pool = PooledDB(
                creator = MySQLdb,  #使用链接数据库的模块
                maxconnections = 6, #连接池允许的最大连接数，0和None表示没有限制
                mincached = 2,      #初始化时，连接池至少创建的空闲的连接，0表示不创建
                maxcached = 5,      #连接池空闲的最多连接数，0和None表示没有限制
                maxshared = 3,      #连接池中最多共享的连接数量，0和None表示全部共享，ps:其实并没有什么用，因为pymsql和MySQLDB等模块中的threadsafety都为1，所有值无论设置多少，_maxcahed永远为0，所以永远是所有链接共享
                blocking = True,    #链接池中如果没有可用共享连接后,是否阻塞等待,True表示等待,False表示不等待然后报错
                setsession = [],    #开始会话前执行的命令列表
                ping = 0,           #ping Mysql 服务端 检查服务是否可用
                host = MYSQL_HOST,
                port = MYSQL_PORT,
                user = MYSQL_USER,
                passwd = MYSQL_PASSWD,
                db = MYSQL_DB,
                charset = 'utf8')

        # 构建NLTK上下文
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    # 获取一个Redis连接
    def GetRedis(self):
        return redis.Redis(connection_pool = self.rds_pool)
    # 获取一个DB连接
    def GetDbConn(self):
        return self.db_pool.connection()

