# -*- coding: utf-8 -*- 

import sys
import time
import nltk
import json
import logging

import keys
import comm

class Video():
    def __init__(self):
        self.name_en = ""        # 英文名称
        self.name_ch = ""        # 中文名称
        self.poster = ""         # 缩略图URL
        self.duration = ""       # 视频长度(秒)
        self.url = ""            # 播放地址
        self.words_script = ""   # 字幕
        self.definition = "360p" # 字幕

################################################################################
# 新建视频信息
# @param
#   ctx: 全局对象
#   v: 视频对象
# @return
#   id: 视频ID
#   code: 错误码
#   message: 错误描述
def CreateVideo(ctx, v):
    db = ctx.GetDbConn()
    cur = db.cursor()

    sql = '''
        INSERT INTO
            video(name_en, name_ch, poster, duration, url, words_script, words, definition)
        VALUES('%s', '%s', '%s', %d, '%s', '%s', '%s', '%s')''' % (v.name_en, v.name_ch, v.poster, v.duration, v.url, v.words_script, v.words, v.definition)

    logging.debug("[%s][%d] sql:%s" % (__file__, sys._getframe().f_lineno, sql))

    try:
        cur.execute(sql) 

	vid = cur.lastrowid

        db.commit()
        cur.close()
        db.close()

        return (vid, comm.OK, "Ok")
    except Exception, e:
        cur.close()
        db.close()
        logging.error("[%s][%d] Create video data failed! name(en):%s errmsg:%s"
                % (__file__, sys._getframe().f_lineno, v.name_en, str(e)))
        return (0, comm.ERR_UNKNOWN, str(e))
    return (0, comm.ERR_DATA_NOT_FOUND, "Create video data failed")

################################################################################
# 更新视频信息
# @param
#   ctx: 全局对象
#   v: 视频对象
# @return
#   code: 错误码
#   message: 错误描述
def UpdateVideo(ctx, video_id, v):
    db = ctx.GetDbConn()
    cur = db.cursor()

    sql = '''
        UPDATE
            video
        SET
            name_en='%s',
            name_ch='%s',
            poster='%s',
            duration=%d,
            url='%s',
            words_script='%s',
            words='%s',
            definition='%s'
        WHERE id=%d''' % (
            v.name_en, v.name_ch, v.poster, v.duration,
            v.url, v.words_script, v.words, v.definition, video_id)

    logging.debug("[%s][%d] sql:%s" % (__file__, sys._getframe().f_lineno, sql))

    try:
        cur.execute(sql) 

        db.commit()
        cur.close()
        db.close()

        return (comm.OK, "Ok")
    except Exception, e:
        cur.close()
        db.close()
        logging.error("[%s][%d] Update video data failed! name(en):%s errmsg:%s"
                % (__file__, sys._getframe().f_lineno, v.name_en, str(e)))
        return (comm.ERR_UNKNOWN, str(e))
    return (comm.ERR_DATA_NOT_FOUND, "Update video data failed")

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
# 将视频ID加入到集合(REDIS)
# @param[in]
#   ctx: 全局对象
#   vid: 视频ID
# @return
#   code: 错误码
#   message: 错误描述
def AddVideoSet(ctx, vid):
    key = keys.RDS_KEY_VIDEO_SET

    try:
        rds = ctx.GetRedis()

        rds.add(key, vid)

        return (comm.OK, "Ok")
    except Exception, e:
        logging.error("[%s][%d] Add video set failed! vid:%d e:%s"
                % (__file__, sys._getframe().f_lineno, vid, str(e)))
        return (comm.ERR_UNKNOWN, str(e))
    return (comm.ERR_UNKNOWN, "Add video set failed!")
