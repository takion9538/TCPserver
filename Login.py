from socket import *
import cx_Oracle
from cryptography.fernet import Fernet

key = b'crNz2jnaPI_OKmA8dj-mLywgFTeMw4WLIlCDZMkUulo='
fernet = Fernet(key)

oracleid = "budi"
oraclepassword = "1234"
count = 0
countfind = 0

con = cx_Oracle.connect(oracleid, oraclepassword, "localhost:1521/XE", encoding="UTF-8")
cursor = con.cursor()
host = "127.0.0.1"
port = 8800

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(10)
print("waiting")

connectionSocket, addr = serverSocket.accept()
print(str(addr), "connected")

data = connectionSocket.recv(1024)
print(data.decode('utf-8'))

connectionSocket.send('connected'.encode('utf-8'))

connection = "client connected"
if data != connection:
    serverSocket.close()




