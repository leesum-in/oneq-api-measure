#!/usr/bin/env python

import sqlite3
import time
import requests

def measureTime(apiList):
    timeArray = []
    
    for i in apiList :
        time = requests.get('http://oneq.nhnent.com'+i[0]).elapsed
        second = time.seconds
        microsecond = time.microseconds
        milisecond = second*1000 + microsecond/1000.0
        apiTime = [i, milisecond]
        timeArray.append(apiTime)
    
    return timeArray

if __name__ == "__main__":
    apiList = [
        '/',
        '/question/create',
        '/api/question',
        '/api/question/1',
#        '/api/tag/tagName',
#        '/my/question/post-count',
#        '/my/quesion/write-count',
#        '/my/quesion/vote-count'
    ]

    timeArray = measureTime(apiList)
    now = time.localtime()
    todayStr = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    timeStr = "%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)
    
    conn = sqlite3.connect('/home1/irteam/apps/oneq-api-measure/db_api')
    cursor = conn.cursor()
    insertQuery = 'INSERT INTO tb_api_time VALUES (?,?,?,?)'
    values = []    
    for i in timeArray :
        uri = i[0]
        elapsed = i[1]
        value = (todayStr, timeStr, uri, elapsed)
        values.append(value)
    
    cursor.executemany(insertQuery, values)
    cursor.close()
    conn.commit()
