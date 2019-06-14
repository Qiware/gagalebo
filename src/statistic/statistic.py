# -*- coding: utf-8 -*- 

import json
import logging

import video

################################################################################
# 统计数据类型
DATA_TYPE_WATCH_VIDEO = 1 # 观看视频消息

################################################################################
# 观看视频的统计处理
# @param[in]
#   rds: REDIS对象
#   data: 消息内容(json解析后的map格式)
# @return
#   code: 错误码
#   message: 错误描述
def WatchVideoHandler(ctx, data):
    try:
        # 判断协议合法性
        if not data.has_key("uid"):
            logging.error("Get uid failed! data:%s" % data)
            return (errno.ERR_UID_INVALID, "Uid is invalid")

        if not data.has_key("video_id"):
            logging.error("Get video id failed! data:%s" % data)
            return (errno.ERR_VIDEO_ID_INVALID, "Video id is invalid")

        # 获取视频信息
        vdata, code, message = video.GetVideoData(ctx, data["video_id"])
        if vdata is None:
            logging.error("Get video data failed! video id:%d code:%d errmsg:%s" %
                    (data["video_id"], code, message))
            return (code, message)

        # 更新观看视频历史
        code, message = video.UpdateVideoHistory(ctx, data["uid"], data["video_id"])
        if errno.OK != code:
            logging.error("Update video history failed! video id:%d code:%d errmsg:%s" % 
                    (data["video_id"], code, message))
            return (code, message)

        # 更新单词学习统计
        code, message = UpdateWordCount(ctx, data["uid"], vdata)
        if errno.OK != code:
            logging.error("Update word count failed! uid:%d video id:%d code:%d errmsg:%s" % 
                    (data["uid"], data["video_id"], code, message))
            return (code, message)

        # 更新统计信息表
        code, message = UpdateStatistic(ctx, data["uid"], vdata["duration"])
        if errno.OK != code:
            logging.error("Update statistic table failed! uid:%d video id:%d code:%d errmsg:%s" % 
                    (data["uid"], data["video_id"], code, message))
            return (code, message)

        return (errno.OK, "Ok")
    except Exception, e:
        logging.error("Watch video handler failed! e:%s" % str(e))
        return (errno.ERR_UNKNOWN, str(e))

    return (errno.ERR_UNKNOWN, "Watch video handler failed")

################################################################################
# 更新视频中的各单词学习统计次数
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
#   vdata: 视频数据(表:video对象)
# @return
#   code: 错误码
#   message: 错误描述
def UpdateWordCount(ctx, uid, vdata):
    try:
        # 解析单词统计信息
        words = json.loads(vdata[TAB_VIDEO_COL_WORDS])

        # 更新各单词学习统计次数
        for word in words.keys():
            num = words[word]
            code, message = word.UpdateWordHistory(ctx, uid, word, num)
            if errno.OK != code:
                logging.error("Update word history failed! uid:%d word:%s code:%d errmsg:%s" % 
                        (uid, word, code, message))
                return (code, message)

        return (errno.OK, "Ok")
    except Exception, e:
        logging.error("Update word count failed! uid:%d vdata:%s e:%s" % (uid, vdata, str(e)))
        return (errno.ERR_UNKNOWN, str(e))

    return (errno.ERR_UNKNOWN, "Update word count failed")

################################################################################
# 更新统计信息表
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
#   duration: 新增学习时长
# @return
#   code: 错误码
#   message: 错误描述
def UpdateStatistic(ctx, uid, duration):
    try:
        # 获取累计学习视频数量
        video_count, code, message = video.GetVideoCountFromRds(ctx, uid)
        if errno.OK != code:
            logging.error("Get video count from redis failed! uid:%d code:%d errmsg:%s" %
                    (uid, code, message))
            return (code, message)

        # 获取累计学习单词数量
        word_count, code, message = video.GetWordCountFromRds(ctx, uid)
        if errno.OK != code:
            logging.error("Get word count from redis failed! uid:%d code:%d errmsg:%s" %
                    (uid, code, message))
            return (code, message)

        while (True):
            db = ctx.GetDbConn()
            cur = db.cursor()

            # 获取统计信息
            sql = "SELECT * FROM statistic WHERE uid='%d'" % (uid)

            cur.execute(sql) 

            s = cur.fetchone()
            if s is None:
                # 新建统计对象
                sql = "
                    INSERT INTO
                        statistic(uid, time, videos, words, score)
                    VALUES(%d, %d, %d, %d, %d)" % (uid, 0, 0, 0, 0)
                cur.execute(sql) 
                cur.commit()

                cur.close()
                db.close()
                continue

            # 更新统计信息
            s["time"] += duration
            s["videos"] = video_count
            s["words"] = word_count

            sql = "
                UPDATE statistic
                SET(time, videos, words)
                VALUES(%d, %d, %d) WHERE uid='%d'" % (s["time"], s["videos"], s["words"], uid)

            cur.execute(sql) 
            db.commit()

            cur.close()
            db.close()
            return (errno.OK, "Ok")
    except Exception, e:
       logging.error("Get data failed! video id:%d e:%s" % (video_id, str(e)))
       return (errno.ERR_UNKNOWN, str(e))
