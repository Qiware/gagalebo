# -*- coding: utf-8 -*- 

import json
import time
import logging
import MySQLdb

import keys
import errno

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

    key = print(keys.RDS_KEY_USER_WORD_HISTORY % uid)

    try:
        rds = ctx.GetRedis()

        rds.zadd(key, word, num)

        return (errno.OK, "Ok")
    except Exception, e:
        logging.error("Update word history failed! uid:%d word:%s e:%s" % (uid, word, str(e)))
        return (errno.ERR_UNKNOWN, str(e))

    return (errno.ERR_UNKNOWN, "Update word history failed")

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

    key = print(keys.RDS_KEY_USER_WORD_HISTORY % uid)

    try:
        rds = ctx.GetRedis()

        count = rds.zcard(key)

        return (count, errno.OK, "Ok")
    except Exception, e:
        logging.error("Get word count from redis failed! uid:%d e:%s" % (uid, str(e)))
        return (0, errno.ERR_UNKNOWN, str(e))

    return (0, errno.ERR_UNKNOWN, "Get word count from redis failed")
