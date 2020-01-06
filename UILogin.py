# -*- coding: utf-8 -*-

#登录界面

#Login Interface
#Written by Haoyang Li

# Form implementation generated from reading ui file 'loginUi.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from re import compile
import imaplib
import smtplib
from threading import Thread

class LoginUi(object):
    def __init__(self):
        #留给外部函数的接口
        self.bokfunc=None
        self.onlyrecievefunc=None
        #用户账号和密码
        self.fmail=''
        self.password=''

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(908, 666)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        #功能部分
        self.funcpart = QtWidgets.QGridLayout()
        self.funcpart.setObjectName("gridLayout")
        #欢迎标签
        self.lwel = QtWidgets.QLabel(Form)
        self.lwel.setObjectName("lwel")
        self.funcpart.addWidget(self.lwel, 0, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.funcpart.addItem(spacerItem2, 1, 0, 1, 3)
        #邮箱标签与邮箱输入框
        self.lfmail = QtWidgets.QLabel(Form)
        self.lfmail.setObjectName("lfmail")
        self.funcpart.addWidget(self.lfmail, 2, 0, 1, 1)
        self.infmail = QtWidgets.QLineEdit(Form)
        self.infmail.setMinimumSize(QtCore.QSize(260, 28))
        self.infmail.setMaximumSize(QtCore.QSize(260, 28))
        self.infmail.setObjectName("infmail")
        self.infmail.setText(self.fmail)
        self.funcpart.addWidget(self.infmail, 2, 1, 1, 2)
        #密码标签与密码输入框
        self.lpassword = QtWidgets.QLabel(Form)
        self.lpassword.setObjectName("lpassword")
        self.funcpart.addWidget(self.lpassword, 3, 0, 1, 1)
        self.inpassword = QtWidgets.QLineEdit(Form)
        self.inpassword.setMinimumSize(QtCore.QSize(260, 28))
        self.inpassword.setMaximumSize(QtCore.QSize(260, 28))
        self.inpassword.setObjectName("inpassword")
        self.inpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inpassword.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.inpassword.setText(self.password)
        self.funcpart.addWidget(self.inpassword, 3, 1, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.funcpart.addItem(spacerItem3, 4, 0, 1, 3)
        #确定按钮
        self.bok = QtWidgets.QPushButton(Form)
        self.bok.setMinimumSize(QtCore.QSize(90, 28))
        self.bok.setMaximumSize(QtCore.QSize(90, 28))
        self.bok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bok.setObjectName("bok")
        self.bok.clicked.connect(self.bokClicked)
        self.funcpart.addWidget(self.bok, 5, 2, 1, 1)
        self.gridLayout_2.addLayout(self.funcpart, 1, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(252, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 197, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem5, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(488, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        #制作者标签按钮（右下角，无功能）
        self.babout = QtWidgets.QPushButton(Form)
        self.babout.setFlat(True)
        self.babout.setObjectName("babout")
        self.horizontalLayout.addWidget(self.babout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 3)
        #初始化
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "login"))
        self.lwel.setText(_translate("Form", "欢迎使用WELLMAIL邮箱\n请输入邮箱和密码"))
        self.lfmail.setText(_translate("Form", "邮箱："))
        self.lpassword.setText(_translate("Form", "密码："))
        self.bok.setText(_translate("Form", "确定"))
        self.babout.setText(_translate("Form", "2018年12月 华中科技大学电信学院 李皓阳 刘鑫 王韵"))

    def bokClicked(self):
        #确认按钮功能实现
        if self.infmail.text() and self.inpassword.text():
            #邮件正则表达式，用于验证邮件是否格式正确
            email_regex=compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
            if email_regex.findall(self.infmail.text()):
                fmail=self.infmail.text()
                password=self.inpassword.text()
                #联网检测是否能够连接SMTP和IMAP4服务器（否则无法使用）
                if True:#not os.path.exists(os.getcwd()+'\\user\\user_maildata\\'+self.fmail):
                    valid=self.validate(fmail,password)
                    if not valid:
                        self.caution(text='无法建立连接，原因可能是：\n①网络未连接\n②账户或密码错误\n③未开启IMAP4\SMTP服务')
                        return
                self.fmail=fmail
                self.password=password
                if self.bokfunc:
                    self.bokfunc()
                else:
                    pass
                    #print('bokfunc=None')
            else:
                self.caution(text='邮箱格式不正确呢    ')
        else:
            self.caution(text='请输入邮箱和密码    ')

    def onlyRecieve(self):
        #有时只能连接IMAP4服务器，因此只能接收邮件
        self.caution(title='登陆',text='无法连接SMTP，但可以接收邮件')
        if self.onlyrecievefunc:
            self.onlyrecievefunc()

    def validate(self,fmail,password):
        #验证函数
        #联网验证线程
        vps = ValidateThread(fmail, password, self.validFinished,self.onlyRecieve)
        vps.start()
        #验证提示框
        self.validbox = QMessageBox(QMessageBox.NoIcon, '稍等', '正在验证邮箱...    ')
        self.validbox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        self.validbox.setWindowOpacity(0.9)
        self.validbox.setDisabled(True)
        self.validbox.setWindowFlags(QtCore.Qt.SubWindow)
        self.validbox.exec()
        valid = vps.run()
        return valid

    def validFinished(self):
        #验证结束后关闭提示框
        self.validbox.setDisabled(False)
        self.validbox.close()

    def caution(self,title='啊哦',text='稍等'):
        #提示框
        msgBox = QMessageBox(QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgBox.setWindowOpacity(0.9)
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.exec()


class ValidateThread(Thread):
    #验证线程
    def __init__(self,fmail,password,finfunc=None,onlyimapfunc=None):
        super().__init__()
        self.fmail=fmail
        self.password=password
        self.valid=True
        #留给外部函数的接口
        self.finfunc=finfunc
        self.onlyimapfunc=onlyimapfunc

    def run(self):
        self.valid=self.validate(self.fmail,self.password)
        return self.valid

    def validate(self,fmail,password):
        #验证功能实现
        #先试图连接IMAP4服务，否则直接验证失败
        #再试图连接SMTP服务，否则为只接收模式
        try:
            mail_host = 'imap.' + fmail.split('@')[-1]
            imapObj = imaplib.IMAP4_SSL(mail_host)
            #print('connected imap')
            #print(fmail,password)
            s=imapObj.login(fmail, password)
            #print('logged imap',s)
            imapObj.logout()
            try:
                mail_host ='smtp.'+fmail.split('@')[-1]
                smtpObj = smtplib.SMTP_SSL(mail_host, 465)
                #print('connected smtp')
                s=smtpObj.login(fmail, password)
                #print('logged smtp',s)
                smtpObj.close()
            except:
                if self.onlyimapfunc:
                    self.onlyimapfunc()
            valid=True
        except:
            valid=False
        if self.finfunc:
            self.finfunc()
        return valid




