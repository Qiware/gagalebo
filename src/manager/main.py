# -*- coding: utf-8 -*- 

# 引用通用组件
import sys
import json
import redis
import logging
import MySQLdb
from flask import Flask,request,render_template

# 引用自定义模块
import comm
import word
import video
import context

################################################################################
logging.basicConfig(
        level=logging.DEBUG,
        filename='manager.log',
        format='%(asctime)s : %(levelname)s : %(message)s')


# 初始化全局对象
ctx = context.Context()

app = Flask(__name__)

################################################################################
# 返回应答数据
# @param
#   code: 返回码
#   message: 错误描述
# @return
#   data: 应答的JSON格式数据
def GenResponse(code, message):
    m = {}

    m["code"] = code
    m["message"] = message

    return json.dumps(m)

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
    try:
        # 提取输入参数
        data = request.get_data()

        (v, code, message) = ParseCreateVideoParam(data)
        if comm.OK != code:
            logging.error("[%s][%d] Parse create video parameter failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return GenResponse(code, message)

        # 分析字幕信息
        (w, code, message) = word.StatisticWord(ctx, v.words_script)
        if comm.OK != code:
            logging.error("[%s][%d] Analyze word script failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return GenResponse(code, message)

        v.words = json.dumps(w)

        # 更新单词库资源
        for key in w.keys():
            (code, message) = word.AddWord(ctx, key, 0, "")
            if comm.OK != code:
                logging.error("[%s][%d] Add word failed! code:%d message:%s"
                        % (__file__, sys._getframe().f_lineno, code, message))
                return GenResponse(code, message)

        # 新建视频资源
        (vid, code, message) = video.CreateVideo(ctx, v)
        if comm.OK != code:
            logging.error("[%s][%d] Create video failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return GenResponse(code, message)

        # 更新视频ID集合
        (code, message) = video.AddVideoSet(ctx, vid)
        if comm.OK != code:
            logging.error("[%s][%d] Add video set failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return GenResponse(code, message)
        return GenResponse(comm.OK, "Ok")
    except Exception as e:
        logging.error("[%s][%d] Create video failed! e:%s"
                % (__file__, sys._getframe().f_lineno, str(e)))
        return GenResponse(comm.ERR_UNKNOWN, str(e))

################################################################################
# 更新视频资源
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
@app.route("/gagalebo/v1/video/<int:video_id>", methods=['PUT'])
def UpdateVideo(video_id):
    try:
        # 提取输入参数
        data = request.get_data()

        (v, code, message) = ParseCreateVideoParam(data)
        if comm.OK != code:
            logging.error("[%s][%d] Parse create video parameter failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return GenResponse(code, message)

        # 分析字幕信息
        (w, code, message) = word.StatisticWord(ctx, v.words_script)
        if comm.OK != code:
            logging.error("[%s][%d] Analyze word script failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return GenResponse(code, message)
        v.words = json.dumps(w)

        # 更新视频资源
        (code, message) = video.UpdateVideo(ctx, video_id, v)
        if comm.OK != code:
            logging.error("[%s][%d] Update video failed! code:%d message:%s"
                    % (__file__, sys._getframe().f_lineno, code, message))
            return GenResponse(code, message)
        return GenResponse(comm.OK, "Ok")
    except Exception as e:
        logging.error("[%s][%d] Update video failed! e:%s"
                % (__file__, sys._getframe().f_lineno, str(e)))
        return GenResponse(comm.ERR_UNKNOWN, str(e))

# 解析创建视频的参数
# @param
#   data: 视频信息
# @return
#   code: 错误码
#   message: 错误描述
def ParseCreateVideoParam(data):
    v = video.Video()

    try:
        jdata = json.loads(data)

        # 校验参数合法性
        # 英文名称
        if not jdata.has_key("name_en") or (0 == len(jdata["name_en"])):
            logging.error("[%s][%d] Get name_en failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, comm.ERR_PARAM_INVALID, "Get name_en failed!")

        v.name_en = jdata["name_en"]

        # 中文名称
        if not jdata.has_key("name_ch") or (0 == len(jdata["name_ch"])):
            logging.error("[%s][%d] Get name_ch failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, comm.ERR_PARAM_INVALID, "Get name_ch failed!")

        v.name_ch = jdata["name_ch"]

        # 缩略图URL
        if not jdata.has_key("poster") or (0 == len(jdata["poster"])):
            logging.error("[%s][%d] Get poster failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, comm.ERR_PARAM_INVALID, "Get poster failed!")

        v.poster = jdata["poster"]

        # 视频时长(秒)
        if not jdata.has_key("duration") or (0 == jdata["duration"]):
            logging.error("[%s][%d] Get duration failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, comm.ERR_PARAM_INVALID, "Get duration failed!")

        v.duration = jdata["duration"]

        # 播放地址
        if not jdata.has_key("url") or (0 == len(jdata["url"])):
            logging.error("[%s][%d] Get url failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, comm.ERR_PARAM_INVALID, "Get url failed!")

        v.url = jdata["url"]

        # 字幕内容
        if not jdata.has_key("words_script") or (0 == len(jdata["words_script"])):
            logging.error("[%s][%d] Get words_script failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, comm.ERR_PARAM_INVALID, "Get words_script failed!")

        v.words_script = jdata["words_script"]

        # 视频清晰度
        if not jdata.has_key("definition") or (0 == len(jdata["definition"])):
            logging.error("[%s][%d] Get definition failed! data:%s"
                    % (__file__, sys._getframe().f_lineno, data))
            return (None, comm.ERR_PARAM_INVALID, "Get definition failed!")

        v.definition = jdata["definition"]

        return (v, comm.OK, "Ok")
    except Exception as e:
        logging.error("[%s][%d] Create video failed! data:%s e:%s"
                % (__file__, sys._getframe().f_lineno, data, str(e)))
        return (None, comm.ERR_UNKNOWN, str(e))
    return (None, comm.ERR_UNKNOWN, "Parse create video parameter failed!")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
