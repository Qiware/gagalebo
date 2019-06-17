# -*- coding: utf-8 -*- 

import time
import nltk
import json
import logging

import keys
import errno

class Video():
    def __init__(self):
        name_en = ""        # 英文名称
        name_ch = ""        # 中文名称
        poster = ""         # 缩略图URL
        duration = ""       # 视频长度(秒)
        url = ""            # 播放地址
        words_script = ""   # 字幕
        definition = "360p" # 字幕

################################################################################
# 获取视频信息
# @param
#   v: 视频数据(表: video对象)
# @return
#   code: 错误码
#   message: 错误描述
def AnalyzeWordScript(ctx, v):
    try:
        m = dict({})
        sentences = ctx.tokenizer.tokenize(v.words_script)
        for idx, sentence in enumerate(sentences):
            words = ntk.tokenize.WordPunctTokenizer().tokenize(sentence)
            for idx, word  in enumerate(words):
                if m.has_key(word):
                    m[word] += 1
                else:
                    m[word] = 1
        v.words = json.dumps(m)
        return (errno.OK, "Ok")
    except Exception as e:
        loggin.error("Analyze word script failed! e:%s" % str(e))
        return (errno.ERR_UNKNOWN, "Analyze word script failed!")
    return (errno.ERR_UNKNOWN, "Analyze word script failed!")

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
        VALUES(%s, %s, %s, %d, %s, %s, %s, %s)''' % (v.name_en, v.name_ch, v.poster, v.duration, v.url, v.words_script, v.words, v.definition)

    try:
        cur.execute(sql) 

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


