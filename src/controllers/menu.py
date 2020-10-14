import json
from src.models.users import Users
from src.resources.constants import PSPrint
from src.controllers.transation import *

def MenuUser():
    print("SELECCIONE UNA OPCION PARA CONTINUAR: \n")
    print("1) INICIAR SESION")
    print("2) CREAR USUARIO\n")
    opcion = ""
    while not opcion.isnumeric():
        opcion = input("SELECCIONAR: ")
        if opcion == "1":
            username = input("\nUSUARIO: ")
            password = input("CONTRASEÑA: ")
            user = Users(username, password)
            dataUser = json.loads(user.LoginUser())
            if dataUser["error"]:
                PSPrint(dataUser["message"], 1)
                MenuUser()
            else:
                Main(dataUser["message"])
        elif opcion == "2":
            username = input("\nUSUARIO: ")
            password = input("CONTRASEÑA: ")
            code = input("CODIGO: ")
            user = Users(username, password, code)
            user.CreateUser()
            MenuUser()
        else:
            MenuUser()    

def MenuSelection(dataUser):
    print("SELECCIONE UNA OPCION PARA CONTINUAR: \n")
    print("1) RECIBIR CANTIDAD")
    print("2) TRANSFERIR MONTO")
    print("3) MOSTRAR BALANCE DE UNA MONEDA")
    print("4) MOSTRAR BALANCE GENERAL")
    print("5) MOSTRAR HISTORICO DE TRANSACCIONES")
    print("6) SALIR DEL PROGRAMA\n")
    opcion = ""
    while not opcion.isnumeric():
        opcion = input("SELECCIONAR: ")
        if opcion == "1":
            TransactionalOperations(dataUser, "RECIBIR")
        elif opcion == "2":
            TransactionalOperations(dataUser, "TRANSFERIR")
        elif opcion == "3":
            CurrencyBalance("UNA MONEDA")
        elif opcion == "4":
            CurrencyBalance("GENERAL")
        elif opcion == "5":
            TransactionHistory()  
        elif opcion == "6":
            break
    if opcion != "6":
        Main(dataUser)    

def Main(dataUser):
    PSPrint(f"***********BIENVENIDO(A) {dataUser['username'].upper()}**************",2)
    MenuSelection(dataUser)