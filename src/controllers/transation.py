import os
import json
import datetime
import requests
from src.resources.constants import *

def GetCriptos():
    listCripto = list() 
    api = requests.get(API,headers = HEADERS).json()["data"]
    for data in api:
        listCripto.append({"symbol": data["symbol"], "price": data["quote"]["USD"]["price"]})    
    return listCripto

def IsCripto():
    criptos = GetCriptos()
    print("\nCRIPTO MONEDAS DISPONIBLES")
    PSPrint(' '.join([f'{cs["symbol"]}' for cs in criptos]) , 1)
    isValidCripto = list()
    while len(isValidCripto) == 0:
        nameCripto = input("MONEDA: ")
        validateCripto = lambda cripto: cripto["symbol"] == nameCripto
        isValidCripto = list(filter(validateCripto, criptos))
    return isValidCripto  

def TransactionalOperations(dataUser, typeOPeration):
    cripto = IsCripto()[0]
    fileUser = json.load(open(FILE, 'r'))
    userOne = dataUser
    userTwo = list()
    while len(userTwo) == 0:
        textCode = ""
        if typeOPeration == "RECIBIR":
            textCode = "CODIGO DE USUARIO DEL CUAL RECIBE: " 
        else: 
            textCode = "CODIGO DE USUARIO A QUIEN DESEA TRANSFERIR: "
        code = input(textCode) 
        if code != userOne["code"]:
            userTwo = list(filter(lambda user: user["code"] == code, fileUser))
        else:
            PSPrint("INGRESE UN CODIGO DE USUARIO DIFERENTE", 1)    
    userTwo = userTwo[0]
    haveMoney = False
    quantity = ""
    while not haveMoney:
        while not quantity.isnumeric():
            quantity = input("CANTIDAD DE MONEDA: ")
        else:
            quantity = float(quantity)    
        balanceUser = float(userTwo["balance"]  if typeOPeration == "RECIBIR" else userOne["balance"])
        if balanceUser==0 or (balanceUser < quantity):
            quantity = ""
            PSPrint("EL USUARIO NO TIENE SUFICIENTE DINERO", 1)
        else:
            haveMoney = True           
    indexUserOne = fileUser.index(userOne)
    indexUserTwo = fileUser.index(userTwo)
    if typeOPeration == "RECIBIR":
        userOne["balance"] += quantity
        userTwo["balance"] -= quantity
    else:
        userOne["balance"] -= quantity
        userTwo["balance"] += quantity    
    fileUser[indexUserOne] = userOne
    fileUser[indexUserTwo] = userTwo
    json.dump(fileUser, open(FILE, 'w'))
    try:
        transaction = list()
        if os.path.exists(FILE_TRANSACTION) and len(open(FILE_TRANSACTION, 'r').read()) > 0:
            fileTrasaction = json.load(open(FILE_TRANSACTION, 'r'))
            for data in fileTrasaction:
                transaction.append(data)
        newTransaction = {
            "date": str(datetime.datetime.now()),
            "symbol": cripto["symbol"],
            "typeOperation": typeOPeration,
            "codeUser": userOne["code"],
            "quantity": quantity,
            "price": cripto["price"]
        }       
        transaction.append(newTransaction)
        json.dump(transaction, open(FILE_TRANSACTION, 'w'))
        PSPrint("Transacción realizada con éxito!",0)
    except Exception as e:
        PSPrint(f"Ha ocurrido un error al registrar la transacción {e}", 3)

def CurrencyBalance(type):      
    if type == "GENERAL":
        total = 0
        criptos = GetCriptos()
        for cs in criptos:
            price = cs["price"]
            total += price
            print(f"\nMONEDA: {cs['symbol']} | MONTO: {price} USD")
        PSPrint(f"MONTO TOTAL: {total} USD",0)       
    else:
        cripto = IsCripto()[0]
        quantity = ""
        while not quantity.isnumeric():
            quantity = input("CANTIDAD DE MONEDA: ")
        PSPrint(f"LA MONEDA {cripto['symbol']} TIENE UN BALANCE DE {(cripto['price'] * float(quantity))} USD",0)
          
def TransactionHistory():
    if os.path.exists(FILE_TRANSACTION) and len(open(FILE_TRANSACTION, 'r').read()) > 0:
        fileTrasaction = json.load(open(FILE_TRANSACTION, 'r'))
        for data in fileTrasaction:
            message = "\n"
            message += f"FECHA: {data['date']}\n"
            message += f"MONEDA: {data['symbol']}\n"
            message += f"TIPO DE OPERACION: {data['typeOperation']}\n"
            message += f"CODIGO DE USUARIO: {data['codeUser']}\n"
            message += f"CANTIDAD: {data['quantity']}\n"
            message += f"MONTO DEL MOMENTO: {data['price']} USD"
            print(f'\33[92m{message}')      
    else:
        PSPrint("NO SE HAN REALIZADO TRANSACCIONES",1)        