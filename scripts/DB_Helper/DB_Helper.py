#!/usr/bin/env python3
# -- coding: utf8 --

import pymysql
import config

g_db_connection = None

def checkConn(conn):
    sq = "SELECT NOW()"
    try:
        with conn.cursor() as cur:
            cur.execute( sq )
            conn.commit()
    except Exception as e:
        return False
    return True

def get_db_conn():
    global g_db_connection
    if g_db_connection is None or not checkConn(g_db_connection):
        g_db_connection = pymysql.connect(host=config.DATABASE['host'], port=config.DATABASE['port'], user=config.DATABASE['user'], password=config.DATABASE['password'], db=config.DATABASE['db'], cursorclass=pymysql.cursors.DictCursor, charset='utf8')
    return g_db_connection

get_db_conn()