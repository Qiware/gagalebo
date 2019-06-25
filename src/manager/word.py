# -*- coding: utf-8 -*- 

import sys
import nltk
import logging

import comm

################################################################################
# 增加新的单词
# @param
#   ctx: 全局对象
#   word: 单词
#   level: 难度系数(1,2,3,4...)
#   description: 描述信息
# @return
#   code: 错误码
#   message: 错误描述
def AddWord(ctx, word, level, description):
    db = ctx.GetDbConn()
    cur = db.cursor()

    sql = '''
        INSERT INTO
            word(word, level, description)
        VALUES('%s', %d, '%s')''' % (word, level, description)

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
        logging.error("[%s][%d] Add word failed! word:%s level:%d description:%s errmsg:%s"
                % (__file__, sys._getframe().f_lineno, word, level, description, str(e)))
        if comm.MYSQL_ERR_DUP_KEY == e[0]:
            return (comm.OK, "Ok")
        return (comm.ERR_UNKNOWN, str(e))
    return (comm.ERR_DATA_NOT_FOUND, "Add word failed")



################################################################################
# 统计段落中的各单词数
# @param
#   ctx: 全局对象
#   paragraph: 英文段落
# @return
#   code: 错误码
#   message: 错误描述
def StatisticWord(ctx, paragraph):
    try:
        m = {}
        sentences = ctx.tokenizer.tokenize(paragraph)
        for idx, sentence in enumerate(sentences):
            words = nltk.tokenize.WordPunctTokenizer().tokenize(sentence)
            for word  in words:
                if not word.isalpha():
                    # 单词中存在'非字母'的字符, 判定为非法单词.
                    continue
                word = word.lower()
                if m.has_key(word):
                    m[word] += 1
                else:
                    m[word] = 1
        return (m, comm.OK, "Ok")
    except Exception as e:
        logging.error("[%s][%d] Analyze word script failed! e:%s"
                % (__file__, sys._getframe().f_lineno, str(e)))
        return (None, comm.ERR_UNKNOWN, "Analyze word script failed!")
    return (None, comm.ERR_UNKNOWN, "Analyze word script failed!")
