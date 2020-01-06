# -*- coding: utf-8 -*-

#通讯录模块

#Contact module
#Written by Xin Liu

# Form implementation generated from reading ui file 'memberForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from re import compile
import os
from UIBrowser import MsgDialog

class MemberUi(object):
    def __init__(self,username='well'):
        self.username=username
        #创建保存用户信息的文件
        self.filename='user\\user_info\\'+self.username+'\\member.txt'
        if not os.path.exists(os.getcwd()+'\\user\\user_info\\'+self.username):
            os.system('mkdir '+os.getcwd()+'\\user\\user_info\\'+self.username)
        if not os.path.exists(self.filename):
            fp=open(self.filename,'wb')
            fp.close()
        #打开文件，读取文件内的用户名及邮箱地址信息
        with open(self.filename,'r+') as file_object:
            lines=file_object.read()
            if len(lines)==0:
               self.line={}
            else:
               self.line = eval(lines)
        self.line={} if not self.line else self.line
        #3个字典：保存创建的，用于显示用户信息的Button
        self.checkBox={}
        self.nmblist={}
        self.emblist={}
        self.number=0
        self.accepted=False

        self.writefunc=None
        self.writeinfo=None

        self.cname=''
        self.cemail=''


    def setupUi(self, Form):
        #创建通讯录界面
        Form.setObjectName("Form")
        Form.resize(950, 600)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.deleteallbutton = QtWidgets.QPushButton(Form)
        self.deleteallbutton.setObjectName("deleteallbutton")
        self.deleteallbutton.clicked.connect(lambda: self.deleteall())
        self.horizontalLayout_3.addWidget(self.deleteallbutton)
        self.infolabel = QtWidgets.QLabel()
        self.infolabel.setFixedSize(300, 28)
        self.horizontalLayout_3.addWidget(self.infolabel)
        self.infolabel.setText('点击联系人发送邮件，点击邮箱修改联系人')
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(342, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.nameedit = QtWidgets.QLineEdit(Form)
        self.nameedit.setObjectName("nameedit")
        self.horizontalLayout_2.addWidget(self.nameedit)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.emailedit = QtWidgets.QLineEdit(Form)
        self.emailedit.setObjectName("emailedit")
        self.horizontalLayout_2.addWidget(self.emailedit)
        self.addbutton = QtWidgets.QPushButton(Form)
        self.addbutton.setMaximumSize(QtCore.QSize(50, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.addbutton.setFont(font)
        self.addbutton.setObjectName("addbutton")
        self.horizontalLayout_2.addWidget(self.addbutton)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 608, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.memberarea = QtWidgets.QScrollArea(Form)
        self.memberarea.setWidgetResizable(True)
        self.memberarea.setObjectName("memberarea")
        self.memberarea.setStyleSheet("QScrollArea {background-color:rgbf(255,255,255,60);}")
        self.memberarea.viewport().setStyleSheet("background-color:rgbf(255,255,255,60);")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 938, 606))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.scrollAreaWidgetContents.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("img/backgroundEmailWriter.png")))
        self.scrollAreaWidgetContents.setPalette(window_pale)
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem2 = QtWidgets.QSpacerItem(244, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)

        spacerItem3 = QtWidgets.QSpacerItem(243, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 3, 1, 1)

        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.gridLayout.addLayout(self.verticalLayout_1, 1, 0, 1, 1)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.gridLayout.addLayout(self.verticalLayout_2, 1, 2, 1, 1)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.gridLayout.addLayout(self.verticalLayout_3, 1, 4, 1, 1)

        spacerItem4 = QtWidgets.QSpacerItem(20, 517, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 2, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 517, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 2, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 517, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 2, 4, 1, 1)
        self.memberarea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.memberarea, 1, 1, 1, 3)

        _translate = QtCore.QCoreApplication.translate
        checkBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        namebutton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        emailbutton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        checkBox.setText("删除")
        checkBox.setFixedSize(50,28)
        namebutton.setFlat(True)
        sp = self.space(60, "邮箱")
        emailbutton.setText("邮箱"+sp)
        emailbutton.setFixedSize(600,28)
        checkBox.setFlat(True)
        sp=self.space(30,"联系人名称")
        namebutton.setText("联系人名称"+sp)
        namebutton.setFixedSize(300,28)
        emailbutton.setFlat(True)
        self.verticalLayout_1.addWidget(checkBox)
        self.verticalLayout_2.addWidget(namebutton)
        self.verticalLayout_3.addWidget(emailbutton)

        #创建3组用于显示用户信息的Button
        for i in range(0, len(self.line)):
            checkBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            checkBox.setFixedSize(50,28)
            self.checkBox[str(i)] = checkBox
            namebutton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            namebutton.setFixedSize(300,28)
            self.nmblist[str(i)] = namebutton
            emailbutton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            emailbutton.setFixedSize(600,28)
            self.emblist[str(i)] = emailbutton

        i = 0
        for key, value in self.line.items():
            _translate = QtCore.QCoreApplication.translate
            self.checkBox[str(i)].setText("×")
            self.checkBox[str(i)].setFlat(True)
            self.checkBox[str(i)].setObjectName("checkBox" + str(i))
            self.verticalLayout_1.addWidget(self.checkBox[str(i)])

            name = key.strip(' ')
            sp=self.space(30,name)
            self.nmblist[str(i)].setFlat(True)
            self.nmblist[str(i)].setObjectName("pushButton" + str(i))
            self.verticalLayout_2.addWidget(self.nmblist[str(i)])
            self.nmblist[str(i)].setText(_translate("Form", name+sp))

            email=value.strip(' ')
            sp = self.space(60, email)
            self.emblist[str(i)].setFlat(True)
            self.emblist[str(i)].setObjectName("pushButton_3" + str(i))
            self.verticalLayout_3.addWidget(self.emblist[str(i)])
            self.emblist[str(i)].setText(_translate("Form", email+sp))
            i = i + 1

        #遍历判断是否有Button被点击
        for key, value in self.checkBox.items():
            self.click(value,key)

        for key, value in self.nmblist.items():
            self.nmClicked(value,key)

        for key,value in self.emblist.items():
            self.rename(value,key)

        self.addbutton.clicked.connect(lambda: self.addmember())
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def click(self, button, key):
        #如果删除Button被点击，就执行删除函数
        button.clicked.connect(lambda: self.delete(key))

    def nmClicked(self,button,key):
        #如果用户名Button被点击，就执行写信函数
        button.clicked.connect(lambda: self.write(key))

    def rename(self,button,key):
        # 如果邮箱Button被点击，就执行修改用户信息的函数
        button.clicked.connect(lambda: self.name(key))

    def name(self,key):
        #修改用户信息（用户名及邮箱地址）
        #print('edit')
        try:
            self.cname=self.nmblist[key].text().strip(' ')
            self.cemail=self.line[self.cname]
        except:
            pass
        oldname=self.cname
        self.question(title='编辑该联系人',mode=True)
        if self.accepted:
            email_regex = compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
            if len(self.cname) == 0 or len(self.cemail) == 0:
                self.caution(title='添加', text='用户名和邮箱没填')
                return
            elif (self.judge()):
                self.caution(title='添加', text='这个联系人已经有了')
                return
            elif (email_regex.findall(self.cemail) == []):
                self.caution(title='添加', text='邮箱格式不正确')
                return
            else:
                sp=self.space(30,self.cname)
                self.nmblist[key].setText(self.cname+sp)
                sp=self.space(60,self.cemail)
                self.emblist[key].setText(self.cemail+sp)
                self.line[self.cname]=self.cemail
            try:
                self.line.pop(oldname)
                #print(self.line[self.cname])
            except:
                pass
            try:
                self.line[self.cname]
            except:
                self.line[self.cname]=self.cemail
            try:
                with open(self.filename, 'w') as file_object:
                    file_object.write(str(self.line))
            except:
                pass

    def write(self,key):
        #跳转到写信界面，进行写信操作
        try:
            name=self.nmblist[key].text().strip(' ')
            email=self.line[name]
        except:
            name=self.cname
            email=self.cemail
        #print(name,email)
        self.writeinfo=(name,email)
        if self.writefunc:
            self.writefunc()

    def judge(self):
        #添加用户时，判断用户是否已存在
        jd=False
        for key1, value1 in self.nmblist.items():
            for key, value in self.emblist.items():
                if self.nameedit.text()==value1.text() and self.emailedit.text()==value.text():
                    jd= True
                if self.cname==value1.text() and self.cemail==value.text():
                    jd= True
        return jd

    def addmember(self):
        #点击添加用户Button，创建新的Button用于显示新用户的信息
        added=False
        email_regex = compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
        if len(self.nameedit.text())==0 or len(self.emailedit.text())==0:
            self.caution(title='添加',text='用户名和邮箱还没填')
            #print('警告： '+'用户名或者邮箱不能为空')
        elif(self.judge()):
            self.caution(title='添加',text='这个联系人已经有了')
            #print("用户已存在，请重新输入！")
        elif(email_regex.findall(self.emailedit.text())==[]):
            self.caution(title='添加',text='邮箱格式不正确')
        else:
            _translate = QtCore.QCoreApplication.translate
            checkBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)

            checkBox.setText("×")
            checkBox.setFlat(True)
            checkBox.setFixedSize(50,28)
            self.verticalLayout_1.addWidget(checkBox)

            name=self.nameedit.text().strip(' ')
            sp = self.space(30, name)
            pushButton.setFlat(True)
            self.verticalLayout_2.addWidget(pushButton)
            pushButton.setText(_translate("Form", name+sp))
            #print(pushButton.text())

            email=self.emailedit.text().strip(' ')
            sp = self.space(60, email)
            pushButton_3.setFlat(True)
            self.verticalLayout_3.addWidget(pushButton_3)
            pushButton_3.setText(_translate("Form", email+sp))

            with open(self.filename, 'w')as file_object:
                self.line[self.nameedit.text()]=self.emailedit.text()
                file_object.write(str(self.line))


            self.nameedit.setText("")
            self.emailedit.setText("")

            self.checkBox["add" + str(self.number)] = checkBox
            checkBox.setObjectName("Box" + str(self.number))
            self.nmblist["add" + str(self.number)] = pushButton
            pushButton.setObjectName("Button" + str(self.number))
            self.emblist["add" + str(self.number)] = pushButton_3
            pushButton_3.setObjectName("Button_3" + str(self.number))
            # checkBox.clicked.connect(lambda: self.delete("add" + str(self.number)))
            self.number = self.number + 1

            for key, value in self.checkBox.items():
                self.click(value, key)

            for key, value in self.nmblist.items():
                self.nmClicked(value, key)

            for key, value in self.emblist.items():
                self.rename(value, key)

            added=True
        return added

    def delete(self, key):
        #删除用户
        self.question(title='删除',text='真的要删除该联系人吗？')
        if not self.accepted:
            return

        try:
            #print(self.filename)
            #print('try del')
            #print(self.nmblist[key].text())
            dk=self.nmblist[key].text().strip(' ')
            self.checkBox[key].close()
            self.nmblist[key].close()
            self.emblist[key].close()

            self.line.pop(dk)

            with open(self.filename, 'w') as file_object:
                file_object.write(str(self.line))

        except:
            #print('try failed')
            pass

    def deleteall(self):
        #将用户全部删除
        self.question(title='全部删除',text='警告：将删除所有联系人')
        if not self.accepted:
            return
        self.question(title='全部删除？',text='真的会删除所有联系人哦')
        if not self.accepted:
            return
        self.question(title='全部删除？？', text='确定要清空吗？')
        if not self.accepted:
            return
        for key, value in self.checkBox.items():
            self.checkBox[key].setText("")
            self.checkBox[key].close()
        for key, value in self.nmblist.items():
            self.nmblist[key].setText("")
            self.nmblist[key].close()
        for key, value in self.emblist.items():
            self.emblist[key].setText("")
            self.emblist[key].close()

        with open(self.filename, 'w')as file_object:
            file_object.write('')
            file_object.close()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.deleteallbutton.setText(_translate("Form", "全部删除"))
        self.label_5.setText(_translate("Form", "用户名"))
        self.label_4.setText(_translate("Form", "邮箱"))
        self.addbutton.setText(_translate("Form", "添加"))

    def caution(self,title='啊哦',text='稍等'):
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgBox.setWindowOpacity(0.9)
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.exec()

    def question(self,title='啊哦',text='确定？',mode=False):
        if mode:
            msgBox = QtWidgets.QDialog()
            msgDia = MsgDialog()
            msgDia.setupUi(msgBox)
            msgDia.uplabel.setText('联系人')
            msgDia.downlabel.setText('邮箱')
            msgDia.upinput.setText(self.cname)
            msgDia.downinput.setText(self.cemail)
            msgDia.buttonBox.accepted.connect(self.msgAccepted)
            msgDia.buttonBox.rejected.connect(self.msgRejected)
            msgBox.setWindowTitle(title)
            msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgBox.resize(200, 50)
            msgBox.exec()
            if self.accepted:
                self.cname=msgDia.upinput.text()
                self.cemail=msgDia.downinput.text()
        else:
            msgBox =QtWidgets.QDialog()
            msgDia=MsgDialog()
            msgDia.setupUi(msgBox)
            msgDia.upinput.close()
            msgDia.downinput.close()
            msgDia.downlabel.close()
            msgDia.uplabel.setText(text)
            msgDia.buttonBox.accepted.connect(self.msgAccepted)
            msgDia.buttonBox.rejected.connect(self.msgRejected)
            msgBox.setWindowTitle(title)
            msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgBox.resize(200,50)
            msgBox.exec()

    def msgAccepted(self):
        self.accepted=True

    def msgRejected(self):
        self.accepted=False

    def space(self,length,text):
        hanzi_regex = compile(r'[\u4E00-\u9FA5]')
        sp=" " * (round(length) - len(text) - len(hanzi_regex.findall(text)))
        return sp

