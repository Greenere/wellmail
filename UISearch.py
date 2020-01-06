# -*- coding: utf-8 -*-

#搜索模块

#Search module
#Written by Xin Liu

# Form implementation generated from reading ui file 'search.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from re import compile

class SearchUi(object):
    def __init__(self,data=None,item=None,keyword=None):
        #待查找的邮件
        self.data =data if data else ''
        self.keyword=keyword if keyword else ''

        #创建用于显示搜索结果的Button
        self.deleteBox={}
        self.sendBox = {}
        self.subjectBox = {}
        self.dateBox = {}
        self.line=[]
        self.item=item if item else 'date'

        self.showfunc=None
        self.cpsd=None
        self.sum=None

    def setupUi(self, Form):
        #创建搜索界面
        Form.setObjectName("Form")
        Form.resize(1023, 667)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.deleteallbutton = QtWidgets.QPushButton(Form)
        self.deleteallbutton.setObjectName("deleteallbutton")

        self.deleteallbutton.clicked.connect(lambda: self.deleteall())

        self.horizontalLayout_3.addWidget(self.deleteallbutton)
        self.infolabel=QtWidgets.QLabel()
        self.infolabel.setFixedSize(1000,28)
        self.horizontalLayout_3.addWidget(self.infolabel)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 605, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(866, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.memberarea = QtWidgets.QScrollArea(Form)
        self.memberarea.setWidgetResizable(True)
        self.memberarea.setObjectName("memberarea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 969, 606))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.memberarea.setStyleSheet("QScrollArea {background-color:rgbf(255,255,255,60);}")
        self.memberarea.viewport().setStyleSheet("background-color:rgbf(255,255,255,60);")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.gridLayout.addLayout(self.verticalLayout_1, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # self.sendbutton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        self.gridLayout.addLayout(self.verticalLayout_2, 1, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 4, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 6, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 517, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 2, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 517, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 2, 2, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 514, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 2, 4, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 517, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 2, 6, 1, 1)
        self.memberarea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.memberarea, 1, 1, 1, 2)


        deletelabel=QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sendlabel=QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        subjectlabel=QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        datelabel=QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        deletelabel.setFlat(True)
        deletelabel.setFixedSize(50,28)
        sendlabel.setFlat(True)
        sendlabel.setFixedSize(300,28)
        subjectlabel.setFlat(True)
        subjectlabel.setMinimumSize(400,28)
        datelabel.setFlat(True)
        datelabel.setFixedSize(150,38)
        self.verticalLayout_1.addWidget(deletelabel)
        self.verticalLayout_2.addWidget(sendlabel)
        self.verticalLayout_3.addWidget(subjectlabel)
        self.verticalLayout_4.addWidget(datelabel)

        _translate = QtCore.QCoreApplication.translate
        deletelabel.setText(_translate("Form", "去除"))
        sp = self.space(34, '发件人')
        sendlabel.setText(_translate("Form", "发件人"+sp))
        sp = self.space(36, '主题')
        subjectlabel.setText(_translate("Form", "主题"+sp))
        datelabel.setText(_translate("Form", "时间"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.getSearch()

    def getSearch(self):
        '''
        可以选择对邮件的subject,from,date，content进行search
        :param  keyword:查找的关键字
        :param  item:需要查找的关键字对应的key
        :return:  line：查找到的对应邮件编号列表
        (print对应的邮件编号，及查找邮件对应的key的value值)
        '''
        data=self.data
        # keyword为查找的关键字
        keyword = self.keyword
        # item为对应关键字所属的key
        item = self.item

        for values in range(0, len(data)):
            if item!='content':
                if keyword in data[values][item]:
                    self.line.append(values)
            else:
                if keyword in data[values]['payload'][item+'0']:
                    self.line.append(values)

        self.sum=len(self.line)
        self.showmail()


    def showmail(self):
        #创建Button用于显示搜索结果
        transdict = {'from':'发件人', 'subject':'主题', 'date':'时间', 'content':'正文'}
        self.infolabel.setText('关键词:'+'\"'+self.keyword+'\"'+'('+transdict[self.item]+')'+' 共找到 '+str(self.getsum())+'封相关邮件')
        for i in range(0,len(self.line)):
            deleteBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.deleteBox[str(i)] = deleteBox
            sendBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.sendBox[str(i)] = sendBox
            subjectBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.subjectBox[str(i)] = subjectBox
            dateBox = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.dateBox[str(i)] = dateBox

            temp=QtWidgets.QPushButton()

            _translate = QtCore.QCoreApplication.translate
            self.deleteBox[str(i)].setText("×")
            self.deleteBox[str(i)].setFlat(True)
            self.deleteBox[str(i)].setObjectName("deleteBox" + str(i))
            self.deleteBox[str(i)].setFixedSize(50,28)
            self.verticalLayout_1.addWidget(self.deleteBox[str(i)])

            sp=self.space(34,self.data[self.line[i]]['from'])
            self.sendBox[str(i)].setText(self.data[self.line[i]]['from']+sp)
            if len(self.data[self.line[i]]['from'])>34:
                self.sendBox[str(i)].setText(self.data[self.line[i]]['from'][0:30]+'....')
                self.sendBox[str(i)].setToolTip(self.data[self.line[i]]['from'])
            self.sendBox[str(i)].setFlat(True)
            self.sendBox[str(i)].setObjectName("sendBox" + str(i))
            self.sendBox[str(i)].setFixedSize(300,28)
            self.verticalLayout_2.addWidget(self.sendBox[str(i)])

            sp =self.space(36, self.data[self.line[i]]['subject'])
            self.subjectBox[str(i)].setFlat(True)
            self.subjectBox[str(i)].setObjectName("subjectBox" + str(i))
            self.subjectBox[str(i)].setMinimumSize(400, 28)
            self.subjectBox[str(i)].setText(self.data[self.line[i]]['subject']+sp)
            if len(self.data[self.line[i]]['subject'])>34:
                self.subjectBox[str(i)].setText(self.data[self.line[i]]['subject'][0:30]+'....')
                self.subjectBox[str(i)].setToolTip(self.data[self.line[i]]['subject'])
            self.verticalLayout_3.addWidget(self.subjectBox[str(i)])

            self.dateBox[str(i)].setText(self.data[self.line[i]]['date'][:16])
            self.dateBox[str(i)].setFlat(True)
            self.dateBox[str(i)].setFixedSize(150,28)
            self.dateBox[str(i)].setObjectName("dateBox" + str(i))
            self.verticalLayout_4.addWidget(self.dateBox[str(i)])

        #判断Button是否被点击
        for key, value in self.deleteBox.items():
                self.clickdelete(value, key)

        for key, value in self.sendBox.items():
                self.clickshow(value,key)

        for key, value in self.subjectBox.items():
                self.clickshow(value,key)

        for key, value in self.dateBox.items():
                self.clickshow(value,key)

    def clickdelete(self, button, key):
        #Button被点击，就执行删除的操作
        button.clicked.connect(lambda: self.delete(key))

    def clickshow(self, button, key):
        # 搜索Button被点击，就执行显示结果的操作
        button.clicked.connect(lambda: self.shows(key))

    def shows(self,key):
        self.cpsd=self.data[self.line[int(key)]]
        if self.showfunc:
            self.showfunc()
        #print(self.data[self.line[int(key)]])
        # print("Yes")

    def getcpsd(self):
        return self.cpsd

    def getsum(self):
        if self.sum:
            return self.sum
        else:
            return 0

    def deleteall(self):
        #删除全部的搜索结果
        for key,value in self.deleteBox.items():
            value.close()
        for key,value in self.sendBox.items():
            value.close()
        for key,value in self.subjectBox.items():
            value.close()
        for key,value in self.dateBox.items():
            value.close()

    def delete(self, key):
        #print("delete")
        self.deleteBox[key].close()
        self.sendBox[key].close()
        self.subjectBox[key].close()
        self.dateBox[key].close()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.deleteallbutton.setText(_translate("Form", "全部去除"))

    def space(self,length,text):
        hanzi_regex = compile(r'[\u4E00-\u9FA5]')
        sp=" " * (round(length) - len(text) - len(hanzi_regex.findall(text)))
        return sp
