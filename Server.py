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

while True :

    data = connectionSocket.recv(1024)
    data = data.decode('utf-8')

    window = 1

    if data == 'login' :

        connectionSocket.send('login'.encode('utf-8'))
        id = connectionSocket.recv(1024)
        print(id)
        id = fernet.decrypt(id).decode('utf-8')
        pw = connectionSocket.recv(1024)
        print(pw)
        pw = fernet.decrypt(pw).decode('utf-8')

        cursor.execute(f"SELECT * FROM LOGIN")

        tf = False
        for row in cursor :
            if row[0] == id :
                tf = True

        if tf:
            cursor.execute(f"SELECT * FROM LOGIN WHERE id = '{id}'")
            out_data = cursor.fetchone()
            out_id = out_data[0]
            out_pw = out_data[1]

            if pw == out_pw:
                print('login success')
                connectionSocket.send('login success'.encode('utf-8'))

                data = connectionSocket.recv(1024)
                data = data.decode('utf-8')

                if data == 'logout' :
                    print("logout success")
                    count = 0
                    print("wrong =", count)

                elif data == 'secession' :
                    cursor.execute(f"DELETE FROM LOGIN WHERE ID = '{id}'")
                    con.commit()
                    print('secession complete')

            else:
                print('login failed')
                connectionSocket.send('login failed'.encode('utf-8'))
                count += 1
                print('wrong =', count)
        else :
            print('login failed')
            connectionSocket.send('login failed'.encode('utf-8'))
            count += 1
            print(count)

            if count >= 5 :
                print('login denied')
                count = 5

            else :
                pass

    elif data == 'sign in' :
        connectionSocket.send('sign in'.encode('utf-8'))
        print('sign up')

        id = connectionSocket.recv(1024)
        id = fernet.decrypt(id).decode('utf-8')
        pw = connectionSocket.recv(1024)
        pw = fernet.decrypt(pw).decode('utf-8')

        cursor.execute(f"INSERT INTO LOGIN VALUES ('{id}', '{pw}')")
        con.commit()

        connectionSocket.send('signed up'.encode('utf-8'))

    elif data == 'check unique' :
        connectionSocket.send('check unique'.encode('utf-8'))
        print('check unique')

        id = connectionSocket.recv(1024)
        id = fernet.decrypt(id)
        id = id.decode('utf-8')

        cursor.execute(f"SELECT * FROM LOGIN")

        tf = False
        for row in cursor:
            if row[0] == id:
                tf = True

        if tf:
            connectionSocket.send('disabled'.encode('utf-8'))
            print('disabled')

        else:
            connectionSocket.send('able'.encode('utf-8'))
            print('able')

    elif data == 'find' :

        connectionSocket.send('find'.encode('utf-8'))
        print('find')

        id = connectionSocket.recv(1024)
        id = fernet.decrypt(id)
        id = id.decode('utf-8')

        cursor.execute(f"SELECT * FROM LOGIN")

        tf = False
        for row in cursor:
            if row[0] == id:
                tf = True
                pw = row[1]

        if tf:
            connectionSocket.send(fernet.encrypt(pw.encode('utf-8')))
            print(pw)
            countfind = 0
        else:
            connectionSocket.send(fernet.encrypt('#'.encode('utf-8')))
            print('failed')
            countfind += 1
            print('wrong =', countfind)

            if countfind >= 5 :
                print('find denied')
                countfind = 5

    else :
        print('connect closed')
        serverSocket.close()

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
