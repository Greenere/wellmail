# -*- coding: utf-8 -*-

#收件箱模块

#Receiverbox module
#Written by Xin Liu

# Form implementation generated from reading ui file 'receiverForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from re import compile
from UIBrowser import DelThread
from UIBrowser import MsgDialog
from auxFunctions import getRange

class RecieveBoxUi(object):
    def __init__(self,psdlist=None,dpsdlist=None):
        #创建用于收信箱内信件基本信息的Button
        self.checkBox={}
        self.subjectBox={}
        self.dateBox={}
        self.memberBox={}
        self.datas = psdlist if psdlist else []
        self.fmail=''
        self.password=''

        self.accepted=False
        self.allselected=False
        self.cpsd=None
        self.showfunc=None
        self.renewfunc=None
        self.resendfunc=None
        self.delfunc=None
        self.delfailfunc=None
        self.delthread=None
        if self.datas!=[]:
            self.data,self.trans = getRange(self.datas)
            #print('sorted')
        else:
            #print('unsorted')
            self.data=self.datas
            for i in range(len(self.data)):
                self.trans={i:i}
        self.dparsedictlist=dpsdlist
        self.key=None

    def setupUi(self, Form):
        #创建收信箱界面
        Form.setObjectName("Form")
        Form.resize(966, 706)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.upline = QtWidgets.QFrame(Form)
        self.upline.setFrameShape(QtWidgets.QFrame.HLine)
        self.upline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.upline.setObjectName("upline")
        self.gridLayout_2.addWidget(self.upline, 0, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.delete_button = QtWidgets.QPushButton(Form)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.sendto_button = QtWidgets.QPushButton(Form)
        self.sendto_button.setObjectName("sendto_button")
        self.sendto_button.clicked.connect(self.resendClicked)
        self.horizontalLayout.addWidget(self.sendto_button)
        self.renew_button = QtWidgets.QPushButton(Form)
        self.renew_button.setObjectName("change_button")
        self.renew_button.clicked.connect(self.renewClicked)
        self.horizontalLayout.addWidget(self.renew_button)
        self.infolabel=QtWidgets.QLabel(Form)
        self.infolabel.setFixedSize(500,28)
        self.infolabel.setObjectName('info_label')
        self.infolabel.setText('一共有 '+str(len(self.data))+' 封邮件，点击查看')
        self.horizontalLayout.addWidget(self.infolabel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(616, 28, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        self.downline = QtWidgets.QFrame(Form)
        self.downline.setFrameShape(QtWidgets.QFrame.HLine)
        self.downline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.downline.setObjectName("downline")
        self.gridLayout_2.addWidget(self.downline, 2, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("QScrollArea {background-color:rgbf(255,255,255,60);}")
        self.scrollArea.viewport().setStyleSheet("background-color:rgbf(255,255,255,60);")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 922, 625))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 562, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(179, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 6, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 562, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 1, 7, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(179, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 562, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 1, 2, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 562, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 1, 5, 1, 1)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        member_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        member_button.setObjectName("member_button")
        member_button.setFixedSize(300,28)
        self.verticalLayout_2.addWidget(member_button)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 2)
        #print('formed2')
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        date_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        date_button.setObjectName("date_button")
        date_button.setFixedSize(220,28)
        self.verticalLayout_4.addWidget(date_button)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 7, 1, 1)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        subject_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        subject_button.setObjectName("subject_button")
        subject_button.setFixedSize(400,28)
        self.verticalLayout_3.addWidget(subject_button)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 5, 1, 1)
        #print('formed3')
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.checkBoxs = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBoxs.setText("")
        self.checkBoxs.setCheckable(True)
        self.checkBoxs.setObjectName("checkBoxs")
        self.checkBoxs.setFixedSize(28,28)
        self.checkBoxs.toggled.connect(self.choose)

        self.verticalLayout_1.addWidget(self.checkBoxs)
        self.gridLayout.addLayout(self.verticalLayout_1, 0, 0, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        sp = self.space(36, "发件人")
        member_button.setText(_translate("Form", "发件人"+sp))
        sp = self.space(25, "时间")
        date_button.setText(_translate("Form", "时间"+sp))
        sp=self.space(48,'主题')
        subject_button.setText(_translate("Form", "主题"+sp))
        member_button.setFlat(True)
        date_button.setFlat(True)
        subject_button.setFlat(True)
        #print('formed4')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 3, 0, 1, 2)
        spacerItem8 = QtWidgets.QSpacerItem(13, 623, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem8, 3, 2, 1, 1)

        self.retranslateUi(Form)
        #self.data = getRange(self.datas)
        self.delete_button.clicked.connect(lambda: self.delete())
        self.showmail()
        QtCore.QMetaObject.connectSlotsByName(Form)


    def showmail(self):
        #创建显示邮件信息的界面
        for i in range(0,len(self.data)):
            checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            self.checkBox[str(i)] = checkBox
            checkBox.setCheckable(True)
            memberBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.memberBox[str(i)] = memberBox
            subjectBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.subjectBox[str(i)] = subjectBox
            dateBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.dateBox[str(i)] = dateBox
            #print('show1')
            _translate = QtCore.QCoreApplication.translate
            self.checkBox[str(i)].setText("")
            self.checkBox[str(i)].setObjectName("deleteBox" + str(i))
            self.checkBox[str(i)].setFixedSize(28,28)
            self.verticalLayout_1.addWidget(self.checkBox[str(i)])
            #print('show2')
            try:
                text = self.data[i]["from"]
            except:
                text='-'
            #print(text)
            sp = self.space(36, text)
            if len(text) > 36:
                text = text[0:32] + '....'
                sp = ''
                self.memberBox[str(i)].setToolTip(text)
            else:
                self.memberBox[str(i)].setToolTip('')
            self.memberBox[str(i)].setText(text+sp)
            self.memberBox[str(i)].setFlat(True)
            self.memberBox[str(i)].setObjectName("sendBox" + str(i))
            self.memberBox[str(i)].setFixedSize(300,28)
            self.verticalLayout_2.addWidget(self.memberBox[str(i)])
            #print('show3')
            try:
                text=self.data[i]["subject"]
            except:
                text='-'
                pass
            sp=self.space(48,text)
            if len(text)>48:
                text=text[0:44]+'....'
                sp=''
                self.subjectBox[str(i)].setToolTip(text)
            else:
                self.subjectBox[str(i)].setToolTip('')
            self.subjectBox[str(i)].setText(text+sp)
            self.subjectBox[str(i)].setFlat(True)
            self.subjectBox[str(i)].setObjectName("subjectBox" + str(i))
            self.subjectBox[str(i)].setFixedSize(400,28)
            self.verticalLayout_3.addWidget(self.subjectBox[str(i)])

            try:
                text = self.data[i]["date"]
            except:
                text='-'
                pass
            sp = self.space(25, text)
            if len(text) > 25:
                text = text[0:26] + ''
                sp = ''
                self.dateBox[str(i)].setToolTip(text)
            else:
                self.dateBox[str(i)].setToolTip('')
            self.dateBox[str(i)].setText(text+sp)
            self.dateBox[str(i)].setFlat(True)
            self.dateBox[str(i)].setObjectName("dateBox" + str(i))
            self.dateBox[str(i)].setFixedSize(220,28)
            self.verticalLayout_4.addWidget(self.dateBox[str(i)])
            #print('show4')

            #遍历判断Button是否被点击，如果被点击就执行显示邮件的操作
            for key, value in self.subjectBox.items():
                self.clickshow(value, key)

            for key, value in self.dateBox.items():
                self.clickshow(value, key)

            for key, value in self.memberBox.items():
                self.clickshow(value, key)
            #print('showfin')

    def clickshow(self, button, key):
        button.clicked.connect(lambda: self.shows(key))

    def shows(self,key):
        self.cpsd=self.data[int(key)]
        try:
            if self.showfunc:
                self.showfunc()
        except:
            pass

    def getcpsd(self):
        return self.cpsd

    def choose(self,checked):
        if checked:
            self.allselected=True
            for key, value in self.checkBox.items():
                self.checkBox[key].setChecked(True)
        else:
            self.allselected=False
            for key, value in self.checkBox.items():
                self.checkBox[key].setChecked(False)

    def removeAll(self):
        for key,value in self.checkBox.items():
            if value.isChecked():
                self.checkBox[key].close()
                self.memberBox[key].close()
                self.subjectBox[key].close()
                self.dateBox[key].close()

    def delete(self):
        #删除收信箱的邮件
        if len(self.datas)<1:
            return
        if self.delthread:
            if self.delthread.isAlive():
                self.caution(title='删除', text='稍等，正在删除...')
                return
        count=0
        for key,value in self.checkBox.items():
            if value.isChecked():
                count+=1
        if count<1:
            self.caution(title='删除',text='请选择需要删除的邮件')
            return
        self.question(title='删除',text='真的要删除这些邮件吗？')
        if not self.accepted:
            return
        if self.allselected:
            self.question(title='删除',text='真的要完全删除吗？')
            if not self.accepted:
                return
            self.question(title='删除',text='这将删除所有邮件')
            if not self.accepted:
                return
        #print("delete")
        dpsd=[]
        for key,value in self.checkBox.items():
            if value.isChecked():
                self.checkBox[key].close()
                self.memberBox[key].close()
                self.subjectBox[key].close()
                self.dateBox[key].close()
                #print('key removed')
                try:
                    dpsd.append(self.data[int(key)])
                    #print('dpsd appended')
                    dps=self.data.pop(int(key))
                    #print('dps poped')
                    self.dparsedictlist.append(dps)
                    #print('dparselist appended')
                    self.datas.pop(self.trans[int(key)])
                    #print('del poped')
                except:
                    pass

        self.delthread = DelThread(self.fmail, self.password, dpsd)
        self.delthread.delfunc = self.delFinished
        self.delthread.delfailfunc = self.delFailed
        self.delthread.setDaemon(True)
        self.delthread.start()
        self.accepted = False
        self.infolabel.setText('一共有 ' + str(len(self.data)) + ' 封邮件，点击查看')

    def delFinished(self):
        if self.delfunc:
            self.delfunc()

    def delFailed(self):
        if self.delfailfunc:
            self.delfailfunc()

    def resendClicked(self):
        #选择需要转发的邮件，
        count = 0
        for key, value in self.checkBox.items():
            if value.isChecked():
                count += 1
        if count < 1:
            self.caution(title='转发',text='请选择需要转发的邮件')
            return
        curkey=[]
        for key,value in self.checkBox.items():
            if value.isChecked():
                curkey.append(key)
        if curkey!=[] :
            self.key=curkey[0]
            if self.resendfunc:
                self.resendfunc()


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.delete_button.setText(_translate("Form", "删除"))
        self.sendto_button.setText(_translate("Form", "转发"))
        self.renew_button.setText(_translate("Form", "刷新"))

    def renewClicked(self):
        if self.renewfunc:
            self.renewfunc()
        else:
            pass
            #print('renewfunc=None')

    def caution(self,title='啊哦',text='稍等'):
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgBox.setWindowOpacity(0.9)
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.exec()

    def space(self,length,text):
        hanzi_regex = compile(r'[\u4E00-\u9FA5]')
        sp=" " * (round(length) - len(text) - len(hanzi_regex.findall(text)))
        return sp

    def question(self,title='啊哦',text='确定？'):
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
