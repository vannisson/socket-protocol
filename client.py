import random
import socket
import json

# Request Model:
#req = {"reqId":"","operation":"","param":"","body":{},"token":""}

def handleRequest():
  id = random.randint(0,100)
  op = input("Digite a operação: ")
  token = input("Token: ")
  cpf = input("CPF: ")
  if op == "READ" or op == "DELETE":
    return {"reqId":id,"operation":op, "param": cpf, "body":{}, "token":token}
  name = input("Name: ")
  city = input("Cidade: ")

  if op == "CHANGE":
    return {"reqId":id,"operation":op, "param": cpf, "body":{"name":name,"city":city}, "token":token}
  elif op == "ADD":
    return {"reqId":id,"operation":op, "param": "", "body":{"cpf":cpf,"name":name,"city":city}, "token":token}
  else:
    return {"status":400, "reqId":id, "message":"Bad Request"}

request = handleRequest()
print(f"Requisição enviada: ", request)
data_string = json.dumps(request)

s = socket.socket()        
 
port = 12345               
 
s.connect(('127.0.0.1', port))
s.send(data_string.encode())

response = s.recv(1024).decode()
print ("Resposta: ",response)

s.close()