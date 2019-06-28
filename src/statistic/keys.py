# -*- coding: utf-8 -*- 

# REDIS-KEY定义

# |ZSET|记录用户的单词学习记录
RDS_KEY_USER_WORD_HISTORY = "rds:key:uid:%d:word:history"

# |ZSET|记录用户的视频学习记录
RDS_KEY_USER_VIDEO_HISTORY = "rds:key:uid:%d:video:history"

# |LIST|统计信息消息队列
RDS_KEY_STATISTIC_MQ = "rds:key:statistic:mq"

# |SET|学习日期时间戳集合
RDS_KEY_USER_STUDY_DATE_SET = "rds:key:uid:%d:study:date:set"
