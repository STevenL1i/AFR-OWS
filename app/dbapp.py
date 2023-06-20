import dbconnect
import datetime

import mysql.connector

regDLtime = datetime.time(18, 30, 0)
wdDLtime = datetime.time(18, 30, 0)
raceCert = {
    "A1": ["A1"],
    "A2": ["A2", "A1"],
    "A3": ["A3", "A2"]
}


def getProfile(id:str):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    query = f'SELECT * FROM driverList WHERE driverName = "{id}";'
    cursor.execute(query)
    result = cursor.fetchall()

    driverProf = {
            "id": id,
            "group": "",
            "team": "",
            "status": "",
            "joindate": ""
        }
    if len(result) > 0:
        driver = result[0]
        driverProf["group"] = driver[2]
        driverProf["team"] = driver[1]
        driverProf["status"] = driver[3]
        joindate_str = driver[4].strftime("%Y-%m-%d")

        driverProf["joindate"] = joindate_str

    else:
        driverProf["group"] = ""
        driverProf["team"] = ""
        driverProf["status"] = "not attended for current season"
        driverProf["joindate"] = ""

    db.close()

    return driverProf


def getRaceByStatus(status:str):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    query = f'SELECT * FROM raceCalendar \
            WHERE raceStatus = "{status}" \
            ORDER BY raceDate ASC;'
    cursor.execute(query)
    result = cursor.fetchall()

    return result

def getRaceByDate(date_from:datetime=None, date_to:datetime=None):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    if date_from != None and date_to != None:
        query = f'SELECT * FROM raceCalendar \
                WHERE raceDate >= "{date_from}" AND raceDate <= "{date_to}" \
                ORDER BY raceDate ASC;'
    elif date_from != None and date_to == None:
        query = f'SELECT * FROM raceCalendar \
                WHERE raceDate >= "{date_from}" \
                ORDER BY raceDate ASC;'
    elif date_from == None and date_to != None:
        query = f'SELECT * FROM raceCalendar \
                WHERE raceDate <= "{date_to}" \
                ORDER BY raceDate ASC;'
    else:
        query = f'SELECT * FROM raceCalendar \
                ORDER BY raceDate ASC;'
        
    cursor.execute(query)
    result = cursor.fetchall()

    return result

def getRaceByGP(gp:str, group:str=None):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    query = f'SELECT * FROM raceCalendar \
            WHERE GP_ENG = "{gp}" '
    if group != None:
        query += f'AND driverGroup = "{group}" '
    
    query += f'ORDER BY raceDate ASC;'
    cursor.execute(query)
    result = cursor.fetchall()

    return result

def getRaceByRound(round:int, group:str=None):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    query = f'SELECT * FROM raceCalendar \
            WHERE Round = {round} '
    if group != None:
        query += f'AND driverGroup = "{group}" '
    
    query += f'ORDER BY raceDate ASC;'
    cursor.execute(query)
    result = cursor.fetchall()

    return result



def getRegist(round:int, gp:str):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()
    drivergroup = ["A1", "A2", "A3"]

    register = {}
    for group in drivergroup:
        query = f'SELECT * FROM registTable \
                WHERE GP = "{gp}" AND raceGroup = "{group}" \
                ORDER BY driverGroup ASC, \
                    CASE team \
                        WHEN "Reserve" THEN 2 \
                        ELSE 1 \
                    END, \
                registTime ASC;'
        cursor.execute(query)
        result = cursor.fetchall()
        for i in range(0, len(result)):
            result[i] = list(result[i])
            result[i][-1] = result[i][-1].strftime("%Y-%m-%d %H:%M:%S")
        register[group] = result
    
    return register



