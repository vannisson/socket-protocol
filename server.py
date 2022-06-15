import socket            
import json 

s = socket.socket()        
print ("Socket successfully created")

users = []
def read(req, users):
  if req["param"]!= "":
    for value in users:
      if value["cpf"] == req["param"]:
        return {"status":200,"reqId":req["reqId"], "message": value}
    return {"status":404,"reqId":req["reqId"], "message": "User not found"}
  else:
    return {"status":200,"reqId":req["reqId"], "message": users}

def add(req, users):
  if req["body"]== "":
    return {"status":400, "reqId":req["reqId"], "message":"Bad Request"}
  for value in users:
    if value["cpf"] == req["body"]["cpf"]:
      return {"status":409,"reqId":req["reqId"], "message":"User added"}
  users.append(req["body"])
  return {"status":200,"reqId":req["reqId"], "message":"User added"}

def change(req, users):
  updated_user = {}
  if req["param"] == "":
    return {"status":400, "reqId":req["reqId"], "message":"Bad Request"}
  else:
    for n in range(len(users)):
      aux = users[n]
      if aux["cpf"] == req["param"]:
        users.pop(n)
        value = {"cpf":req["param"], "name":req["body"]["name"], "city":req["body"]["city"]}
        users.append(value)
        return {"status":200,"reqId":req["reqId"], "message": value}
        
    return {"status":404,"reqId":req["reqId"], "message": "User not found"}

def delete(req, users):
  for n in range(len(users)):
    aux = users[n]
    if aux["cpf"] == req["param"]:
      users.pop(n)
  return {"status":200,"reqId":req["reqId"],"message":"User deleted successfully"}

def handleOperation(req, users):
  if req["operation"] == "READ":
    return read(req, users)
  elif req["operation"] == "ADD":
    return add(req, users)
  elif req["operation"] == "CHANGE":
    return change(req, users)
  elif req["operation"] == "DELETE":
    return delete(req, users)
  else:
    return {"status":400, "reqId":req["reqId"], "message":"Bad Request"}

def handleRequestWithAuth(req, users):
  if req["token"]!= "":
    return handleOperation(req, users)
  else:
    return {"status":401, "reqId":req["reqId"], "message":"Unauthorized"}

port = 12345               
 
s.bind(('', port))        
print ("socket binded to %s" %(port))
 

s.listen(5)    
print ("socket is listening")           
 
while True:
  # try:
    c, addr = s.accept()    
    print ('Got connection from', addr )
    
    request = c.recv(1024)
    data_loaded = json.loads(request)
    print(f"Received Request: {data_loaded}")

    response = handleRequestWithAuth(data_loaded, users)

    data_string = json.dumps(response) 
    c.send(data_string.encode())
  
    c.close()

  # except Exception as e:
  #         error_response = {}
  #         print({"status":500, "reqId":data_loaded["reqId"], "message":"Internal Server Error"})
  #         c.close()
  #         break  


			
	