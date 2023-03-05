import tkinter as tk
from socket import *
from tkinter import *

from cryptography.fernet import Fernet
from tkinter import messagebox

key = b'crNz2jnaPI_OKmA8dj-mLywgFTeMw4WLIlCDZMkUulo='
fernet = Fernet(key)

ip = "127.0.0.1"
port = 8800
addr = (ip, port)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(addr)

print("connected")
clientSocket.send("client connected".encode('utf-8'))

data = clientSocket.recv(1024)

window = tk.Tk()
window.title("로그인")
window.geometry("350x200+100+100")
window.resizable(False, False)

idLabel = tk.Label(window,
                   text="아이디",
                   width=8,
                   height=1,
                   font=('맑은 고딕', 16, 'bold'),
                   bg='white',
                   fg='black')
idLabel.grid(row=0, column=0, padx=10, pady=10)

pwLabel = tk.Label(window,
                   text="패스워드",
                   width=8,
                   height=1,
                   font=('맑은 고딕', 16, 'bold'),
                   bg='white',
                   fg='black')
pwLabel.grid(row=1, column=0, padx=10, pady=10)

idEntry = tk.Entry(window,
                   width=8,
                   font=('맑은 고딕', 16, 'bold'),
                   bg='white',
                   fg='black')
idEntry.grid(row=0, column=1, padx=10, pady=10)

pwEntry = tk.Entry(window,
                   width=8,
                   font=('맑은 고딕', 16, 'bold'),
                   bg='white',
                   fg='black',
                   show='*')
pwEntry.grid(row=1, column=1, padx=10, pady=10)

def onClick():
    clientSocket.send('login'.encode('utf-8'))
    clientSocket.recv(1024)

    id = idEntry.get()
    pw = pwEntry.get()

    clientSocket.send(fernet.encrypt(id.encode('utf-8')))
    clientSocket.send(fernet.encrypt(pw.encode('utf-8')))

    data = clientSocket.recv(1024)
    print(data.decode('utf-8'))

    if data.decode('utf-8') == 'login success':
        LoginSuccess()

def LoginSuccess() :
    myPage = tk.Tk()
    myPage.title("마이페이지")
    myPage.geometry("1050x680")
    myPage.protocol("WM_DELETE_WINDOW", lambda : [myPage.destroy(),
                                                  clientSocket.send("logout".encode('utf-8'))])

    google = PhotoImage(file="google.png", master=myPage)

    logoutButton = tk.Button(myPage,
                            width=6,
                            font=('맑은 고딕', 12, 'bold'),
                            text='로그아웃',
                            bg='white',
                            command=lambda : [myPage.destroy()])
    logoutButton.grid(row=0, column=1, padx=5, pady=5, sticky='W')

    deleteButton = tk.Button(myPage,
                             width=6,
                             font=('맑은 고딕', 12, 'bold'),
                             text='회원탈퇴',
                             bg='white',
                             command=lambda : [Secession(), myPage.destroy()])
    deleteButton.grid(row=0, column=0, padx=5, pady=5, sticky='W')

    googleLable = tk.Label(myPage,
                           image=google)
    googleLable.grid(row=1, rowspan=20, column=0, columnspan=20)

    myPage.mainloop()

def Secession() :
    if messagebox.askokcancel("탈퇴", "정말 탈퇴하시겠습니까?"):
        clientSocket.send("secession".encode('utf-8'))
        messagebox.showinfo("완료", "회원 탈퇴가 완료되었습니다.")

loginButton = tk.Button(window,
                        width=6,
                        font=('맑은 고딕', 12, 'bold'),
                        text='로그인',
                        bg='white',
                        command=onClick)
loginButton.grid(row=1, column=3, padx=10, pady=10)

def Find():
    windowFind = tk.Tk()
    windowFind.title("찾기")
    windowFind.geometry("300x200+100+100")
    windowFind.resizable(False, False)
    findIdLabel = tk.Label(windowFind,
                           text="아이디",
                           width=8,
                           height=1,
                           font=('맑은 고딕', 16, 'bold'),
                           bg='white',
                           fg='black')
    findIdLabel.grid(row=0, column=0, padx=10, pady=10)

    findPwLabel = tk.Label(windowFind,
                           text="패스워드",
                           width=8,
                           height=1,
                           font=('맑은 고딕', 16, 'bold'),
                           bg='white',
                           fg='black')
    findPwLabel.grid(row=1, column=0, padx=10, pady=10)

    findIdText = tk.Entry(windowFind,
                          width=8,
                          font=('맑은 고딕', 16, 'bold'),
                          bg='white',
                          fg='black')
    findIdText.grid(row=0, column=1, padx=10, pady=10)

    findPwText = tk.Entry(windowFind,
                          width=8,
                          font=('맑은 고딕', 16, 'bold'),
                          bg='white',
                          state='disabled',
                          fg='black')
    findPwText.grid(row=1, column=1, padx=10, pady=10)

    def FindPW():
        clientSocket.send('find'.encode('utf-8'))
        clientSocket.recv(1024)

        id = findIdText.get()
        clientSocket.send(fernet.encrypt(id.encode('utf-8')))
        pw = clientSocket.recv(1024)
        pw = fernet.decrypt(pw)
        pw = pw.decode('utf-8')

        if pw == '#':
            windowFindFalse = tk.Tk()
            windowFindFalse.title("찾기")
            windowFindFalse.geometry("200x70+100+100")
            windowFindFalse.resizable(False, False)
            findIdLabel = tk.Label(windowFindFalse,
                                   text='일치하지 않음',
                                   width=14,
                                   height=1,
                                   font=('맑은 고딕', 16, 'bold'),
                                   bg='white',
                                   fg='black')
            findIdLabel.grid(row=0, column=0, padx=10, pady=10)

            windowFindFalse.mainloop()

        else :
            windowFindTrue = tk.Tk()
            windowFindTrue.title("찾기")
            windowFindTrue.geometry("200x70+100+100")
            windowFindTrue.resizable(False, False)
            findIdLabel = tk.Label(windowFindTrue,
                                   text=pw,
                                   width=12,
                                   height=1,
                                   font=('맑은 고딕', 16, 'bold'),
                                   bg='white',
                                   fg='black')
            findIdLabel.grid(row=0, column=0, padx=10, pady=10)

            windowFindTrue.mainloop()

    findPwButton = tk.Button(windowFind,
                             width=7,
                             font=('맑은 고딕', 12, 'bold'),
                             text='찾기',
                             bg='white',
                             command=FindPW)
    findPwButton.grid(row=3, column=0, padx=10, pady=10)

    windowFind.mainloop()

