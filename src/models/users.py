import os
import json
import datetime
from src.resources.constants import FILE, FOLDER , PSPrint

class Users:
    def __init__(self, username, password, code="0000"):
        self.username = username
        self.password = password
        self.code = code

    def CreateUser(self):
        try:
            listUsers = list()
            if not os.path.exists(FOLDER):
                os.makedirs(FOLDER)
            if os.path.exists(FILE) and len(open(FILE, 'r').read()) > 0:
                fileUser = json.load(open(FILE, 'r'))
                for data in fileUser:
                    if data["code"] != self.code:
                        listUsers.append(data)
                    else:
                        return PSPrint("Ya existe un usuario registrado con este código", 2)
            newUser = {
                "username": self.username,
                "password": self.password,
                "code": self.code,
                "balance": float(100000),
                "createAt": str(datetime.datetime.now())
            }
            listUsers.append(newUser)
            if self.username!="" and self.password!="" and self.code!="":
                json.dump(listUsers, open(FILE, 'w'))
                PSPrint("Usuario registrado!",0)
            else:
                PSPrint("No se admiten campos vacios",1)    
        except Exception as e:
            PSPrint(f"Ha ocurrido un error al registrar el usuario {e}", 3)

    def LoginUser(self):
        if os.path.exists(FILE) and len(open(FILE, 'r').read()) > 0:
            fileUser = json.load(open(FILE, 'r'))
            compareFields = lambda data: data["username"] == self.username and data["password"] == self.password
            dataUser = list(filter(compareFields, fileUser))
            if len(dataUser) > 0: 
                return self.InfoUser(dataUser[0], False)
            else:
                return self.InfoUser("Usuario o contraseña incorrectos")
        else:
            return self.InfoUser("No hay usuarios registrados")

    def InfoUser(self, message, isError=True):
        return json.dumps({"message": message, "error": isError})
