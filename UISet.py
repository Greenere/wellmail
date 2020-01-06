# -*- coding: utf-8 -*-

#设置界面

#Set module
#Written by Haoyang Li

# Form implementation generated from reading ui file 'setUi.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from UIBrowser import MsgDialog
from os import getcwd
import sys

class SetUi(object):
    #设置界面
    def __init__(self,fmail='wellmail@well.com',password='password',backpath=getcwd()):
        #设置状态
        self.accepted=False
        self.append=False#是否同步发件
        self.new=True#是否只接收最新邮件
        #用户信息
        self.fmail=fmail
        self.password=password
        self.backpath=backpath
        #留给外部函数的接口
        self.newfunc=None
        self.appendfunc=None
        self.fmailfunc=None
        self.codefunc=None
        self.backpathfunc=None

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(950, 650)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 0, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(925, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 4)
        #同步收发与刷新模式部分
        self.lgetsend = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lgetsend.sizePolicy().hasHeightForWidth())
        self.lgetsend.setSizePolicy(sizePolicy)
        self.lgetsend.setObjectName("lgetsend")
        self.gridLayout.addWidget(self.lgetsend, 2, 0, 1, 1)
        #同步收发和刷新模式点选框
        self.cbappend = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbappend.sizePolicy().hasHeightForWidth())
        self.cbappend.setSizePolicy(sizePolicy)
        self.cbappend.setObjectName("cbappend")
        self.cbappend.toggled.connect(self.appendChecked)
        self.gridLayout.addWidget(self.cbappend, 2, 1, 1, 1)
        self.cbnew = QtWidgets.QCheckBox(Form)
        self.cbnew.setObjectName("cbnew")
        self.cbnew.toggled.connect(self.newChecked)
        self.cbnew.setChecked(self.new)
        self.gridLayout.addWidget(self.cbnew, 3, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(586, 508, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 11, 1)
        spacerItem2 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 3)
        #切换用户部分
        self.lfmail = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lfmail.sizePolicy().hasHeightForWidth())
        self.lfmail.setSizePolicy(sizePolicy)
        self.lfmail.setObjectName("lfmail")
        self.gridLayout.addWidget(self.lfmail, 5, 0, 1, 1)
        self.bfmail = QtWidgets.QPushButton(Form)
        self.bfmail.setMinimumSize(QtCore.QSize(250, 0))
        self.bfmail.setMaximumSize(QtCore.QSize(280, 28))
        self.bfmail.setObjectName("bfmail")
        self.bfmail.setFlat(True)
        self.bfmail.clicked.connect(self.bfmailClicked)
        self.gridLayout.addWidget(self.bfmail, 5, 1, 1, 2)
        self.lcode = QtWidgets.QLabel(Form)
        self.lcode.setObjectName("lcode")
        self.gridLayout.addWidget(self.lcode, 6, 0, 1, 1)
        self.bcode = QtWidgets.QPushButton(Form)
        self.bcode.setMinimumSize(QtCore.QSize(250, 0))
        self.bcode.setMaximumSize(QtCore.QSize(280, 28))
        self.bcode.setObjectName("bcode")
        self.bcode.setFlat(True)
        self.bcode.clicked.connect(self.bcodeClicked)
        self.gridLayout.addWidget(self.bcode, 6, 1, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 7, 0, 1, 3)
        #背景图片部分（不能切换，可以显示路径）
        self.lback = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lback.sizePolicy().hasHeightForWidth())
        self.lback.setSizePolicy(sizePolicy)
        self.lback.setObjectName("lback")
        self.gridLayout.addWidget(self.lback, 8, 0, 1, 1)
        self.bback = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(250)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bback.sizePolicy().hasHeightForWidth())
        self.bback.setSizePolicy(sizePolicy)
        self.bback.setObjectName("bback")
        self.bback.setFlat(True)
        self.bback.clicked.connect(self.bbackClicked)
        self.gridLayout.addWidget(self.bback, 8, 1, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 9, 0, 1, 3)
        spacerItem5 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 10, 0, 1, 3)
        spacerItem6 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 11, 0, 1, 3)
        spacerItem7 = QtWidgets.QSpacerItem(329, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 12, 0, 1, 3)
        spacerItem8 = QtWidgets.QSpacerItem(20, 248, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 13, 2, 1, 1)
        #初始化
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "设置"))
        self.lgetsend.setText(_translate("Form", "收发设置："))
        self.cbappend.setText(_translate("Form", "同步删发"))
        self.cbnew.setText(_translate("Form", "只收取最新邮件"))
        self.lfmail.setText(_translate("Form", "发件账户："))
        self.bfmail.setText(_translate("Form", self.fmail+' '*(30-len(self.fmail))))
        self.lcode.setText(_translate("Form", "密码："))
        self.bcode.setText(_translate("Form", '●'*len(self.password)+' '*(20-len(self.password))))
        self.lback.setText(_translate("Form", "背景图片："))
        self.bback.setText(_translate("Form", self.backpath))
        self.bback.setToolTip(self.backpath)

    def renew(self):
        #刷新设置界面
        self.lfmail.setText("发件账户：")
        self.bfmail.setText(self.fmail+' '*(30-len(self.fmail)))
        self.lcode.setText("密码：")
        self.bcode.setText('●' * len(self.password)+' '*(20-len(self.password)))
        self.lback.setText( "背景图片：")
        self.bback.setText(self.backpath)
        self.bback.setToolTip(self.backpath)
    #确认框函数
    def magAccepted(self):
        self.accepted=True

    def msgRejected(self):
        self.accepted=False

    def newChecked(self):
        #刷新模式点选
        if self.cbnew.isChecked():
            self.new=True
        else:
            self.caution(title='收取设置',text='不选这一项，刷新时会获取所有邮件，用时较长')
            self.new=False
        if self.newfunc:
            self.newfunc()

    def appendChecked(self):
        #同步发件点选
        if self.cbappend.isChecked():
            self.caution(title='发送设置', text='选择这一项，发信时会同步信件到服务器‘已发送’文件夹')
            self.append=True
        else:
            self.append=False
        if self.appendfunc:
            self.appendfunc()

    def bfmailClicked(self):
        #切换账户函数
        #点击账户切换账户
        if self.fmailfunc:
            self.fmailfunc()

    def bcodeClicked(self):
        #点击密码也是切换账户
        self.bfmailClicked()
        if self.codefunc:
            self.codefunc()

    def bbackClicked(self):
        if self.backpathfunc:
            self.backpathfunc()

    def caution(self,title='啊哦',text='稍等'):
        #提示框
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgBox.setWindowOpacity(0.9)
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QWidget()
    mw = SetUi()
    mw.setupUi(win)
    win.show()
    sys.exit(app.exec_())