findButton = tk.Button(window,
                       width=6,
                       font=('맑은 고딕', 12, 'bold'),
                       text='찾기',
                       bg='white',
                       command=Find)
findButton.grid(row=2, column=1, padx=10, pady=10)


def SignUp():
    windowSign = tk.Tk()
    windowSign.title("회원가입")
    windowSign.geometry("350x200+100+100")
    windowSign.resizable(False, False)
    signIdLabel = tk.Label(windowSign,
                           text="아이디",
                           width=8,
                           height=1,
                           font=('맑은 고딕', 16, 'bold'),
                           bg='white',
                           fg='black')
    signIdLabel.grid(row=0, column=0, padx=10, pady=10)

    signPwLabel = tk.Label(windowSign,
                           text="패스워드",
                           width=8,
                           height=1,
                           font=('맑은 고딕', 16, 'bold'),
                           bg='white',
                           fg='black')
    signPwLabel.grid(row=1, column=0, padx=10, pady=10)

    signIdText = tk.Entry(windowSign,
                          width=8,
                          font=('맑은 고딕', 16, 'bold'),
                          bg='white',
                          fg='black')
    signIdText.grid(row=0, column=1, padx=10, pady=10)

    signPwText = tk.Entry(windowSign,
                          width=8,
                          font=('맑은 고딕', 16, 'bold'),
                          bg='white',
                          fg='black',
                          show='*')
    signPwText.grid(row=1, column=1, padx=10, pady=10)

    def SignIn():
        clientSocket.send('sign in'.encode('utf-8'))
        clientSocket.recv(1024)

        id = signIdText.get()
        pw = signPwText.get()
        clientSocket.send(fernet.encrypt(id.encode('utf-8')))
        clientSocket.send(fernet.encrypt(pw.encode('utf-8')))
        signInButton.configure(state='disabled')
        clientSocket.recv(1024)
        print('signed up')

    signInButton = tk.Button(windowSign,
                             width=7,
                             font=('맑은 고딕', 12, 'bold'),
                             text='회원가입',
                             bg='white',
                             state='disabled',
                             command=lambda : [SignIn(), windowSign.destroy()])
    signInButton.grid(row=3, column=0, padx=10, pady=10)

    def CheckUnique():
        clientSocket.send('check unique'.encode('utf-8'))
        clientSocket.recv(1024)

        id = signIdText.get()
        id = str(id)

        clientSocket.send(fernet.encrypt(id.encode('utf-8')))
        check = clientSocket.recv(1024)
        check = check.decode('utf-8')

        if check == 'able':
            signIdText.configure(state='disabled')
            checkButton.configure(state='disabled')
            signInButton.configure(state='normal')

            windowAble = tk.Tk()
            windowAble.title("사용가능")
            windowAble.geometry("150x70+100+100")
            windowAble.resizable(False, False)

            ableLabel = tk.Label(windowAble,
                                 text="사용가능",
                                 width=8,
                                 height=1,
                                 font=('맑은 고딕', 16, 'bold'),
                                 bg='white',
                                 fg='black')
            ableLabel.grid(row=0, column=0, padx=10, pady=10)

        else:
            windowDisabled = tk.Tk()
            windowDisabled.title("사용불가")
            windowDisabled.geometry("180x70+100+100")
            windowDisabled.resizable(False, False)

            DisabledLabel = tk.Label(windowDisabled,
                                     text="사용불가",
                                     width=8,
                                     height=1,
                                     font=('맑은 고딕', 16, 'bold'),
                                     bg='white',
                                     fg='black')
            DisabledLabel.grid(row=0, column=0, padx=10, pady=10)

    checkButton = tk.Button(windowSign,
                            width=6,
                            font=('맑은 고딕', 12, 'bold'),
                            text='중복확인',
                            bg='white',
                            command=CheckUnique)
    checkButton.grid(row=0, column=2, padx=10, pady=10)


signupButton = tk.Button(window,
                         width=6,
                         font=('맑은 고딕', 12, 'bold'),
                         text='회원가입',
                         bg='white',
                         command=SignUp)
signupButton.grid(row=2, column=0, padx=10, pady=10)

def on_closing() :
    if messagebox.askokcancel("종료", "정말 종료하시겠습니까?"):
        window.destroy()
        clientSocket.send("close connect".encode('utf-8'))

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
