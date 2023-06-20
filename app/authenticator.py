import os
import time, datetime



def checkpassword(id:str, password:str):
    username = ""
    for c in id:
        if ord(c) >= 65 and ord(c) <= 90:
            username += c
        elif ord(c) >= 97 and ord(c) <= 122:
            username += c
        elif ord(c) >= 48 and ord(c) <= 57:
            username += c

    result = {"username": username, "password": password}

    os.system('printf "\n\n"')
    os.system(f'echo "User login:"')
    os.system(f'echo "Time: {datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}"')
    os.system(f'echo "ID: {id}"')
    os.system(f'echo -n "AuthHash: "')
    authhash = getHashString(username, password)

    if authhash == "server time out":
        result["validation"] = authhash
        return result
    
    conf = open("/usr/local/vpnserver/vpn_server.config", "r", encoding="utf-8")
    conf = conf.readlines()

    startlinenum = 0
    endlinenum = 0
    index = 0
    for i in range(0, len(conf)):
        line = conf[i]
        if line.find("UserList") != -1:
            startlinenum = i
            index = conf[i+1].find("{")
        
    for i in range(startlinenum, len(conf)):
        line = conf[i]
        try:
            if line[index] == "}":
                endlinenum = i
                break
        except IndexError:
            pass

    authstring = None

    for i in range(startlinenum, endlinenum+1):
        line = conf[i]
        token = line.split(" ")
        try:
            if token[0].find("declare") != -1 and token[1].replace("\n","") == username:
                authstring = conf[i+3].split(" ")[-1].replace("\n","")
                break
            else:
                continue

        except IndexError:
            pass

    if authhash == authstring:
        result["validation"] = "login success"
    else:
        result["validation"] = "username/password validation error"
    
    os.system(f'echo {result["validation"]}')
    return result




def getHashString(username:str, password:str):
    os.system("rm -rf sha0string.txt")
    os.system(f'mono /data/sha0generator/sha0.out {username} {password}')
    for i in range(0, 5):
        echo = os.system("test -f '/data/sha0generator/sha0string.txt'")
        if echo == 0:
            break
        else:
            time.sleep(1)
        
    if echo != 0:
        return "server time out"
    
    f = open("sha0string.txt", "r", encoding="utf-8")
    hashstring = f.read()
    f.close()
    os.system("rm -rf sha0string.txt")

    return hashstring