# -*- coding: utf-8 -*- 

import nltk
import logging

import comm

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
