# -*- coding: utf-8 -*- 

import json
import redis
import logging
import MySQLdb

import context
import statistic

if __name__ == "__main__":
    # 初始化全局对象
    ctx = context.Context()

    while (True):
        try:
            rds = ctx.GetRedis()

            # 侦听统计消息
            m = rds.brpop(RDS_KEY_STATISTIC_MQ, 0)

            # 解析统计消息
            data = json.loads(m)
            if not data.has_key("id"):
                logging.error("Get data type failed! m:%s" % m)
                continue

            # 判断消息类型
            if data["id"] == statistic.DATA_TYPE_WATCH_VIDEO: # 观看视频统计
                if data.has_key("data"):
                    code, message = statistic.WatchVideoHandler(ctx, json.loads(data["data"]))
                    if errno.OK != code:
                        logging.error("Watch video handler failed! code:%d errmsg:%s" % (code, message))
                    continue
                logging.error("Get message data failed! m:%s" % m)
                continue
            logging.error("Unknown data type! m:%s" % m)
        except Exception, e:
            logging.error("Catch exception! e:%s" % str(e))

    print("Call main")
