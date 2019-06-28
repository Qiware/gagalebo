# -*- coding: utf-8 -*- 

import sys
import logging

import comm

################################################################################
# 获取账号信息
# @param[in]
#   ctx: 全局对象
#   uid: 用户ID
# @return
#   data: 账号数据(表: account对象)
#   code: 错误码
#   message: 错误描述
def GetAccountData(ctx, uid):
    db = ctx.GetDbConn()
    cur = db.cursor()

    sql = "SELECT * FROM account WHERE id='%d'" % (uid)

    try:
        cur.execute(sql) 

        data = cur.fetchone()

        db.commit()
        cur.close()
        db.close()

        return (data, comm.OK, "Ok")
    except Exception, e:
        cur.close()
        db.close()
        logging.error("[%s][%d] Get account data failed! uid:%d errmsg:%s"
                % (__file__, sys._getframe().f_lineno, uid, str(e)))
        return (None, comm.ERR_UNKNOWN, str(e))
    return (None, comm.ERR_DATA_NOT_FOUND, "Get account data failed")
