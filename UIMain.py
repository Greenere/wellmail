# -*- coding: utf-8 -*-
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from UIBrowser import MailBrowser
from UIBrowser import MsgDialog
from emailRetriever import *
from re import compile
from UILogin import LoginUi,ValidateThread
from UIWriter import emailWriter
from UISet import SetUi
from UISearch import SearchUi
from UIContact import MemberUi
from UIReceiver import RecieveBoxUi
from auxFunctions import weather

class MainUi(object):
    #主界面
    def __init__(self):
        #状态
        self.accepted=False
        self.first=True
        self.append=False
        self.renewing=False
        self.new=True
        self.delsync=True
        #初始标签窗口和标签窗口字典
        self.starttab=self.startTab()
        self.tabdict={}
        #标签窗口计数
        self.tabcount=1
        #上方提示信息
        self.infotext=''
        #空邮件
        self.emptypsd={'subject':'-',
                       'from':'-',
                       'to':'-',
                       'date':'-',
                       'payload':{'content0':'-'},
                       'file':{'filename':[]},
                       'flag':'Empty'}
        self.emptypsd['subject']='欢迎使用WELLMAIL邮箱'
        self.emptypsd['from']='WELLMAIL<well@wellmail.com>'
        self.emptypsd['to']='WELLMAILUSER'
        self.emptypsd['payload']['content0']='欢迎使用WELLMAIL邮箱\n（此邮件为示例邮件,不在您的邮箱中，只作示例）'
        #邮件列表
        self.parsedictlist=[]
        self.parsedictlist.append(self.emptypsd)
        self.dparsedictlist=[]#已删除邮件列表
        #用户信息
        self.username=''
        self.fmail=''#账户
        self.password=''#密码
        self.sender = ''  # 发件名称
        #搜索信息（搜索关键字）
        self.searchitem= '发件人'
        #回复转发信息
        self.subject=None
        self.content=None
        self.tmail=None
        self.time=None
        self.replyinfo=[]
        #读取本地邮件线程
        self.readthread=None
        #刷新线程和刷新标志
        self.renewthread=None
        self.renewed=False
        #收件箱标签窗口
        self.rbcan=None
        self.rbtab=None
        #背景图片路径
        self.backpath=os.getcwd()+'\\'+'img\\background.png'


    def setupUi(self, Form):
        #窗口设置
        Form.setObjectName("Form")
        Form.resize(1200, 600)
        Form.setMaximumSize(1200,800)
        self.mainlayout = QtWidgets.QGridLayout(Form)
        self.mainlayout.setObjectName("mainlayout")
        #发件名称（可双击编辑）与发件地址（双击可以复制）信息
        self.userlayout = QtWidgets.QGridLayout()
        self.userlayout.setObjectName("userlayout")
        self.lusername = QtWidgets.QLabel(Form)
        self.lusername.setMinimumSize(QtCore.QSize(100, 28))
        self.lusername.setMaximumSize(QtCore.QSize(100, 28))
        self.lusername.setObjectName("lusername")
        self.userlayout.addWidget(self.lusername, 0, 0, 1, 1)
        self.busername = DCbutton(Form)#QtWidgets.QPushButton(Form)
        self.busername.setMinimumSize(QtCore.QSize(280, 28))
        self.busername.setMaximumSize(QtCore.QSize(280, 28))
        self.busername.setFlat(True)
        self.busername.setObjectName("busername")
        self.busername.setText(self.username)
        self.busername.doubleclick=self.busernameClicked
        self.busername.setToolTip('双击编辑')
        self.userlayout.addWidget(self.busername, 0, 1, 1, 1)
        self.inusername = DCline(Form)
        self.inusername.setMinimumSize(QtCore.QSize(280, 28))
        self.inusername.setObjectName("inusername")
        self.inusername.setText(self.username)
        self.inusername.close()
        self.inusername.doubleclick=self.inusernameFinished
        self.inusername.editingFinished.connect(self.infmailFinished)
        self.userlayout.addWidget(self.inusername, 0, 1, 1, 1)
        self.lfmail = QtWidgets.QLabel(Form)
        self.lfmail.setMinimumSize(QtCore.QSize(100, 28))
        self.lfmail.setMaximumSize(QtCore.QSize(100, 28))
        self.lfmail.setObjectName("lfmail")
        self.userlayout.addWidget(self.lfmail, 1, 0, 1, 1)
        self.bfmail = DCbutton(Form)
        self.bfmail.setMinimumSize(QtCore.QSize(280, 28))
        self.bfmail.setMaximumSize(QtCore.QSize(280, 28))
        self.bfmail.setFlat(True)
        self.bfmail.setObjectName("bfmail")
        self.bfmail.setText(self.fmail)
        self.bfmail.doubleclick=self.bfmailClicked
        self.bfmail.setToolTip('双击编辑')
        self.userlayout.addWidget(self.bfmail, 1, 1, 1, 1)
        self.infmail = DCline(Form)
        self.infmail.setMinimumSize(QtCore.QSize(280, 28))
        self.infmail.setObjectName("infmail")
        self.infmail.setText(self.username)
        self.infmail.close()
        self.infmail.doubleclick=self.infmailFinished
        self.userlayout.addWidget(self.infmail, 1, 1, 1, 1)
        self.mainlayout.addLayout(self.userlayout, 0, 0, 2, 2)
        #主要信息栏
        self.linfo = QtWidgets.QLabel(Form)
        self.linfo.setMinimumSize(QtCore.QSize(300, 60))
        self.linfo.setMaximumSize(QtCore.QSize(16777215, 60))
        self.linfo.setObjectName("linfo")
        self.mainlayout.addWidget(self.linfo, 0, 2, 2, 1)
        spacerItem = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mainlayout.addItem(spacerItem, 0, 3, 1, 1)
        #搜索项目选择按钮
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setMinimumSize(QtCore.QSize(145, 28))
        self.comboBox.setMaximumSize(QtCore.QSize(145, 28))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.searchitem=self.comboBox.currentText()
        self.mainlayout.addWidget(self.comboBox, 0, 4, 1, 1)
        #搜素按钮
        self.bsearch = QtWidgets.QPushButton(Form)
        self.bsearch.setMinimumSize(QtCore.QSize(145, 28))
        self.bsearch.setMaximumSize(QtCore.QSize(145, 28))
        self.bsearch.setObjectName("bsearch")
        self.bsearch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bsearch.clicked.connect(self.bsearchClicked)
        self.mainlayout.addWidget(self.bsearch, 0, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mainlayout.addItem(spacerItem1, 1, 3, 1, 1)
        #搜素输入框
        self.searchinput = QtWidgets.QLineEdit(Form)
        self.searchinput.setMinimumSize(QtCore.QSize(300, 28))
        self.searchinput.setMaximumSize(QtCore.QSize(300, 28))
        self.searchinput.setObjectName("searchinput")
        self.searchinput.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        #self.searchinput.editingFinished.connect(self.searchinputFinished)
        self.mainlayout.addWidget(self.searchinput, 1, 4, 1, 2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setMinimumSize(QtCore.QSize(1000, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mainlayout.addWidget(self.line, 2, 0, 1, 6)
        #收信按钮
        self.mbrecieve = QtWidgets.QPushButton(Form)
        self.mbrecieve.setMinimumSize(QtCore.QSize(90, 28))
        self.mbrecieve.setMaximumSize(QtCore.QSize(90, 28))
        self.mbrecieve.setObjectName("mbrecieve")
        self.mbrecieve.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mbrecieve.clicked.connect(self.mbrecieveClicked)
        self.mainlayout.addWidget(self.mbrecieve, 3, 0, 1, 1)
        #标签窗口
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setMinimumSize(QtCore.QSize(900, 640))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.tabCloseRequested.connect(self.tabClose)
        self.tabWidget.tabBarClicked.connect(self.tabChoose)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        startcan=QWidget()
        self.starttab.setupUi(startcan)
        self.tabWidget.addTab(startcan,'欢迎')
        self.mainlayout.addWidget(self.tabWidget, 3, 1, 7, 5)
        #发信按钮
        self.mbsend = QtWidgets.QPushButton(Form)
        self.mbsend.setMinimumSize(QtCore.QSize(90, 28))
        self.mbsend.setMaximumSize(QtCore.QSize(90, 28))
        self.mbsend.setObjectName("mbsend")
        self.mbsend.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mbsend.clicked.connect(self.mbsendClicked)
        self.mainlayout.addWidget(self.mbsend, 4, 0, 1, 1)
        #通讯录按钮
        self.mbcontact = QtWidgets.QPushButton(Form)
        self.mbcontact.setMinimumSize(QtCore.QSize(90, 28))
        self.mbcontact.setMaximumSize(QtCore.QSize(90, 28))
        self.mbcontact.setObjectName("mbcontact")
        self.mbcontact.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mbcontact.clicked.connect(self.mbcontactClicked)
        self.mainlayout.addWidget(self.mbcontact, 5, 0, 1, 1)
        #收件箱按钮
        self.mbrecievebox = QtWidgets.QPushButton(Form)
        self.mbrecievebox.setMinimumSize(QtCore.QSize(90, 28))
        self.mbrecievebox.setMaximumSize(QtCore.QSize(90, 28))
        self.mbrecievebox.setObjectName("mbrecievebox")
        self.mbrecievebox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mbrecievebox.clicked.connect(self.mbrecieveboxClicked)
        self.mainlayout.addWidget(self.mbrecievebox, 6, 0, 1, 1)
        #垃圾箱按钮
        # self.mbjunkbox = QtWidgets.QPushButton(Form)
        # self.mbjunkbox.setMinimumSize(QtCore.QSize(90, 28))
        # self.mbjunkbox.setMaximumSize(QtCore.QSize(90, 28))
        # self.mbjunkbox.setObjectName("mbjunkbox")
        # self.mbjunkbox.close()
        # self.mbjunkbox.setFlat(True)
        # self.mbjunkbox.setDisabled(True)
        # #self.mbjunkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # #self.mainlayout.addWidget(self.mbjunkbox, 7, 0, 1, 1)
        #设置按钮
        self.mbset = QtWidgets.QPushButton(Form)
        self.mbset.setMinimumSize(QtCore.QSize(90, 28))
        self.mbset.setMaximumSize(QtCore.QSize(90, 28))
        self.mbset.setObjectName("mbset")
        self.mbset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mbset.clicked.connect(self.mbsetClicked)
        self.mainlayout.addWidget(self.mbset, 7, 0, 1, 1)
        #左下角信息
        self.dinfo = QtWidgets.QLabel(Form)
        self.dinfo.setFixedSize(90, 100)
        self.mainlayout.addWidget(self.dinfo, 8, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(87, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainlayout.addItem(spacerItem2, 9, 0, 1, 1)
        #初始化
        #关闭功能按钮，打开登陆界面，获取天气信息
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.setDisable(True)
        self.closeFuncButtons()
        self.tabWidget.setTabBarAutoHide(True)
        window_pale = QtGui.QPalette()
        window_pale.setBrush(Form.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(self.backpath)))
        Form.setPalette(window_pale)
        Form.setWindowOpacity(0.98)
        try:
            self.weainfo = weather()
        except:
            self.weainfo=['','','','']
        self.dinfo.setText("气温  \n>" + self.weainfo[0] + "-" + self.weainfo[1] + "\n" +
                           "天气  \n>" + self.weainfo[2] + "\n" + "风力  \n>" + self.weainfo[3])

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "WELLMAIL邮箱"))
        self.lusername.setText(_translate("Form", "发件名称："))
        self.lfmail.setText(_translate("Form", "发件地址："))
        self.comboBox.setItemText(0, _translate("Form", "发件人"))
        self.comboBox.setItemText(1, _translate("Form", "主题"))
        self.comboBox.setItemText(2, _translate("Form", "时间"))
        self.comboBox.setItemText(3, _translate("Form", "正文"))
        self.bsearch.setText(_translate("Form", "搜索"))
        self.mbrecieve.setText(_translate("Form", "收信"))
        self.mbsend.setText(_translate("Form", "写信"))
        self.mbcontact.setText(_translate("Form", "通讯录"))
        self.mbrecievebox.setText(_translate("Form", "收件箱"))
        self.mbset.setText(_translate("Form", "设置"))

    def setDisable(self,disabled):
        #设置功能按钮失效
        self.mbsend.setDisabled(disabled)
        self.mbrecieve.setDisabled(disabled)
        self.mbset.setDisabled(disabled)
        self.mbcontact.setDisabled(disabled)
        #self.mbjunkbox.setDisabled(disabled)
        self.mbrecievebox.setDisabled(disabled)
        self.bsearch.setDisabled(disabled)
        self.comboBox.setDisabled(disabled)
        self.searchinput.setDisabled(disabled)
        self.bfmail.setDisabled(disabled)
        self.busername.setDisabled(disabled)
        self.linfo.setDisabled(disabled)
        self.lfmail.setDisabled(disabled)
        self.lusername.setDisabled(disabled)

    def closeFuncButtons(self):
        #隐藏功能按钮
        self.dinfo.close()
        self.mbsend.close()
        self.mbrecieve.close()
        self.mbset.close()
        self.mbcontact.close()
        #self.mbjunkbox.close()
        self.mbrecievebox.close()

    def showFuncButtons(self):
        #显示功能按钮
        self.dinfo.show()
        self.mbsend.show()
        self.mbrecieve.show()
        self.mbset.show()
        self.mbcontact.show()
        #self.mbjunkbox.show()
        self.mbrecievebox.show()

    def setUser(self,username=None,fmail=None):
        #设置用户信息
        hanzi_regex = compile(r'[\u4E00-\u9FA5]')#汉字正则表达式，用于左对齐
        self.sender=username if username else self.sender
        if fmail:
            self.fmail=fmail
        if len(self.sender)<34:
            self.busername.setText(self.sender+" "*(34-len(self.sender)-len(hanzi_regex.findall(self.sender))))
            self.busername.setToolTip('')
        else:
            self.busername.setText(self.sender[0:30]+'....')
            self.busername.setToolTip(self.sender)
        if len(self.fmail)<34:
            self.bfmail.setText(self.fmail+" "*(34-len(self.fmail)-len(hanzi_regex.findall(self.fmail))))
            self.bfmail.setToolTip('')
        else:
            self.bfmail.setText(self.fmail[0:30]+'....')
            self.bfmail.setToolTip(self.fmail)

    def mbsetClicked(self):
        #设置按钮功能实现
        #只能打开一个设置界面
        for tabtext in list(self.tabdict.keys()):
            if '设置' in tabtext:
                self.tabWidget.setCurrentWidget(self.setcan)
                return
        #创建设置界面
        self.settab=SetUi(fmail=self.fmail,password=self.password,backpath=self.backpath)
        self.setcan=QWidget()
        self.settab.new=self.new
        self.settab.setupUi(self.setcan)
        self.settab.appendfunc=self.appendSet
        self.settab.newfunc=self.newSet
        self.settab.fmailfunc=self.fmailSet
        self.tabCount()
        self.tabWidget.addTab(self.setcan, '设置' + str(self.tabcount))
        self.tabWidget.setCurrentWidget(self.setcan)
        self.tabdict['设置' + str(self.tabcount)] = self.settab
        self.tabcount += 1
        self.setindex=self.tabWidget.currentIndex()
        self.tabChoose(self.tabWidget.currentIndex())

    def fmailSet(self):
        #设置界面切换账户功能实现
        msgBox = MsgDialog()
        msgDia = QtWidgets.QDialog()
        msgBox.setupUi(msgDia)
        msgBox.uplabel.setText('发件账户')
        msgBox.upinput.setText(self.fmail)
        msgDia.setWindowTitle('切换账户')
        msgBox.downlabel.setText('密码')
        msgBox.downinput.setText(self.password)
        msgBox.downinput.setEchoMode(QtWidgets.QLineEdit.Password)
        msgDia.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgDia.accepted.connect(self.msgAccepted)
        msgDia.rejected.connect(self.msgRejected)
        msgDia.resize(60, 50)
        msgDia.exec()
        fmail=msgBox.upinput.text()
        password=msgBox.downinput.text()
        if self.accepted:
            if fmail=='':
                return
            if password=='':
                return
            email_regex = compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
            if email_regex.findall(fmail)==[]:
                self.caution(text='邮箱格式不正确     ')
                return
            self.vps = ValidateThread(fmail, password,self.validFinished)
            self.vps.start()
            self.validbox = QMessageBox(QMessageBox.NoIcon, '稍等', '正在验证邮箱...    ')
            self.validbox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            self.validbox.setWindowFlags(QtCore.Qt.SubWindow)
            self.validbox.setWindowOpacity(0.8)
            self.validbox.setDisabled(True)
            self.validbox.exec()
            #self.caution(text='正在验证邮箱...      ')
            valid = self.vps.run()
            if not valid:
                self.caution(text='该账户无法建立连接，原因可能是：\n①网络未连接\n②账户或密码错误\n③未开启IMAP4\SMTP服务')
                return
            self.fmail=fmail
            self.username=fmail
            self.password=password
            self.settab.fmail=fmail
            self.settab.password=password
            self.settab.renew()
            self.setUser(self.sender, self.fmail)
            self.parsedictlist.clear()
            self.parsedictlist.append(self.emptypsd)
            self.first=True
            #第一次使用需要创建配套文件夹
            try:
                if not os.path.exists(os.getcwd() + '\\user\\user_maildata\\' + self.username):
                    self.first = True
                    filepath = os.getcwd() + '\\user\\user_maildata' + '\\' + self.username
                    os.system('mkdir user\\user_maildata\\' + self.username)
                    os.system('dir /b ' + filepath + ' > ' + filepath + '\\wellmaillist.welllist')
                    if not os.path.exists(os.getcwd() + '\\user\\user_info\\' + self.username):
                        os.system('mkdir ' + os.getcwd() + '\\user\\user_info\\' + self.username)
                    #print('get ready')
                else:
                    self.first = False
                    self.renewed = True
                    #print('maildir existsa')
            except:
                pass
                #print('maildir existsb')
            if self.first:
                self.caution(title='登陆', text='首次使用可以在’设置‘选择刷新时收取全部邮件')
        else:
            pass

    def validFinished(self):
        #验证结束
        #print('finished')
        self.validbox.setDisabled(False)
        self.validbox.close()

    def appendSet(self):
        #同步收发设置
        self.append=self.tabdict[self.tabWidget.tabText(self.tabWidget.currentIndex())].append
        #print(self.append)

    def newSet(self):
        #刷新模式设置
        self.new=self.tabdict[self.tabWidget.tabText(self.tabWidget.currentIndex())].new
        #print(self.new)

    def okClicked(self):
        #登陆界面确认按钮函数
        self.fmail=self.starttab.infmail.text()
        self.username=self.starttab.infmail.text()
        #第一次使用需创建配套文件夹
        try:
            if not os.path.exists(os.getcwd()+'\\user\\user_maildata\\'+self.username):
                self.first=True
                filepath = os.getcwd() + '\\user\\user_maildata' + '\\' + self.username
                os.system('mkdir user\\user_maildata\\'+self.username)
                os.system('dir /b ' + filepath + ' > ' + filepath + '\\wellmaillist.welllist')
                if not os.path.exists(os.getcwd() + '\\user\\user_info\\' + self.username):
                    os.system('mkdir ' + os.getcwd() + '\\user\\user_info\\' + self.username)
                #print('get ready')
            else:
                self.first=False
                self.renewed=True
                #print('maildir existsa')
        except:
            pass
            #print('maildir existsb')
        if self.first:
            #第一次使用给出刷新设置提示信息
            self.caution(title='登陆',text='首次使用可以在’设置‘选择刷新时收取全部邮件')
        self.password=self.starttab.inpassword.text()
        self.sender='wellmailuser'
        #设置用户信息，关闭登陆界面，读取本地邮件，打开收件箱界面
        self.setUser(self.sender,self.fmail)
        self.tabClose(self.tabWidget.currentIndex())
        self.tabWidget.setTabsClosable(True)
        self.readWellmailFile()
        try:
            self.mbrecieveboxClicked()
        except:
            pass
        #解禁并显示功能按钮
        self.setDisable(False)
        self.tabChoose(self.tabWidget.currentIndex())
        self.showFuncButtons()
        self.tabWidget.setTabBarAutoHide(False)

    #确认函数
    def msgAccepted(self):
        self.accepted=True

    def msgRejected(self):
        self.accepted=False

    def tabClose(self,index):
        #标签窗口关闭
        if self.tabWidget.tabText(index)!='欢迎':
            #欢迎界面为初始界面，不计入标签窗口
            self.tabcount-=1
            #print(self.tabcount)
            try:
                #删除关闭的标签窗口
                self.tabdict.pop(self.tabWidget.tabText(index))
            except:
                pass
        #移除相应标签
        self.tabWidget.removeTab(index)

    def tabChoose(self,index):
        #标签选择
        text=self.tabWidget.tabText(index)
        rctab=self.tabdict[text]
        self.ctab=rctab
        try:
            #回复与转发功能需要获取当前收信界面的信息
            replyinfo=rctab.getInfo()
            self.content=replyinfo[2]
            self.subject=replyinfo[0]
            self.tmail=replyinfo[1]
            self.time=replyinfo[3]
        except:
            pass

    def startTab(self):
        #登陆界面
        starttab=LoginUi()
        starttab.bokfunc=self.okClicked
        starttab.fmail='lihaoyangsohu@sohu.com'
        starttab.password=''
        return starttab

    def inusernameFinished(self):
        #发件名称编辑结束后切换成按钮
        self.sender=self.inusername.text()
        self.inusername.close()
        self.busername.show()
        self.setUser(username=self.sender)

    def busernameClicked(self):
        #发件名称按钮双击后切换成编辑模式
        self.busername.close()
        self.inusername.show()
        self.setUser(username=self.sender)
        self.inusername.setText(self.sender)

    def infmailFinished(self):
        #发件地址编辑框编辑结束后切换成按钮
        #不保存编辑的内容（但可以利用编辑框复制该信息）
        self.infmail.close()
        self.setUser(None,self.fmail)
        self.bfmail.show()

    def bfmailClicked(self):
        #发件地址按钮双击后切换成编辑模式
        self.bfmail.close()
        self.infmail.show()
        self.infmail.setText(self.fmail)

    def mbrecieveClicked(self,date=None,subject=None):
        try:
            #print(len(self.parsedictlist))
            if self.parsedictlist==[]:
                return
            if len(self.parsedictlist)<1:
                return
            self.mbrecieveClickedTry(date,subject)
        except:
            pass

    def mbrecieveClickedTry(self,date=None,subject=None):
        #收件按钮实现功能
        QApplication.processEvents()
        #如果从别的界面打开收信界面，且设置了date和subject，搜索并显示匹配的邮件
        #保证从收件箱或者搜索界面点击相应邮件可以打开相应邮件的收信界面
        if date:
            #print(date)
            cpsd=0
            for psd in self.parsedictlist:
                if psd['date']!=date:
                    cpsd+=1
                else:
                    break
        else:
            #一般情况下，保证每次打开收信界面时都有不同的变化
            #根据标签数目点击下一封按钮
            cpsd=0
            for n in range(0,self.tabcount):
                cpsd+=1
        #创建收件界面
        #print(cpsd)
        rctab=MailBrowser(cpsd,self.parsedictlist)
        rccan=QWidget()
        #rctab.currentpsd=cpsd
        rctab.parsedictlist=self.parsedictlist
        rctab.dparsedictlist=self.dparsedictlist
        rctab.fmail=self.fmail
        rctab.password=self.password
        rctab.username=self.username
        rctab.replyfunc=self.replyClicked
        rctab.resendfunc=self.resendClicked
        rctab.savecontactfunc=self.savecontactClicked
        rctab.renewfunc=self.renewClicked
        rctab.delfunc=self.delFinished
        rctab.delfailfunc=self.delFailed
        rctab.delsync=self.delsync
        rctab.replyinfo=self.replyinfo
        rctab.setupUi(rccan)
        #print('all set')
        #计数，显示，保存该界面
        self.tabCount()
        self.tabWidget.addTab(rccan,'收信'+str(self.tabcount))
        try:
            self.tabWidget.setCurrentWidget(rccan)
        except:
            pass
        self.tabdict['收信'+str(self.tabcount)]=rctab
        self.tabcount+=1
        #选择该界面，确保回复和转发时信息正确
        self.tabChoose(self.tabWidget.currentIndex())

    def readWellmailFile(self):
        #本地邮件读取函数
        QApplication.processEvents()
        #yprint('ready read')
        #当有读取线程正在运行时返回，防止冲突
        if self.readthread:
            if self.readthread.isAlive():
                return
        #创建本地邮件读取线程
        self.readthread = ReadMailThread(os.getcwd(), self.username)
        self.readthread.parsedictlist = self.parsedictlist
        self.readthread.setDaemon(True)
        self.readthread.start()

    def renewClicked(self):
        #刷新按钮功能实现
        QApplication.processEvents()
        #如果有刷新线程正在运行，则显示目前已经刷新到的内容
        if self.renewthread:
            if self.renewthread.isAlive():
                self.renewing=True
                self.renewFinshed()
                return
        #禁止在刷新过程中删除（防止冲突）
        if self.rbtab:
            try:
                self.rbtab.delete_button.setDisabled(True)
            except:
                pass
        #创建刷新线程
        self.renewthread=RenewThread(self.fmail, self.password)
        self.renewthread.new=self.new
        self.renewthread.parsedictlist=self.parsedictlist
        self.renewthread.finishfunc=self.renewFinshed
        self.renewthread.setDaemon(True)
        self.renewthread.start()
        #提示正在刷新
        self.linfo.setText('努力获取新邮件中...')


    def renewFinshed(self):
        #刷新完成后读取本地邮件（刷新的邮件会保存到本地）
        self.readWellmailFile()
        if self.renewing:
            #正在刷新时提示正在刷新
            self.linfo.setText('已加载当前邮件（正在更新）\n点击‘收件箱’或‘收信’查看')
        else:
            #刷新完成后允许删除
            if self.rbtab:
                try:
                    self.rbtab.delete_button.setDisabled(False)
                except:
                    pass
            self.linfo.setText('已加载当前邮件\n点击‘收件箱’或‘收信’查看')
            #设置已经刷新为真
            if not self.new:
                self.new=True
        #读取后不再是第一次，也不再处于刷新状态
        self.renewing=False
        self.first=False

    #以下三个函数基于回复和发信操作
    def replyClicked(self):
        #回复按钮功能实现
        self.tabChoose(self.tabWidget.currentIndex())
        content=self.replyGenerator()
        tmail=self.tmail
        subject='回复：'+self.subject
        self.mbsendClicked(content,tmail,subject)

    def resendClicked(self):
        #转发按钮功能实现（没有收件人的回复）
        self.tabChoose(self.tabWidget.currentIndex())
        content = self.replyGenerator()
        tmail=''
        subject = '转发：' + self.subject
        self.mbsendClicked(content, tmail, subject)

    def writeClicked(self):
        #通讯录点击联系人写信功能实现
        for tabtext in list(self.tabdict.keys()):
            if '通讯录' in tabtext:
                cntab=self.tabdict[tabtext]
                self.tmail=cntab.writeinfo[0]+'<'+cntab.writeinfo[1]+'>'
                self.mbsendClicked(tmail=self.tmail)

    def replyGenerator(self):
        #回复内容生成
        content="""<div><br></div><div><div><br></div><div><br></div><div style="font-size: 12px;font-family: Arial Narrow;padding:2px 0 2px 0;">------------------&nbsp;原始邮件&nbsp;------------------</div><div style="font-size: 12px;background:#86cfff;padding:8px;"><div><b>发件人:</b>&nbsp;SENDER&lt;FMAIL&gt;;</div><div  style="font-size: 12px;background:#86cfff;padding:8px;"><b>发送时间:</b>&nbsp;DATE</div><div  style="font-size: 12px;background:#86cfff;padding:8px;"><b>收件人:</b>&nbsp;RECIEVER&lt;TMAIL&gt;;<wbr></div><div></div><div style="font-size: 12px;background:#86cfff;padding:8px;"><b>主题:</b>&nbsp;SUBJECT</div></div><div><br></div>CONTENT</div>"""
        content=content.replace('SENDER',self.sender)
        content=content.replace('FMAIL',self.fmail)
        content=content.replace('RECIEVER',self.tmail.split('<')[0])
        content=content.replace('TMAIL',self.tmail.split('<')[-1].strip('>'))
        content=content.replace('SUBJECT',self.subject)
        content=content.replace('DATE',self.time)
        content=content.replace('CONTENT',self.content)
        return content

    def delFinished(self):
        #删除完成函数
        #在线删除完成后删除本地邮件
        #print('del fin')
        try:
            dname = self.dparsedictlist[-1]['date']
            for s in ['[', '\\', ':', '*', '?', '<', '>', '|', ']']:
                dname = dname.replace(s, "")
            dname = dname + '.wellmail'
            os.system('del ' + "\"" + os.getcwd() + '\\user\\user_maildata\\'+self.fmail+'\\'+ dname + "\"")
        except:
            pass
        #再次判断是否删除成功
        self.delFailed()

    def delFailed(self):
        #删除失败后的操作
        #在线删除失败有可能是因为用户在别的端口删除了该邮件
        #因此删除失败后再次尝试删除本地邮件
        filepath=os.getcwd()+'\\user\\user_maildata\\'+self.fmail
        try:
            dname=self.dparsedictlist[-1]['date']
            for s in ['[','\\',':','*','?','<','>','|',']']:
                dname=dname.replace(s,"")
            dname=dname+'.wellmail'
            os.system('del '+"\""+os.getcwd()+'\\user\\user_maildata\\'+self.fmail+'\\'+dname+"\"")
            if not os.path.exists("\""+os.getcwd()+'\\user\\user_maildata\\'+self.fmail+'\\'+dname+"\""):
                self.linfo.setText('邮件已经删除')
            else:
                self.linfo.setText('邮件删除失败')
        except:
            if not os.path.exists("\""+os.getcwd()+'\\user\\user_maildata\\'+self.fmail+'\\'+dname+"\""):
                self.linfo.setText('邮件已经删除')
            else:
                self.linfo.setText('邮件删除失败')
        try:
            #生成新的本地邮件列表，保证下一次读取不出错
            os.system('dir /b ' + filepath + ' > ' + filepath + '\\wellmaillist.welllist')
        except:
            pass
        #读取本地邮件
        self.readWellmailFile()

    def savecontactClicked(self):
        #保存到通讯录按钮实现
        self.tabChoose(self.tabWidget.currentIndex())
        self.mbcontactClicked(save=True)
        pass

    def mbsendClicked(self,content=None,tmail=None,subject=None):
        #发信按钮功能实现
        swtab=emailWriter(content,tmail,subject,self.parsedictlist,self.username)
        swcan=QWidget()
        swtab.setupUi(swcan)
        swtab.fmail=self.fmail
        swtab.sender=self.sender
        swtab.password=self.password
        swtab.sendfunc1=self.sendStarted
        swtab.sendfunc2=self.sendFinished
        swtab.sendfailfunc=self.sendFailed
        swtab.backfunc=self.sendCanceled
        swtab.append=self.append
        self.tabCount()
        self.tabWidget.addTab(swcan, '写信' + str(self.tabcount))
        self.tabWidget.setCurrentWidget(swcan)
        self.tabdict['写信' + str(self.tabcount)] = swtab
        self.tabcount += 1
        #设置文本编辑器（内置窗口）背景
        actwin=swtab.Writing.activeSubWindow()
        window_pale = QtGui.QPalette()
        window_pale.setBrush(actwin.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("img/backgroundTextEditor.png")))
        actwin.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        actwin.setPalette(window_pale)

    def sendCanceled(self):
        #发送界面返回按钮
        try:
            self.tabWidget.removeTab(self.tabWidget.currentIndex())
            self.tabcount-=1
        except:
            pass

    def sendStarted(self):
        #开始发送邮件
        #此时禁止写信界面发生变化
        #等到发送完成或失败后解禁
        self.disabledtabindex=self.tabWidget.currentIndex()
        self.tabWidget.currentWidget().setDisabled(True)
        self.linfo.setText('邮件正在发送...')

    def sendFailed(self):
        #邮件发送失败
        self.tabWidget.widget(self.disabledtabindex).setDisabled(False)
        self.linfo.setText('邮件发送失败')

    def sendFinished(self):
        #邮件发送完成
        self.linfo.setText('邮件发送完成...')
        self.tabWidget.widget(self.disabledtabindex).setDisabled(False)


    def mbrecieveboxClicked(self):
        #收件箱按钮功能实现
        QApplication.processEvents()
        #收件箱界面只能打开一个，再次点击将关闭现有的重新打开（保证内容更新）
        for tabtext in list(self.tabdict.keys()):
            if '收件箱' in tabtext:
                self.tabWidget.setCurrentWidget(self.rbcan)
                self.tabClose(self.tabWidget.currentIndex())
                break
        #创建收件箱界面
        rbtab = RecieveBoxUi(psdlist=self.parsedictlist)
        rbcan = QWidget()
        rbtab.fmail = self.fmail
        rbtab.password = self.password
        rbtab.showfunc = self.showClicked
        rbtab.renewfunc = self.renewClicked
        rbtab.resendfunc = self.boxresendClicked
        rbtab.delfunc = self.delFinished
        rbtab.delfailfunc = self.delFailed
        rbtab.dparsedictlist = self.dparsedictlist
        rbtab.setupUi(rbcan)
        #计数并保存该界面
        self.tabCount()
        self.tabWidget.addTab(rbcan, '收件箱' + str(self.tabcount))
        self.tabWidget.setCurrentWidget(rbcan)
        self.rbcan=rbcan
        self.rbtab=rbtab
        self.tabdict['收件箱' + str(self.tabcount)] = rbtab
        self.tabcount += 1

    def boxresendClicked(self):
        #发件箱转发按钮功能实现
        #先显示该邮件，然后自动点击收信界面的转发按钮，然后关闭收信界面
        self.rbtab.shows(self.rbtab.key)
        self.resendClicked()
        self.tabClose(self.tabWidget.currentIndex()-1)

    def bsearchClicked(self):
        #搜索按钮功能实现
        #搜索界面关键字类别是英文标识，因此需要进行转换
        transdict={'发件人':'from','主题':'subject','时间':'date','正文':'content'}
        #设置搜索关键字类别与搜索关键字
        self.searchitem=transdict[self.comboBox.currentText()]
        self.searchkey=self.searchinput.text()
        #创建搜索界面并进行搜索
        srcan=QWidget()
        srtab=SearchUi(data=self.parsedictlist,item=self.searchitem,keyword=self.searchkey)
        srtab.showfunc=self.showClicked
        srtab.setupUi(srcan)
        #计数保存该界面
        self.tabCount()
        self.tabWidget.addTab(srcan,'搜索'+str(self.tabcount))
        self.tabWidget.setCurrentWidget(srcan)
        self.tabdict['搜索'+str(self.tabcount)]=srtab
        self.tabcount+=1

    def showClicked(self):
        #搜索界面点击邮件主题、发件人、时间显示该邮件实现
        cpsd=self.tabdict[self.tabWidget.tabText(self.tabWidget.currentIndex())].getcpsd()
        #print(cpsd['date'],cpsd['subject'])
        #根据相应时间和主题查找并显示相应邮件
        self.mbrecieveClicked(date=cpsd['date'],subject=cpsd['subject'])

    def searchinputFinished(self):
        #实现搜索关键字输入框非空时，按回车进行搜索
        if self.searchinput.text()!='':
            self.bsearchClicked()

    def mbcontactClicked(self,save=False):
        #通讯录按钮功能实现
        #save关键字用于其他界面调用此函数来保存联系人
        exist=False
        #通讯录界面只能打开一个
        for tabtext in list(self.tabdict.keys()):
            if '通讯录' in tabtext:
                self.tabWidget.setCurrentWidget(self.mbcan)
                mbtab=self.tabdict[tabtext]
                exist=True
                break
        #当前不存在通讯录界面则创建一个新的
        if not exist:
            self.mbcan=QWidget()
            mbtab=MemberUi(username=self.username)
            mbtab.setupUi(self.mbcan)
            mbtab.writefunc=self.writeClicked
            self.tabCount()
            self.tabWidget.addTab(self.mbcan,'通讯录'+str(self.tabcount))
            self.tabdict['通讯录'+str(self.tabcount)]=mbtab
            self.tabcount+=1
            self.tabWidget.setCurrentWidget(self.mbcan)
        if save:
            #保存写信界面的联系人
            #具体实现为打开通讯录界面，输入相应的用户名和地址，点击添加，然后关闭通讯录界面
            added=False
            try:
                mbtab.emailedit.setText(self.tmail.split('<')[1].strip('>').strip(' '))
                mbtab.nameedit.setText(self.tmail.split('<')[0].strip(' '))
                added=mbtab.addmember()
                if not exist:
                    self.tabClose(self.tabWidget.currentIndex())
                if added:
                    self.caution(title='保存联系人',text='联系人已经成功保存到通讯录')
            except:
                try:
                    mbtab.emailedit.setText(self.tmail)
                    mbtab.nameedit.setText(self.tmail)
                    added=mbtab.addmember()
                    if not exist:
                        self.tabClose(self.tabWidget.currentIndex())
                    if added:
                        self.caution(title='保存联系人', text='联系人已经成功保存到通讯录')
                except:
                    if not exist:
                        if '通讯录' in self.tabWidget.tabText(self.tabWidget.currentIndex()):
                            self.tabClose(self.tabWidget.currentIndex())
                    self.caution(title='保存联系人',text='该联系人无法保存')


    def tabCount(self):
        #标签计数，将tabcount设置为当前标签数目加1
        self.tabcount=1
        while str(self.tabcount) in str(self.tabdict.keys()):
            self.tabcount+=1

    def caution(self,title='啊哦',text='稍等'):
        #提示框
        msgBox = QMessageBox(QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgBox.setWindowOpacity(0.9)
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.exec()


class RenewThread(threading.Thread):
    #刷新线程
    def __init__(self,fmail,password,psdlist=None):
        super().__init__()
        #邮件列表
        self.msglist=[]
        #用户信息
        self.fmail=fmail
        self.username=fmail
        self.password=password
        #默认获取收件箱的内容
        self.maildir='INBOX'
        #默认只收取新邮件，收信后标识已读
        self.new=True
        self.seen=True
        #邮件字典列表（用于存放收取并解析的邮件）
        self.parsedictlist=psdlist if psdlist else []
        #刷新完成后执行的函数和完成标识
        self.finishfunc=None
        self.renewed=True

    def run(self):
        #print('run',self.new)
        #获取邮件
        try:
            self.msglist=getEmailIMAP4(self.fmail,self.password,maildir=self.maildir,new=self.new,seen=self.seen)
        except:
            self.renewed=False
            if self.finishfunc:
                self.finishfunc()
        #print('got')
        #解析邮件
        try:
            for msg in self.msglist:
                psd=parseEmail(msg)
                #对于无时间戳的邮件，添加‘-’防止出错
                if psd['date']=='-':
                    continue
                #只添加新邮件（因为可能设置为全部收取）
                if psd not in self.parsedictlist:
                    self.parsedictlist.append(psd)
                #print('msgparsed')
        except:
            pass
        if len(self.parsedictlist)<1:
            self.renewed=False
        if self.finishfunc:
            self.finishfunc()

class ReadMailThread(threading.Thread):
    #读取线程
    def __init__(self,filepath=os.getcwd(),username=''):
        super().__init__()
        #读取完成标识
        self.fin=False
        #读取所需信息（当前工作路径和当前用户）
        self.filepath=filepath
        self.username=username
        #读取后存放邮件字典的列表
        self.parsedictlist=None
        #留给外部的读取进度函数接口
        self.readfilefunc=None
        self.readfinfunc=None

    def run(self):
        self.fin=False
        #读取邮件列表
        self.filelist=readWelllist(self.filepath,self.username)
        if self.filelist==[]:
            #如果列表为空则完成读取
            #print('emty fir')
            if self.readfinfunc:
                self.readfinfunc()
            return
        for file in self.filelist:
            #依次读取邮件列表中的邮件
            self.parsedict=readWellmailFile(self.filepath+'\\user\\user_maildata\\' + self.username,file)
            #print('read')
            if self.parsedictlist:
                #将读取到的邮件添加到当前邮件列表中
                if self.parsedict not in self.parsedictlist:
                    self.parsedictlist.append(self.parsedict)
                    #print('appended')
            if self.readfilefunc:
                self.readfilefunc()
        self.fin=True
        #读取完成
        if self.readfinfunc:
            self.readfinfunc()

class DCbutton(QPushButton):
    #双击扩展按钮
    def __init__(self,parent=None):
        super(DCbutton,self).__init__(parent)
        self.doubleclick=None

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.doubleclick:
            self.doubleclick()

class DCline(QLineEdit):
    #双击扩展单行文本输入框
    def __init__(self,parent=None):
        super(DCline,self).__init__(parent)
        self.doubleclick=None

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.doubleclick:
            self.doubleclick()



