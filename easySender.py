#coding=utf8

#简单的发件GUI程序

#A simple email sender to demonstrate the lower modules
#Written by Haoyang Li

import emailSender as sendEmailModule
import emailRetriever as getEmailModule
import tkinter
import tkinter.messagebox
import os

def inputBox(text,command,x,y,anchor,width):
    ibox=tkinter.Button(top,text=text,command=command,width=10,height=1)
    ibox.place(x=x,y=y,anchor=anchor)
    ientry=tkinter.Entry(top,width=width)
    ientry.place(x=x+85,y=y+5,anchor=anchor)
    return ientry

def commandv():
    sender=et1.get()
    tmail=et2.get()
    subject=et3.get()
    fmail=et5.get()
    psw=et6.get()
    pathlist=None
    content=ct.get('0.0',tkinter.END)

    if etf.get():
        pathlist=[etf.get()]
        try:
            if not os.path.exists(pathlist[0]):
                pathlist=None
        except:
            pathlist=None
    if pathlist:
        fstate='附件已经成功获取\n'
    else:
        fstate='\n'

    msg = sendEmailModule.createEmail(subject, content, fmail, sender, tmail, pathlist)
    psd=getEmailModule.parseEmail(msg)
    print(psd)
    getEmailModule.saveParsedEmail(psd,'D:\\works\\ptest\\email_proj2018','testpayload.txt')
    tkinter.messagebox.showinfo('ESM','邮件已经保存\n'+fstate)

def commands():
    sender = et1.get()
    tmail=et2.get()
    tmail_list = et2.get().split(';')
    subject = et3.get()
    fmail = et5.get()
    psw = et6.get()
    pathlist = None
    content = ct.get('0.0', tkinter.END)

    if etf.get():
        pathlist = [etf.get()]
        try:
            if not os.path.exists(pathlist[0]):
                pathlist = None
        except:
            pathlist = None
    if pathlist:
        fstate = '附件已经成功获取\n'
    else:
        fstate = '\n'

    msg = sendEmailModule.createEmail(subject, content, fmail, sender, tmail, pathlist)
    try:
        mailstate=sendEmailModule.sendEmailSMTP(fmail,psw,tmail_list,msg)
        tkinter.messagebox.showinfo('ESM', '邮件已经发送\n' + mailstate+fstate)
    except:
        tkinter.messagebox.showinfo('ESM', '邮件发送失败\n' + mailstate+fstate)
    return mailstate

def commandf():
    pathlist=None
    if etf.get():
        pathlist = [etf.get()]
        try:
            if not os.path.exists(pathlist[0]):
                pathlist = None
        except:
            pathlist = None
    if pathlist:
        fstate='附件存在\n'
    else:
        fstate='附件不存在\n'
    tkinter.messagebox.showinfo('ESM',fstate)
    return fstate

top=tkinter.Tk()
top.geometry('500x500')
top.title('EasySendMailbox')
top.resizable(False,False)

sx=10
sy=10
tkinter.Label(top,text='-·'*100).place(x=sx,y=sy,anchor='nw')
sy+=20
textlist=['发件人','收件人','主题','正文']
et1=tkinter.Entry(top,width=50)
bt1=tkinter.Button(top,text=textlist[0],width=10)
bt1.place(x=sx,y=sy,anchor='nw')
et1.place(x=sx+85,y=sy+5,anchor='nw')
et1.insert('0','<此处填写发件人>')
sy+=40
et2=tkinter.Entry(top,width=50)
bt2=tkinter.Button(top,text=textlist[1],width=10)
bt2.place(x=sx,y=sy,anchor='nw')
et2.place(x=sx+85,y=sy+5,anchor='nw')
et2.insert('0','<此处填写收件邮箱地址>')
sy+=40
et3=tkinter.Entry(top,width=50)
bt3=tkinter.Button(top,text=textlist[2],width=10)
bt3.place(x=sx,y=sy,anchor='nw')
et3.place(x=sx+85,y=sy+5,anchor='nw')
et3.insert('0','<此处填写主题>')
sy+=40
tkinter.Label(top,text=textlist[3]+'-·'*100).place(x=sx,y=sy,anchor='nw')
sy+=25
ct=tkinter.Text(top,width=62,height=14)
ct.place(x=sx,y=sy,anchor='nw')
bts=tkinter.Button(top,text='发送',width=5,height=10,command=commands)
bts.place(x=sx+442,y=sy,anchor='nw')
btv=tkinter.Button(top,text='保存',width=5,height=1,command=commandv)
btv.place(x=sx+442,y=sy+190,anchor='nw')
ct.insert(tkinter.INSERT,'<此处填写正文>')
sy+=190
etf=tkinter.Entry(top,width=50)
btf=tkinter.Button(top,text='附件',command=commandf,width=10)
btf.place(x=sx,y=sy,anchor='nw')
etf.place(x=sx+85,y=sy+5,anchor='nw')
etf.insert('0','<此处填写附件地址>')
sy+=30
tkinter.Label(top,text='-·'*100).place(x=sx,y=sy,anchor='nw')
sy+=25
et5=tkinter.Entry(top,width=50)
bt5=tkinter.Button(top,text='发件邮箱',width=10)
bt5.place(x=sx,y=sy,anchor='nw')
et5.place(x=sx+85,y=sy+5,anchor='nw')
et5.insert('0','<此处填写发件邮箱地址>')
sy+=40
et6=tkinter.Entry(top,width=50,show='x')
bt6=tkinter.Button(top,text='密码SMTP',width=10)
bt6.place(x=sx,y=sy,anchor='nw')
et6.place(x=sx+85,y=sy+5,anchor='nw')

top.mainloop()
