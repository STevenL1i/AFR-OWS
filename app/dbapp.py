import dbconnect

def getProfile(id:str):
    db = dbconnect.connect_with_conf("server.json", "db")
    cursor = db.cursor()

    query = f'SELECT * FROM driverList WHERE driverName = "{id}";'
    cursor.execute(query)
    result = cursor.fetchall()

    driverProf = {}

    return driverProf