# -*- coding: utf-8 -*- 

import sys
import json
import redis
import logging
import MySQLdb

import keys
import context
import statistic

if __name__ == "__main__":
    # 初始化全局对象
    ctx = context.Context()

    while (True):
        try:
            rds = ctx.GetRedis()

            print(rds)

            # 侦听统计消息
            m = rds.brpop(keys.RDS_KEY_STATISTIC_MQ, 0)

            # 解析统计消息
            data = json.loads(m)
            if not data.has_key("id"):
                logging.error("[%s][%d] Get data type failed! m:%s" 
                        % (__file__, sys._getframe().f_lineno, m))
                continue
            exit(0)

            # 判断消息类型
            if data["id"] == statistic.DATA_TYPE_WATCH_VIDEO: # 观看视频统计
                if data.has_key("data"):
                    (code, message) = statistic.WatchVideoHandler(ctx, json.loads(data["data"]))
                    if comm.OK != code:
                        logging.error("[%s][%d] Watch video handler failed! code:%d errmsg:%s" 
                                % (__file__, sys._getframe().f_lineno, code, message))
                    continue
                logging.error("[%s][%d] Get message data failed! m:%s"
                        % (__file__, sys._getframe().f_lineno, m))
                continue
            logging.error("[%s][%d] Unknown data type! m:%s"
                    % (__file__, sys._getframe().f_lineno, m))
        except Exception, e:
            logging.error("[%s][%d] Catch exception! e:%s" 
                    % (__file__, sys._getframe().f_lineno, str(e)))

    print("Call main")
