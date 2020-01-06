# -*- coding: utf-8 -*-

#写信模块

#Email writer module
#Written by Haoyang Li

# Form implementation generated from reading ui file 'writeForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from auxFunctions import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from UIEditor import TextEditor
from emailSender import *
from re import compile
from threading import Thread

class emailWriter(object):
    def __init__(self,content=None,tmail=None,subject=None,psdlist=None,username=None):
        self.mainpsdlist=psdlist if psdlist else []
        self.conpsdlist=[]
        self.parsedictlist=[]
        self.lines={}
        self.lines=getMembers(data=self.parsedictlist)
        self.MemberButton=[]
        self.file = []
        self.uploadfile =[]
        self.filepath ={}
        self.filecount=0
        self.get=[]
        self.texteditor=TextEditor()
        self.accepted=False

        self.subject=subject
        self.to=tmail
        self.content=content
        self.username=username if username else 'wellmailuser'
        self.fmail='wellmail@well.com'
        self.password=''
        self.sender='weller'
        self.reciever='wellee'
        self.pathlist=list(self.filepath.values())
        self.edcan=None
        self.append=False

        self.sendfunc1=None
        self.sendfunc2=None
        self.sendfailfunc=None
        self.backfunc=None
        self.backfuncpara=None

        memberfilename = 'user\\user_info\\' + self.username + '\\member.txt'
        if os.path.exists(memberfilename):
            with open(memberfilename, 'r+') as file_object:
                lines = file_object.read()
                if len(lines) == 0:
                    self.contact = {}
                else:
                    self.contact = eval(lines)
            for key,value in self.contact.items():
                self.conpsdlist.append({'from':key+'<'+value+'>'})
            self.parsedictlist=self.conpsdlist
            self.lines = getMembers(data=self.parsedictlist)
        else:
            pass
            #print('no such file',memberfilename)

    def setupUi(self, Form):
        #创建写信界面
        Form.setObjectName("Form")
        Form.resize(1004, 709)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ReceiverLayout = QtWidgets.QHBoxLayout()
        self.ReceiverLayout.setObjectName("ReceiverLayout")
        self.Receiver_label = QtWidgets.QLabel(Form)
        self.Receiver_label.setObjectName("Receiver_label")
        self.ReceiverLayout.addWidget(self.Receiver_label)
        self.Receiver_edit = QtWidgets.QLineEdit(Form)
        self.Receiver_edit.setObjectName("Receiver_edit")
        self.ReceiverLayout.addWidget(self.Receiver_edit)
        self.gridLayout_2.addLayout(self.ReceiverLayout, 0, 0, 1, 4)
        self.Member_label = QtWidgets.QPushButton(Form)
        self.Member_label.setFlat(True)
        self.Member_label.setObjectName("Member_label")
        self.Member_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Member_label.setToolTip('点击切换')
        self.gridLayout_2.addWidget(self.Member_label, 0, 4, 2, 1)
        self.SubjectLayout = QtWidgets.QHBoxLayout()
        self.SubjectLayout.setObjectName("SubjectLayout")
        self.Subject_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Subject_label.sizePolicy().hasHeightForWidth())
        self.Subject_label.setSizePolicy(sizePolicy)
        self.Subject_label.setObjectName("Subject_label")
        self.SubjectLayout.addWidget(self.Subject_label)
        self.Subject_edit = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Subject_edit.sizePolicy().hasHeightForWidth())
        self.Subject_edit.setSizePolicy(sizePolicy)
        self.Subject_edit.setObjectName("Subject_edit")
        self.SubjectLayout.addWidget(self.Subject_edit)
        self.gridLayout_2.addLayout(self.SubjectLayout, 1, 0, 1, 4)
        self.Text_label = QtWidgets.QLabel(Form)
        self.Text_label.setObjectName("Text_label")
        self.gridLayout_2.addWidget(self.Text_label, 2, 0, 1, 1)

        self.Writing = QtWidgets.QMdiArea()
        self.Writing.setObjectName("Writing")
        self.edcan=QtWidgets.QWidget()
        self.texteditor.setupUi(self.edcan)
        self.Writing.addSubWindow(self.edcan)
        self.edcan.showMaximized()
        self.gridLayout_2.addWidget(self.Writing, 2, 1, 2, 3)

        self.Member = QtWidgets.QScrollArea(Form)
        self.Member.setStyleSheet("QScrollArea {background-color:rgbf(255,255,255,60);}")
        self.Member.viewport().setStyleSheet("background-color:rgbf(255,255,255,60);")
        self.Member.setWidgetResizable(True)
        self.Member.setObjectName("Member")
        window_pale = QtGui.QPalette()
        window_pale.setBrush(Form.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(os.getcwd()+'\\'+'img\\backgroundEmailWriter.png')))
        self.verticalLayout_2 = QtWidgets.QWidget(Form)
        self.verticalLayout_2.setPalette(window_pale)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.spacerItem = QtWidgets.QSpacerItem(20, 500, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.setLayout(self.verticalLayout)
        self.Member.setWidget(self.verticalLayout_2)
        self.gridLayout_2.addWidget(self.Member, 2, 4, 4, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.filepart = QtWidgets.QHBoxLayout()
        self.filepart.setObjectName("FilelLayout")
        self.File_label = QtWidgets.QLabel(Form)
        self.File_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.File_label.setObjectName("File_label")
        self.filepart.addWidget(self.File_label)
        self.bappendfile = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bappendfile.sizePolicy().hasHeightForWidth())
        self.bappendfile.setSizePolicy(sizePolicy)
        self.bappendfile.setMaximumSize(QtCore.QSize(100, 30))
        self.bappendfile.setObjectName("bappendfile")
        self.bappendfile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bappendfile.clicked.connect(self.bappendfileClicked)
        self.filepart.addWidget(self.bappendfile)
        self.gridLayout_2.addLayout(self.filepart, 4, 1, 1, 3)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 5, 1, 1, 3)
        self.filepart = QtWidgets.QHBoxLayout()
        self.filepart.setObjectName("FilesLayout")
        self.gridLayout_2.addLayout(self.filepart, 7, 2, 2, 1)
        self.SendLayout = QtWidgets.QHBoxLayout()
        self.SendLayout.setObjectName("SendLayout")
        self.bsend = QtWidgets.QPushButton(Form)
        self.bsend.setMaximumSize(QtCore.QSize(100, 30))
        self.bsend.setObjectName("Send_button")
        self.bsend.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bsend.clicked.connect(self.bsendClicked)
        self.SendLayout.addWidget(self.bsend)
        self.Back_button = QtWidgets.QPushButton(Form)
        self.Back_button.setMaximumSize(QtCore.QSize(100, 30))
        self.Back_button.setObjectName("Back_button")
        self.Back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Back_button.clicked.connect(self.backbuttonClicked)
        self.SendLayout.addWidget(self.Back_button)
        self.gridLayout_2.addLayout(self.SendLayout, 7, 4, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(240, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 8, 3, 1, 1)

        self.setMembers()
        self.verticalLayout.addItem(self.spacerItem)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        #self.line.close()
        self.File_label.setText('')


        if self.to:
            self.Receiver_edit.setText(self.to)
        if self.subject:
            self.Subject_edit.setText(self.subject)
        if self.content:
            self.texteditor.textEdit.setHtml(self.content)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Receiver_label.setText(_translate("Form", "收件人:"))
        self.Member_label.setText(_translate("Form", "通讯录"))
        self.Member_label.setCheckable(True)
        self.Member_label.toggled.connect(self.memberChecked)
        self.Subject_label.setText(_translate("Form", "主题:  "))
        self.Text_label.setText(_translate("Form", "正文"))
        self.File_label.setText(_translate("Form", "附件"))
        self.bappendfile.setText(_translate("Form", "添加附件"))
        self.bsend.setText(_translate("Form", "发送"))
        self.Back_button.setText(_translate("Form", "返回"))


    def setMembers(self):
        #用于显示右边栏的通讯录列表
        for i in range(0, len(self.lines)):
            self.Button = DCbutton()
            self.Button.setFixedSize(140, 28)
            self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.MemberButton.append(self.Button)

        for i in range(0, len(self.lines)):
            self.MemberButton[i].setFlat(True)
            self.MemberButton[i].setObjectName("MemberButton__" + str(i))
            self.verticalLayout.addWidget(self.MemberButton[i])
            self.button = self.MemberButton[i]
            self.click(self.button, i)
            self.doubleclick(self.button,i)


        for i in range(0, len(self.lines)):
            hanzi_regex = compile(r'[\u4E00-\u9FA5]')
            if len(self.lines[i][0]) < 14:
                self.MemberButton[i].setText(self.lines[i][0] + " " * (14 - len(self.lines[i][0]) - len(hanzi_regex.findall(self.lines[i][0]))))
                self.MemberButton[i].setToolTip('')
            else:
                self.MemberButton[i].setText(self.lines[i][0][0:9] + '....')
                self.MemberButton[i].setToolTip(self.lines[i][0])


    def msgAccepted(self):
        self.accepted=True

    def msgRejected(self):
        self.accepted=False

    def memberChecked(self,checked):
        #点击标签可以在当前收件人与通讯录列表再见切换
        if checked:
            try:
                self.lines = getMembers(data=self.mainpsdlist)
                for but in self.MemberButton:
                    but.close()
                self.MemberButton.clear()
                self.verticalLayout.removeItem(self.spacerItem)
                self.setMembers()
                self.verticalLayout.addItem(self.spacerItem)
                self.Member_label.setText('当前收件箱的发件人')
            except:
                pass
        else:
            self.lines = getMembers(data=self.conpsdlist)
            for but in self.MemberButton:
                but.close()
            self.MemberButton.clear()
            self.verticalLayout.removeItem(self.spacerItem)
            self.setMembers()
            self.verticalLayout.addItem(self.spacerItem)
            self.Member_label.setText('通讯录')

    def backbuttonClicked(self):
        if self.backfunc:
            self.backfunc()

    def bappendfileClicked(self):
        #添加附件的类型
        filetype="All Files (*);;Text Files (*.txt);;Jpeg (*.jpg);;Png (*.png);;Doc Files(*.doc);;Pdf Files(*.pdf)"
        msgBox=QtWidgets.QWidget()
        files, ok1 = QFileDialog.getOpenFileNames(msgBox, "多文件选择", "C:/", filetype)
        for path in files:
            self.bappendfileClickedOne(path)

    def bappendfileClickedOne(self,path):
        #选择需要发送的附件
        path = path
        name = path.split('/')[-1]
        self.accepted=True
        if self.accepted:
            try:
                fp=open(path,'rb')
                fp.close()
            except:
                try:
                    fp=open(path+'\\'+name,'rb')
                    path=path+'\\'+name
                    fp.close()
                except:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
                    msgBox.setWindowTitle('添加附件')
                    msgBox.setText('该附件不存在额')
                    msgBox.exec()
                    return
            self.addFileButton(name,path)
            self.showFileButton()
            self.File_label.setText('附件')
            #print(str(self.filepath))
        else:
            pass
            #print('rejected')
        #self.line.show()

    def addFileButton(self,filename,filepath):
        if filename not in self.filepath.keys():
            self.file.append(QtWidgets.QPushButton())
            self.file[-1].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.file[-1].setFlat(True)
            self.file[-1].setObjectName("file"+str(len(self.file)))
            self.file[-1].setText(filename)
            self.file[-1].setCheckable(True)
            self.file[-1].setChecked(True)
            self.filepath[filename]=filepath
            self.uploadfile.append(filename)
            self.file[-1].toggled.connect(self.fileButtonPress)
            self.filecount+=1

    def fileButtonPress(self):
        #添加附件Button被点击，就选择自己想发送的附件
        for fb in self.file:
            if fb.isChecked():
                if fb.text() in self.uploadfile:
                    pass
                else:
                    self.uploadfile.append(fb.text())
            else:
                try:
                    fb.close()
                    self.uploadfile.remove(fb.text())
                    self.filepath.pop(fb.text())
                    self.filecount-=1
                except:
                    pass
                try:
                    self.file.remove(fb)
                except:
                    pass
        if self.uploadfile == []:
            self.File_label.setText('')
            #self.line.close()
        #print(self.uploadfile)

    def showFileButton(self):
        #将添加的附加以Button形式显示在下方
        layout=QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        n=0
        m=0
        maxbutton=10 if len(self.file)<20 else 20
        for fb in self.file:
            layout.addWidget(fb,m,n)
            n+=1
            if n%maxbutton==0:
                m+=1
                n=0
        self.filepart.addLayout(layout)

    def bsendClicked(self):
        self.subject = self.Subject_edit.text()
        self.to = self.Receiver_edit.text()
        #print(self.to)
        if self.to=='' :
            self.caution(text='记得填写收件人哦    ')
            return
        if self.to[-1]!=';':
            self.to+=';'
        self.content = self.texteditor.textEdit.toHtml()
        delp="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">"""
        reps="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""
        self.content=self.content.replace(delp,reps)
        self.pathlist = list(self.filepath.values())
        email_regex = compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
        for tmail in self.to.split(';'):
            if tmail=='':
                continue
            if not email_regex.findall(tmail):
                self.caution(text='收件人邮箱格式不正确呢  ')
                return
        #print('checked')
        if self.sendfunc1:
            self.sendfunc1()
        tmail_list=self.to.split(';')
        tmail_list.pop(-1)
        #print(tmail_list)
        msg=createEmail(self.subject, self.content, self.fmail, self.sender, tmail_list,self.pathlist)
        #print('created')
        #print(tmail_list)
        sendthread=SendEmailThread(self.fmail,self.password,tmail_list,msg,self.append)
        sendthread.finfunc=self.sendfunc2
        sendthread.failfunc=self.sendfailfunc
        #sendthread.start()
        self.caution(title='稍等',text='邮件正在发送...    ')
        success=sendthread.run()
        if not success:
            self.caution(title='抱歉',text='邮件发送失败，原因可能是\n①网络连接断开\n②发件账户或密码错误（点击设置可以修改）\n③该账户未开通SMTP服务')


    def click(self, button, i):
        button.clicked.connect(lambda: self.shows(i))

    def doubleclick(self,button,i):
        button.doubleclick=lambda: self.oneshow(i)

    def shows(self, i):
        _translate = QtCore.QCoreApplication.translate
        currentto=self.Receiver_edit.text()
        if currentto!='':
            currentto+=';'
        try:
            self.Receiver_edit.setText(_translate("Form", currentto+self.lines[i][0] + "<" + self.lines[i][1] + ">"))
        except:
            try:
                self.Receiver_edit.setText(_translate("Form", currentto+self.lines[i][0]))
            except:
                #print(self.lines[i])
                self.caution(text='该地址可能有问题，无法添加')

    def oneshow(self,i):
        _translate = QtCore.QCoreApplication.translate
        try:
            self.Receiver_edit.setText(_translate("Form", self.lines[i][0] + "<" + self.lines[i][1] + ">"))
        except:
            try:
                self.Receiver_edit.setText(_translate("Form", self.lines[i][0]))
            except:
                #print(self.lines[i])
                self.caution(text='该地址可能有问题，无法添加')

    def caution(self,title='啊哦',text='稍等'):
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.setWindowOpacity(0.8)
        msgBox.exec()

class SendEmailThread(Thread):
    def __init__(self,fmail,password,tmail_list,msg,append,finfunc=None,failfunc=None):
        super().__init__()
        self.fmail=fmail
        self.password=password
        self.tmail_list=tmail_list
        self.msg=msg
        self.append=append

        self.finfunc=finfunc
        self.failfunc=failfunc

    def run(self):
        mailstate = sendEmailSMTP(self.fmail, self.password, self.tmail_list,self.msg, self.append)
        #print(mailstate)
        if '失败' in mailstate:
            if self.failfunc:
                self.failfunc()
            return False
        else:
            if self.finfunc:
                self.finfunc()
            return True

class DCbutton(QtWidgets.QPushButton):
    def __init__(self,parent=None):
        super(DCbutton,self).__init__(parent)
        self.doubleclick=None

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.doubleclick:
            self.doubleclick()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = emailWriter()
    mw = QtWidgets.QWidget()
    win.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())