# -*- coding: utf-8 -*- 

import json
import redis
import logging

# REDIS配置信息
REDIS_HOST = "10.11.178.43"
REDIS_PORT = 6379
REDIS_PASSWD = "12345678"
REDIS_DB = 0

# |LIST|统计信息消息队列
RDS_KEY_STATISTIC_MQ = "rds:key:statistic:mq"

class Context():
    # 初始化
    def __init__(self):
        # 构建REDIS连接池
        self.rds_pool = redis.ConnectionPool(
                host=REDIS_HOST,
                password=REDIS_PASSWD,
                port=REDIS_PORT,
                db=REDIS_DB);

    # 获取一个Redis连接
    def GetRedis(self):
        return redis.Redis(connection_pool = self.rds_pool)
    # 获取一个DB连接
    def GetDbConn(self):
        return self.db_pool.connection()

if __name__ == "__main__":
    ctx = Context()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

    rds = ctx.GetRedis()

    print(rds)

    data = "{\"uid\":10000, \"video_id\":1,\"play_time\":154328812}"

    m = {}
    m["id"] = 1
    m["data"] = data

    # 发送数据
    rds.lpush(RDS_KEY_STATISTIC_MQ, json.dumps(m))

    print(json.dumps(m))
