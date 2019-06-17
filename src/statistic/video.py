# -*- coding: utf-8 -*- 

import time
import logging

import keys
import errno

################################################################################
# 获取视频信息
# @param[in]
#   ctx: 全局对象
#   video_id: 视频ID
# @return
#   data: 视频数据(表: video对象)
#   code: 错误码
#   message: 错误描述
def GetVideoData(ctx, video_id):
    db = ctx.GetDbConn()
    cur = db.cursor()

    sql = "SELECT * FROM video WHERE id='%d'" % (video_id)

    try:
        cur.execute(sql) 

        data = cur.fetchone()

        cur.close()
        db.close()

        return (data, errno.OK, "Ok")
    except Exception, e:
        cur.close()
        db.close()
        logging.error("Get data failed! video id:%d errmsg:%s" % (video_id, str(e)))
        return (None, errno.ERR_UNKNOWN, str(e))
    return (None, errno.ERR_DATA_NOT_FOUND, "Get video data failed")

################################################################################
# 更新视频历史
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
#   video_id: 视频ID
# @return
#   code: 错误码
#   message: 错误描述
def UpdateVideoHistory(ctx, uid, video_id):
    try:
        rds = ctx.GetRedis()

        key = keys.RDS_KEY_USER_VIDEO_HISTORY % (uid)

        rds.zset(key, video_id, int(time.time()))

        return (errno.OK, "Ok")
    except Exception, e:
        logging.error("Update video history failed! uid:%d video_id:%d e:%s" % (uid, video_id, str(e)))
        return (errno.ERR_UNKNOWN, str(e))
    return (errno.ERR_UNKNOWN, "Update video history failed")

################################################################################
# 获取用户累计学习视频数量(REDIS)
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
# @return
#   count: 视频数量
#   code: 错误码
#   message: 错误描述
def GetVideoCountFromRds(ctx, uid):
    key = keys.RDS_KEY_USER_VIDEO_HISTORY % (uid)

    try:
        rds = ctx.GetRedis()

        count = rds.zcard(key)

        return (count, errno.OK, "Ok")
    except Exception, e:
        logging.error("Get video count from redis failed! uid:%d e:%s" % (uid, str(e)))
        return (0, errno.ERR_UNKNOWN, str(e))
    return (0, errno.ERR_UNKNOWN, "Get video count from redis failed!")
