import datetime


def roleChecker(tokenrole,userrole):
    try:
        roles={"Admin":1,"School":2,"Reception":3,"Teacher":4,"Student":5}
        if (roles[tokenrole]<roles[userrole]):
            return True
        return False
    except:
        return False

def roleTimer(tokenrole):
    try:
        roles={"Admin":500,"School":100,"Reception":300,"Teacher":400,"Student":500}
        return ( datetime.datetime.utcnow() + datetime.timedelta(hours=roles[tokenrole]))
    except:
        return ( datetime.datetime.utcnow() + datetime.timedelta(hours=100))