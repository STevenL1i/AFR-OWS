import authenticator

id = "afr_public"
pwd = "afr_public"
usr = ""
for c in id:
    if ord(c) >= 65 and ord(c) <= 90:
        usr += c
    elif ord(c) >= 97 and ord(c) <= 122:
        usr += c
    elif ord(c) >= 48 and ord(c) <= 57:
        usr += c

usr = "STevenL2i"
pwd = "ABC1120abc"

authhash = authenticator.getHashString(usr, pwd)

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
        if token[0].find("declare") != -1 and token[1].replace("\n","") == usr:
            authstring = conf[i+3].split(" ")[-1].replace("\n","")
            break
        else:
            continue

    except IndexError:
        pass

if authhash == authstring:
    validation = "login success!!!"
else:
    validation = "username/password validation error"

print(validation)