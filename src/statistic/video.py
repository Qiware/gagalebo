# -*- coding: utf-8 -*- 

import time
import logging

import keys
import comm

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

        return (data, comm.OK, "Ok")
    except Exception, e:
        cur.close()
        db.close()
        logging.error("[%s][%d] Get data failed! video id:%d errmsg:%s"
                % (__file__, sys._getframe().f_lineno, video_id, str(e)))
        return (None, comm.ERR_UNKNOWN, str(e))
    return (None, comm.ERR_DATA_NOT_FOUND, "Get video data failed")

################################################################################
# 更新视频历史
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
#   video_id: 视频ID
#   play_time: 视频播放时间
# @return
#   code: 错误码
#   message: 错误描述
def UpdateVideoHistory(ctx, uid, video_id, play_time):
    try:
        rds = ctx.GetRedis()

        key = keys.RDS_KEY_USER_VIDEO_HISTORY % (uid)

        rds.zset(key, video_id, play_time)

        return (comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Update video history failed! uid:%d video_id:%d play_time:%d e:%s"
                % (__file__, sys._getframe().f_lineno, uid, video_id, play_time, str(e)))
        return (comm.ERR_UNKNOWN, str(e))
    return (comm.ERR_UNKNOWN, "Update video history failed")

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

        return (count, comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Get video count from redis failed! uid:%d e:%s"
                % (__file__, sys._getframe().f_lineno, uid, str(e)))
        return (0, comm.ERR_UNKNOWN, str(e))
    return (0, comm.ERR_UNKNOWN, "Get video count from redis failed!")
