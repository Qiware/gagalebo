# -*- coding: utf-8 -*- 

import sys
import comm
import json
import logging

import word
import video
import account

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
            logging.error("[%s][%d] Get uid failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (comm.ERR_UID_INVALID, "Uid is invalid")

        if not data.has_key("video_id"):
            logging.error("[%s][%d] Get video id failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (comm.ERR_VIDEO_ID_INVALID, "Video id is invalid")

        if not data.has_key("play_time"):
            logging.error("[%s][%d] Get video play time failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (comm.ERR_VIDEO_ID_INVALID, "Video play time is invalid")

        # 获取视频信息
        (vdata, code, message) = video.GetVideoData(ctx, data["video_id"])
        if vdata is None:
            logging.error("[%s][%d] Get video data failed! video id:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, data["video_id"], code, message))
            return (code, message)

        # 更新观看视频历史
        (code, message) = video.UpdateVideoHistory(ctx, data["uid"], data["video_id"], data["play_time"])
        if comm.OK != code:
            logging.error("[%s][%d] Update video history failed! video id:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, data["video_id"], code, message))
            return (code, message)

        # 更新学习天数
        (code, message) = AddStudyDate(ctx, data["play_time"])
        if comm.OK != code:
            logging.error("[%s][%d] Update study days failed! video id:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, data["video_id"], code, message))
            return (code, message)

        # 更新单词学习统计
        (code, message) = UpdateWordCount(ctx, data["uid"], vdata)
        if comm.OK != code:
            logging.error("[%s][%d] Update word count failed! uid:%d video id:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, data["uid"], data["video_id"], code, message))
            return (code, message)

        # 更新统计信息表
        (code, message) = UpdateStatistic(ctx, data["uid"], vdata[comm.TAB_VIDEO_COL_DURATION])
        if comm.OK != code:
            logging.error("[%s][%d] Update statistic table failed! uid:%d video id:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, data["uid"], data["video_id"], code, message))
            return (code, message)

        return (comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Watch video handler failed! e:%s"
                % (__file__, sys._getframe().f_lineno, str(e)))
        return (comm.ERR_UNKNOWN, str(e))

    return (comm.ERR_UNKNOWN, "Watch video handler failed")

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
        words = json.loads(vdata[comm.TAB_VIDEO_COL_WORDS])

        # 更新各单词学习统计次数
        for key in words.keys():
            num = words[key]
            (code, message) = word.UpdateWordHistory(ctx, uid, key, num)
            if comm.OK != code:
                logging.error("[%s][%d] Update word history failed! uid:%d word:%s code:%d errmsg:%s"
                        % (__file__, sys._getframe().f_lineno, uid, word, code, message))
                return (code, message)

        return (comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Update word count failed! uid:%d vdata:%s e:%s"
                % (__file__, sys._getframe().f_lineno, uid, vdata, str(e)))
        return (comm.ERR_UNKNOWN, str(e))

    return (comm.ERR_UNKNOWN, "Update word count failed")

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
        # 获取账号信息
        (user, code, message) = account.GetAccountData(ctx, uid)
        if comm.OK != code:
            logging.error("[%s][%d] Get user failed! uid:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, uid, code, message))
            return (code, message)

        # 获取累计学习视频数量
        (video_count, code, message) = video.GetVideoCountFromRds(ctx, uid)
        if comm.OK != code:
            logging.error("[%s][%d] Get video count from redis failed! uid:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, uid, code, message))
            return (code, message)

        # 获取累计学习单词数量
        (word_count, code, message) = word.GetWordCountFromRds(ctx, uid)
        if comm.OK != code:
            logging.error("[%s][%d] Get word count from redis failed! uid:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, uid, code, message))
            return (code, message)

        # 获取累计学习天数
        (days, code, message) = GetStudyDaysFromRds(ctx, uid)
        if comm.OK != code:
            logging.error("[%s][%d] Get days from redis failed! uid:%d code:%d errmsg:%s"
                    % (__file__, sys._getframe().f_lineno, uid, code, message))
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
                sql ='''
                    INSERT INTO
                        statistic(uid, time, videos, words, days, score)
                    VALUES(%d, %d, %d, %d, %d)''' % (uid, 0, 0, 0, 0, 0)

                cur.execute(sql) 

                db.commit()

                cur.close()
                db.close()
                continue

            print('s:', s)

            # 更新统计信息
            total_tm = s[comm.TAB_STATISTIC_COL_TIME] + duration
            score = int((tm / days) * user[comm.TAB_ACCOUNT_COL_TIME_SETTING])

            sql = '''
                UPDATE statistic
                SET time=%d, videos=%d, words=%d, days=%d, score=%d
                WHERE uid=%d''' % (total_tm, video_count, word_count, days, score, uid)

            cur.execute(sql) 
            db.commit()

            cur.close()
            db.close()

            return (comm.OK, "Ok")
    except Exception, e:
       logging.error("[%s][%d] Get data failed! uid:%d e:%s"
               % (__file__, sys._getframe().f_lineno, uid, str(e)))
       return (comm.ERR_UNKNOWN, str(e))

################################################################################
# 添加学习日期
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
#   tm: 观看视频时间戳
# @return
#   code: 错误码
#   message: 错误描述
def AddStudyDate(ctx, uid, tm):

    key = keys.RDS_KEY_USER_STUDY_DATE_SET % (uid)

    try:
        rds = ctx.GetRedis()

        date = tm - tm%86400

        rds.sadd(key, date)

        return (comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Update study days failed! uid:%d word:%s e:%s"
                % (__file__, sys._getframe().f_lineno, uid, word, str(e)))
        return (comm.ERR_UNKNOWN, str(e))

    return (comm.ERR_UNKNOWN, "Update word history failed")

################################################################################
# 获取用户累计学习天数
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
# @return
#   days: 学习天数
#   code: 错误码
#   message: 错误描述
def GetStudyDaysFromRds(ctx, uid):

    key = keys.RDS_KEY_USER_STUDY_DATE_SET % (uid)

    try:
        rds = ctx.GetRedis()

        days = rds.scard(key)

        return (days, comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Get study days from redis failed! uid:%d e:%s"
                % (__file__, sys._getframe().f_lineno, uid, str(e)))
        return (0, comm.ERR_UNKNOWN, str(e))

    return (0, comm.ERR_UNKNOWN, "Get study days from redis failed")
