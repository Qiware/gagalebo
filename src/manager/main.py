# -*- coding: utf-8 -*- 

# 引用通用组件
import sys
import json
import redis
import logging
import MySQLdb
from flask import Flask,request,render_template

# 引用自定义模块
import video
import errno
import context

################################################################################
# 初始化全局对象
ctx = context.Context()

app = Flask(__name__)

################################################################################
# 新建视频资源
# @protocol
# {
#   "name_en": "$name_en",              // 英文名称
#   "name_ch": "$name_ch",              // 中文名称
#   "poster": "$poster",                // 缩略图URL
#   "duration": $duration,              // 视频时长
#   "url": "$url",                      // 视频播放地址
#   "words_script": "$words_script",    // 字幕
#   "definition": "$definition",        // 视频清晰度(ex: 360p, 480p, 720p, 1080p...)
# }
@app.route("/gagalebo/v1/video", methods=['POST'])
def CreateVideo():
    v = video.Video()

    try:
        # 提取输入参数
        data = request.get_data()

        (v, code, message) = ParseCreateVideoParam(data)
        if errno.OK != code:
            logging.error("[%s][%d] Parse create video parameter failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return message


        # 分析字幕信息
        (w, code, message) = word.StatisticWord(ctx, v.words_script)
        if errno.OK != code:
            logging.error("[%s][%d] Analyze word script failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return message
        v.words = json.dumps(w)

        # 新建视频资源
        (code, message) = video.CreateVideo(v)
        if errno.OK != code:
            logging.error("[%s][%d] Create video failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return message
        return "Ok"
    except Exception as e:
        logging.error("[%s][%d] Create video failed! e:%s"
                % (__file__, sys._getframe().f_lineno, str(e)))
        return str(e)

# 解析创建视频的参数
# @param
#   data: 视频信息
# @return
#   code: 错误码
#   message: 错误描述
def ParseCreateVideoParam(data):
    try:
        jdata = json.loads(data)

        # 校验参数合法性
        # 英文名称
        if not jdata.has_key("name_en") or (0 == len(jdata["name_en"])):
            logging.error("[%s][%d] Get name_en failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, errno.ERR_PARAM_INVALID, "Get name_en failed!")

        v.name_en = jdata["name_en"]

        # 中文名称
        if not jdata.has_key("name_ch") or (0 == len(jdata["name_ch"])):
            logging.error("[%s][%d] Get name_ch failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, errno.ERR_PARAM_INVALID, "Get name_ch failed!")

        v.name_en = jdata["name_ch"]

        # 缩略图URL
        if not jdata.has_key("poster") or (0 == len(jdata["poster"])):
            logging.error("[%s][%d] Get poster failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, errno.ERR_PARAM_INVALID, "Get poster failed!")

        v.poster = jdata["poster"]

        # 视频时长(秒)
        if not jdata.has_key("duration") or (0 == jdata["duration"]):
            logging.error("[%s][%d] Get duration failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, errno.ERR_PARAM_INVALID, "Get duration failed!")

        v.duration = jdata["duration"]

        # 播放地址
        if not jdata.has_key("url") or (0 == len(jdata["url"])):
            logging.error("[%s][%d] Get url failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, errno.ERR_PARAM_INVALID, "Get url failed!")

        v.url = jdata["url"]

        # 字幕内容
        if not jdata.has_key("words_script") or (0 == len(jdata["words_script"])):
            logging.error("[%s][%d] Get words_script failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, errno.ERR_PARAM_INVALID, "Get words_script failed!")

        v.words_script = jdata["words_script"]

        # 视频清晰度
        if not jdata.has_key("definition") or (0 == len(jdata["definition"])):
            logging.error("[%s][%d] Get definition failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, errno.ERR_PARAM_INVALID, "Get definition failed!")

        v.definition = jdata["definition"]

        return (v, errno.OK, "Ok")
    except Exception as e:
        logging.error("[%s][%d] Create video failed! e:%s"
                % (__file__, sys._getframe().f_lineno, str(e)))
        return (None, errno.ERR_UNKNOWN, str(e))
    return (None, errno.ERR_UNKNOWN, "Parse create video parameter failed!")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
