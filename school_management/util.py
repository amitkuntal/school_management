import datetime
from django.core.files import File
import base64


def roleChecker(tokenrole,userrole):
    try:
        roles={"Admin":1,"School":2,"Reception":3,"Teacher":4,"Student":5}
        if (tokenrole =='Admin' and userrole == 'Admin'):
            return True
        elif (roles[tokenrole]<roles[userrole]):
            return True
        else:
            return False
    except:
        return False

def roleTimer(tokenrole):
    try:
        roles={"Admin":500,"School":100,"Reception":300,"Teacher":400,"Student":500}
        return ( datetime.datetime.utcnow() + datetime.timedelta(hours=roles[tokenrole]))
    except:
        return ( datetime.datetime.utcnow() + datetime.timedelta(hours=100))


def readFiles(fileName):
    f = open('.'+str(fileName), 'rb')
    image = File(f)
    data = base64.b64encode(image.read())
    f.close()
    return data