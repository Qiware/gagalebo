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
#   code: 错误码
#   message: 错误描述
def CreateVideo(ctx, v):
    db = ctx.GetDbConn()
    cur = db.cursor()

    sql = '''
        INSERT INTO
            video(name_en, name_ch, poster, duration, url, words_script, words, definition)
        VALUES('%s', '%s', '%s', %d, '%s', '%s', '%s', '%s')''' % (v.name_en, v.name_ch, v.poster, v.duration, v.url, v.words_script, v.words, v.definition)

    logging.error("[%s][%d] sql:%s" % (__file__, sys._getframe().f_lineno, sql))

    try:
        cur.execute(sql) 

        db.commit()
        cur.close()
        db.close()

        return (comm.OK, "Ok")
    except Exception, e:
        cur.close()
        db.close()
        logging.error("[%s][%d] Create video data failed! name(en):%s errmsg:%s"
                % (__file__, sys._getframe().f_lineno, v.name_en, str(e)))
        return (comm.ERR_UNKNOWN, str(e))
    return (comm.ERR_DATA_NOT_FOUND, "Create video data failed")


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