def driverRegist(id:str, gp:str, racegroup:str):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    regresult = {
        "id": id,
        "gp": gp,
        "racegroup": racegroup,
        "result": "stand by"
        }

    driverprof = getProfile(id)
    """
    driverprof = {
        "id":
        "group":
        "team":
        "status":
        "joindate":
    }
    """
    # check driver whether attended for this season
    if driverprof["status"] == "not attended for current season":
        regresult["result"] = "您目前没有报名参加本赛季，请先从群公告内的报名链接报名本赛季"
        return regresult

    # check driver whether retired/ban for this season
    if driverprof["team"] == "Retired":
        regresult["result"] = "您目前已经退出本赛季（或被赛季禁赛），无法再参加本赛季后续的比赛"
        return regresult
    
    # check driver is allow to attend race in this group
    if regresult["racegroup"] not in raceCert[driverprof["group"]]:
        regresult["result"] = f'您目前是{driverprof["group"]}组别车手，暂时无法参加{regresult["racegroup"]}组别的比赛'
        return regresult
    
    # check whether within the regist time
    raceinfo = getRaceByGP(gp, racegroup)
    raceinfo = raceinfo[0]
        ### example raceinfo output
        ### (1, datetime.date(2023, 2, 10), '澳大利亚', 'Australia', 'A3', 'FINISHED')
    regDL = datetime.datetime.combine(raceinfo[1], regDLtime)
    if datetime.datetime.today() > regDL:
        regresult["result"] = "报名时间已截止，请联系当场比赛主持进行补报名"
        return regresult
    

    # regist to database after all condition checked
    try:
        query = "INSERT INTO registTable (driverName, team, driverGroup, GP, raceGroup, registTime) \
                VALUES (%s, %s, %s, %s, %s, %s);"
        val = (id, driverprof["team"], driverprof["group"], gp, racegroup, datetime.datetime.today())
        cursor.execute(query, val)
        db.commit()
        regresult["result"] = f'您已成功报名{regresult["racegroup"]}组别{raceinfo[2]}站的比赛，请刷新页面'
    
    except mysql.connector.errors.IntegrityError:
        regresult["result"] = f'您已报名过{regresult["racegroup"]}组别{raceinfo[2]}站的比赛，请刷新页面'


    return regresult
    


def driverWithdraw(id:str, gp:str, racegroup:str):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    regresult = {
        "id": id,
        "gp": gp,
        "racegroup": racegroup,
        "result": "stand by"
    }

    raceinfo = getRaceByGP(gp, racegroup)
    raceinfo = raceinfo[0]
        ### example raceinfo output
        ### (1, datetime.date(2023, 2, 10), '澳大利亚', 'Australia', 'A3', 'FINISHED')
    wdDL = datetime.datetime.combine(raceinfo[1], wdDLtime)
    if datetime.datetime.today() > wdDL:
        regresult["result"] = "报名时间已截止，请联系当场比赛主持取消报名"
        return regresult

    query = f'DELETE FROM registTable \
            WHERE driverName = "{id}" \
            AND GP = "{gp}" \
            AND raceGroup = "{racegroup}";'
    cursor.execute(query)
    db.commit()
    regresult["result"] = f'您已取消{regresult["racegroup"]}组别{raceinfo[2]}站的比赛，请刷新页面'
    
    return regresult




def getRadioList():
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    query = "SELECT * FROM afr_db.radio \
            ORDER BY timesplayed ASC, lastplayed ASC, orderdate ASC;"
    cursor.execute(query)
    result = cursor.fetchall()

    for i in range(len(result)):
        result[i] = list(result[i])
        try:
            result[i][6] = result[i][6].strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            pass

    return {"songlist": result}



def songorder(id:str, songname:str, artist:str, album:str, link:str):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    orderresult = {
        "id": id,
        "result": "stand by"
    }

    query = f'SELECT * FROM afr_db.Blacklist \
            WHERE id = "{id}" AND type = "radio ban";'
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        orderresult["result"] = "您已被加入点歌台黑名单\n有问题请与管理员联系"
        return orderresult

    
    if songname.replace(" ", "") == "":
        orderresult["result"] = "歌曲名不能为空"
        return orderresult
    
    if artist.replace(" ", "") == "" and link.replace(" ", "") == "":
        orderresult["result"] = "必须输入一个歌手名或分享链接"
        return orderresult
    
    today = datetime.datetime.today()
    today_str = today.strftime("%Y-%m-%d %H:%M")

    try:
        query = "INSERT INTO afr_db.radio VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        val = (id, songname, artist, album, link, today_str, None, 0)
        cursor.execute(query, val)
        db.commit()

        orderresult["result"] = f'歌曲 "{songname}" 点播成功，请刷新页面'
        return orderresult
    
    except mysql.connector.errors.IntegrityError as e:
        # Duplicate entry 'xxx' for key 'radio.PRIMARY'
        if str(e).find("Duplicate entry") != -1 and str(e).find("radio.PRIMARY") != -1:
            orderresult["result"] = "该歌曲已被点播，如果有特殊情况请联系管理员"
        else:
            orderresult["result"] = f'出现未知错误：{str(e)}\n请联系管理员寻求帮助'
        
        return orderresult
    