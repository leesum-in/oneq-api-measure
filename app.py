# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
import sqlite3
import math

app = Flask(__name__)

def selectQuery(uri):
    query = "SELECT *  FROM (SELECT sub.atDay as atDay, sub.a, AVG((tb_api_time.elapsed - sub.a)*(tb_api_time.elapsed - sub.a)) FROM tb_api_time, (SELECT atDay, AVG(tb_api_time.elapsed) as a FROM tb_api_time WHERE uri="+uri+" GROUP BY atDay) as sub where tb_api_time.uri="+uri+" and tb_api_time.atDay = sub.atDay GROUP BY sub.atDay ORDER BY sub.atDay DESC LIMIT 0, 10) as A ORDER BY A.atDay ASC"
    return query

def fetchList(uri, cursor):
    returnDic={}
    dayList = list()
    seriesList = list()
    seriesDicAvg = {}
    seriesDicVar = {}
    seriesDicAvg['name'] = "Average(ms)"
    seriesDicVar['name'] = "StandardVeriation(ms)"
    seriesDicAvg['data'] = list()
    seriesDicVar['data'] = list()
    cursor.execute(selectQuery(uri))
    for row in cursor:
        dayList.append(row[0])
        seriesDicAvg['data'].append(row[1])
        seriesDicVar['data'].append(math.sqrt(row[2]))
    
    seriesList.append(seriesDicAvg)
    seriesList.append(seriesDicVar)
    returnDic['categories'] = dayList
    returnDic['series'] = seriesList

    return returnDic

@app.route('/')
def index():
    db = sqlite3.connect("db_api")
    cursor = db.cursor()

    homeDic = fetchList("'/'", cursor)
    apiQuestionsDic = fetchList("'/api/question'", cursor)
    apiQuestionDic = fetchList("'/api/question/1'", cursor)
    createQuestionDic = fetchList("'/question/create'", cursor)

    db.close()
    return render_template('index.html', homeDic=homeDic, apiQuestionsDic=apiQuestionsDic, apiQuestionDic=apiQuestionDic, createQuestionDic=createQuestionDic)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8888)