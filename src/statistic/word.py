# -*- coding: utf-8 -*- 

import sys
import json
import time
import logging
import MySQLdb

import comm
import keys

################################################################################
# 更新单词学习
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
#   word: 单词
#   num: 新增学习次数
# @return
#   code: 错误码
#   message: 错误描述
def UpdateWordHistory(ctx, uid, word, num):

    key = keys.RDS_KEY_USER_WORD_HISTORY % (uid)

    try:
        rds = ctx.GetRedis()

        #rds.zadd(key, {word: num})
        rds.zincrby(key, word, num)

        return (comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Update word history failed! uid:%d word:%s e:%s"
                % (__file__, sys._getframe().f_lineno, uid, word, str(e)))
        return (comm.ERR_UNKNOWN, str(e))

    return (comm.ERR_UNKNOWN, "Update word history failed")

################################################################################
# 获取用户累计学习单词数量(REDIS)
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
# @return
#   count: 学习单词数量
#   code: 错误码
#   message: 错误描述
def GetWordCountFromRds(ctx, uid):

    key = keys.RDS_KEY_USER_WORD_HISTORY % uid

    try:
        rds = ctx.GetRedis()

        count = rds.zcard(key)

        print("count", count)

        return (count, comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Get word count from redis failed! uid:%d e:%s"
                % (__file__, sys._getframe().f_lineno, uid, str(e)))
        return (0, comm.ERR_UNKNOWN, str(e))

    return (0, comm.ERR_UNKNOWN, "Get word count from redis failed")
