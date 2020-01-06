# -*- coding: utf-8 -*-

#信件浏览器

#Email Browser
#Written by Haoyang Li

# Form implementation generated from reading ui file 'readMailBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import sys
from os import getcwd
from re import compile
from emailRetriever import readWellmailFile
from emailRetriever import readWellmailDir
from emailSender import createEmail
from emailRetriever import parseEmail
from emailRetriever import saveParsedFile
from emailRetriever import deleteEmailIMAP4
from threading import Thread

class MailBrowser(object):
    def __init__(self,cpsd=0,psdlist=[]):
        self.accepted=False
        self.contentph=False
        #邮件内容与用户信息
        self.contenttext='<正文>'
        self.sender='WellMailSender<well@wellmail.com>'
        self.reciever='WellMailReciever<wellr@wellmail.com>'
        self.time='20181221'
        self.subject='<主题>'
        #附件列表
        self.file=[]
        self.fileone=False
        #邮件待阅列表和已删除列表
        self.parsedictlist=psdlist
        self.dparsedictlist=[]
        self.currentpsd=cpsd#当前邮件序号
        #附件下载列表
        self.downloadfile=[]
        self.downloadpath=getcwd()
        #空邮件
        self.emptypsd={'subject':'-','from':'-','to':'-','date':'-','payload':{'content0':'-'},'file':{'filename':[]},'flag':'Empty'}
        self.emptypsd['subject']='欢迎使用WELLMAIL邮箱'
        self.emptypsd['from']='WELLMAIL<well@wellmail.com>'
        self.emptypsd['to']='WELLMAILUSER'
        self.emptypsd['payload']['content0']='欢迎使用WELLMAIL邮箱\n（此邮件为本地邮件,不在您的邮箱中，只作示例）'
        #留给模块外部的函数接口
        self.replyfunc=None
        self.resendfunc=None
        self.savecontactfunc=None
        self.renewfunc=None
        self.nexfunc=None
        self.prefunc=None
        self.delfunc=None
        self.delfailfunc=None
        self.delthread=None
        #用户信息
        self.fmail=''
        self.password=''
        self.username='Wellmail'
        self.delsync=True
        #统计信息
        self.info={'当前信件':cpsd,'总数':len(psdlist)}

    def setupUi(self, Form):
        #界面窗口设置
        Form.setObjectName("Form")
        Form.resize(950, 600)
        Form.setMinimumSize(QtCore.QSize(946, 603))
        Form.setMouseTracking(False)
        Form.setWindowOpacity(1)
        Form.setWindowTitle('接收邮件')
        Form.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))

        self.mainlayout = QtWidgets.QGridLayout(Form)
        self.mainlayout.setObjectName("mainlayout")
        #发件人，收件人，主题，时间标签
        self.infopart1 = QtWidgets.QVBoxLayout()
        self.infopart1.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.infopart1.setObjectName("infopart1")
        self.lsender = QtWidgets.QLabel(Form)
        self.lsender.setMinimumSize(QtCore.QSize(90, 20))
        self.lsender.setMaximumSize(QtCore.QSize(90, 20))
        self.lsender.setObjectName("lsender")
        self.infopart1.addWidget(self.lsender)
        self.lreciever = QtWidgets.QLabel(Form)
        self.lreciever.setMinimumSize(QtCore.QSize(90, 20))
        self.lreciever.setMaximumSize(QtCore.QSize(90, 20))
        self.lreciever.setObjectName("lreciever")
        self.infopart1.addWidget(self.lreciever)
        self.ltime = QtWidgets.QLabel(Form)
        self.ltime.setMinimumSize(QtCore.QSize(90, 20))
        self.ltime.setMaximumSize(QtCore.QSize(90, 20))
        self.ltime.setObjectName("ltime")
        self.infopart1.addWidget(self.ltime)
        self.lsubject = QtWidgets.QLabel(Form)
        self.lsubject.setMinimumSize(QtCore.QSize(90, 20))
        self.lsubject.setMaximumSize(QtCore.QSize(90, 20))
        self.lsubject.setObjectName("lsubject")
        self.infopart1.addWidget(self.lsubject)
        self.mainlayout.addLayout(self.infopart1, 0, 0, 1, 1)
        #发件人，收件人，主题，时间内容
        self.infopart2 = QtWidgets.QVBoxLayout()
        self.infopart2.setObjectName("infopart2")
        self.bsender = DCbutton(Form)
        self.bsender.setMinimumSize(QtCore.QSize(715, 22))
        self.bsender.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bsender.setFlat(True)
        self.bsender.setObjectName("bsender")
        self.bsender.doubleclick=self.savecontactClicked
        self.bsender.setToolTip('双击保存该联系人到通讯录')
        self.infopart2.addWidget(self.bsender)
        self.breciever = DCbutton(Form)
        self.breciever.setMinimumSize(QtCore.QSize(715, 22))
        self.breciever.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.breciever.setFlat(True)
        self.breciever.setObjectName("breciever")
        self.infopart2.addWidget(self.breciever)
        self.btime = QtWidgets.QPushButton(Form)
        self.btime.setMinimumSize(QtCore.QSize(715, 22))
        self.btime.setFlat(True)
        self.btime.setObjectName("btime")
        self.infopart2.addWidget(self.btime)
        self.bsubject = QtWidgets.QPushButton(Form)
        self.bsubject.setMinimumSize(QtCore.QSize(715, 22))
        self.bsubject.setFlat(True)
        self.bsubject.setObjectName("bsubject")
        self.infopart2.addWidget(self.bsubject)
        self.mainlayout.addLayout(self.infopart2, 0, 1, 1, 1)
        #右上角信息
        self.linfo = QtWidgets.QLabel(Form)
        self.linfo.setMinimumSize(QtCore.QSize(91, 111))
        self.linfo.setMaximumSize(QtCore.QSize(91, 111))
        self.linfo.setObjectName("linfo")
        self.linfo.setText(self.infoText())
        self.mainlayout.addWidget(self.linfo, 0, 2, 1, 1)
        #正文（一个用于浏览网页，一个用于浏览HTML源）
        self.content = QWebEngineView(Form)
        self.content.setObjectName("content")
        self.content.setHtml(self.contenttext)
        self.mainlayout.addWidget(self.content, 2, 0, 1, 2)
        self.contentp = QtWidgets.QTextEdit()
        self.contentp.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.contentp.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.contentp.setObjectName("contentp")
        self.contentp.setPlainText(self.contenttext)
        self.mainlayout.addWidget(self.contentp, 2, 0, 1, 2)
        self.contentp.close()
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mainlayout.addWidget(self.line, 1, 0, 1, 3)
        #右侧功能按键
        self.funcpart = QtWidgets.QVBoxLayout()
        self.funcpart.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.funcpart.setObjectName("funcpart")
        #切换显示格式
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.toggled.connect(self.checkBoxChecked)
        self.funcpart.addWidget(self.checkBox)
        #切换上一封，下一封邮件
        self.nex_pre = QtWidgets.QHBoxLayout()
        self.nex_pre.setObjectName("nex_pre")
        self.pre = QtWidgets.QPushButton(Form)
        self.pre.setMinimumSize(QtCore.QSize(40, 28))
        self.pre.setMaximumSize(QtCore.QSize(40, 28))
        self.pre.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pre.setObjectName("pre")
        self.pre.clicked.connect(self.preClicked)
        self.pre.setToolTip('上一封')
        self.nex_pre.addWidget(self.pre)
        self.nex = QtWidgets.QPushButton(Form)
        self.nex.setMinimumSize(QtCore.QSize(40, 28))
        self.nex.setMaximumSize(QtCore.QSize(40, 28))
        self.nex.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.nex.setObjectName("nex")
        self.nex.clicked.connect(self.nexClicked)
        self.nex.setToolTip('下一封')
        self.nex_pre.addWidget(self.nex)
        self.funcpart.addLayout(self.nex_pre)
        #保存发件人到通讯录
        self.savecontact = QtWidgets.QPushButton(Form)
        self.savecontact.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.savecontact.setObjectName("savecontact")
        self.savecontact.setToolTip('保存发件人')
        self.savecontact.clicked.connect(self.savecontactClicked)
        self.funcpart.addWidget(self.savecontact)
        #回复
        self.reply = QtWidgets.QPushButton(Form)
        self.reply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reply.setObjectName("reply")
        self.reply.clicked.connect(self.replyClicked)
        self.funcpart.addWidget(self.reply)
        #转发
        self.resend = QtWidgets.QPushButton(Form)
        self.resend.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.resend.setObjectName("reply")
        self.resend.clicked.connect(self.resendClicked)
        self.funcpart.addWidget(self.resend)
        #删除
        self.delete_2 = QtWidgets.QPushButton(Form)
        self.delete_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_2.setObjectName("delete_2")
        self.delete_2.clicked.connect(self.deleteClicked)
        self.funcpart.addWidget(self.delete_2)
        #保存邮件
        self.msave = QtWidgets.QPushButton(Form)
        self.msave.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.msave.setObjectName("msave")
        self.msave.clicked.connect(self.msaveClicked)
        self.funcpart.addWidget(self.msave)
        #刷新
        self.renew = QtWidgets.QPushButton(Form)
        self.renew.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.renew.setObjectName("renew")
        self.renew.clicked.connect(self.renewClicked)
        self.funcpart.addWidget(self.renew)
        spacerItem = QtWidgets.QSpacerItem(20, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.funcpart.addItem(spacerItem)
        self.mainlayout.addLayout(self.funcpart, 2, 2, 1, 1)
        #附件部分
        self.filepart = QtWidgets.QVBoxLayout()
        self.filepart.setObjectName("filepart")
        self.lfile_save = QtWidgets.QHBoxLayout()
        self.lfile_save.setObjectName("lfile_save")
        self.lfile = QtWidgets.QLabel(Form)
        self.lfile.setObjectName("lfile")
        self.lfile_save.addWidget(self.lfile)
        spacerItem1 = QtWidgets.QSpacerItem(404, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lfile_save.addItem(spacerItem1)
        #保存附件
        self.save = QtWidgets.QPushButton(Form)
        self.save.setMinimumSize(QtCore.QSize(99, 28))
        self.save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save.setObjectName("save")
        self.save.clicked.connect(self.saveClicked)
        self.lfile_save.addWidget(self.save)
        self.filepart.addLayout(self.lfile_save)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.filepart.addWidget(self.line_2)
        #附件名称
        self.mainlayout.addLayout(self.filepart, 3, 0, 1, 3)
        #初始化
        self.retranslateUi(Form)
        #初始化时关闭附件部分
        self.closeFilepart()
        if len(self.parsedictlist)>0:
            self.showParseDict(self.parsedictlist[self.currentpsd])
        else:
            self.showParseDict(self.emptypsd)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "收件"))
        self.lsender.setText(_translate("Form", "发件人："))
        self.lreciever.setText(_translate("Form", "收件人："))
        self.ltime.setText(_translate("Form", "时间："))
        self.lsubject.setText(_translate("Form", "主题："))
        self.checkBox.setText(_translate("Form", "查看HTML"))
        self.pre.setText(_translate("Form", "←"))
        self.nex.setText(_translate("Form", "→"))
        self.savecontact.setText(_translate("Form", "保存到通讯录"))
        self.reply.setText(_translate("Form", "回复"))
        self.resend.setText(_translate("Form","转发"))
        self.delete_2.setText(_translate("Form", "删除"))
        self.msave.setText(_translate("Form", "另存为"))
        self.renew.setText(_translate("Form", "刷新"))
        self.lfile.setText(_translate("Form", "附件"))
        self.save.setText(_translate("Form", "另存为"))

    def setDisable(self,disabled):
        #设置部分按钮失效的函数
        self.delete_2.setDisabled(disabled)
        self.reply.setDisabled(disabled)
        self.resend.setDisabled(disabled)
        self.save.setDisabled(disabled)
        self.savecontact.setDisabled(disabled)

    def infoText(self):
        #用于更新统计信息
        return '当前信件\n'+str(self.info['当前信件'])+'\n备阅总数\n'+str(self.info['总数'])

    def checkBoxChecked(self):
        #切换显示模式
        if self.contentph:
            self.content.close()
            self.contentp.show()
            if self.checkBox.isChecked():
                self.contentp.setPlainText(self.contenttext)
            else:
                self.contentp.setHtml(self.contenttext)
        else:
            if self.checkBox.isChecked():
                self.content.close()
                self.contentp.show()
                self.contentp.setPlainText(self.contenttext)
            else:
                self.contentp.close()
                self.content.show()
                self.content.setHtml(self.contenttext)

    def preClicked(self):
        #上一封按钮功能实现
        self.info['当前信件']=self.currentpsd
        self.info['总数'] = len(self.parsedictlist)
        self.linfo.setText(self.infoText())
        #留给外部函数的接口
        if self.prefunc:
            self.prefunc()
        #调整当前序号
        if len(self.parsedictlist)>0:
            if self.currentpsd>0:
                self.currentpsd-=1
            else:
                self.currentpsd=len(self.parsedictlist)-1
            self.showParseDict(self.parsedictlist[self.currentpsd])
        else:
            self.showParseDict(self.emptypsd)
        #对于原始空邮件，禁止部分按钮
        if self.parsedictlist[self.currentpsd]==self.emptypsd:
            self.setDisable(True)
        else:
            self.setDisable(False)


    def nexClicked(self):
        #下一封按钮功能实现
        self.info['当前信件'] = self.currentpsd
        self.info['总数'] = len(self.parsedictlist)
        self.linfo.setText(self.infoText())
        #留给外部函数的接口
        if self.nexfunc:
            self.nexfunc()
        #调整当前序号
        if len(self.parsedictlist)>0:
            if self.currentpsd<len(self.parsedictlist)-1:
                self.currentpsd+=1
            else:
                self.currentpsd=0
            self.showParseDict(self.parsedictlist[self.currentpsd])
        else:
            self.showParseDict(self.emptypsd)
        #对于原始空邮件，禁止部分按钮
        if self.parsedictlist[self.currentpsd]==self.emptypsd:
            self.setDisable(True)
        else:
            self.setDisable(False)


    def savecontactClicked(self):
        #保存到通讯录按钮功能实现
        if len(self.parsedictlist)>0:
            #留给外部函数接口
            if self.savecontactfunc:
                self.savecontactfunc()
            else:
                pass
                #print('savecontactfunc=None')
        else:
            msgBox = QMessageBox(QMessageBox.NoIcon, '啊哦', '没有发件人可以保存呢')
            msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgBox.exec()

    def replyClicked(self):
        #回复按钮功能实现
        if len(self.parsedictlist)>0:
            if self.replyfunc:
                self.replyfunc()
            else:
                pass
                #print('replyfunc=None')
        else:
            msgBox = QMessageBox(QMessageBox.NoIcon, '啊哦', '没有可以回复的邮件了')
            msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgBox.exec()

    def getInfo(self):
        #邮件信息获取函数，用于回复、转发时调用
        return (self.subject,self.sender,self.contenttext,self.time)

    def resendClicked(self):
        #转发按钮功能实现
        if len(self.parsedictlist)>0:
            if self.resendfunc:
                self.resendfunc()
            else:
                pass
                #print('resendfunc=None')
        else:
            msgBox = QMessageBox(QMessageBox.NoIcon, '啊哦', '没有可以转发的邮件了')
            msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgBox.exec()

    def deleteClicked(self):
        #删除按钮功能实现
        if len(self.parsedictlist)>0:
            if self.delthread:
                if self.delthread.isAlive():
                    self.caution(title='删除',text='稍等，正在删除上一封邮件')
                    return
            #确认框
            msgBox = MsgDialog()
            msgDia = QDialog()
            msgBox.setupUi(msgDia)
            msgBox.uplabel.setText('确定要删除这封邮件吗？')
            msgDia.setWindowTitle('删除')
            msgBox.downlabel.close()
            msgBox.downinput.close()
            msgBox.upinput.close()
            msgDia.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgDia.accepted.connect(self.msgAccepted)
            msgDia.rejected.connect(self.msgRejected)
            msgDia.resize(60,50)
            msgDia.exec()
            if self.accepted:
                #调用删除进程
                dpsd=self.parsedictlist.pop(self.currentpsd)
                self.dparsedictlist.append(dpsd)
                self.dparsedictlist[-1]['flag']+='\\delete'
                self.nexClicked()
                self.delthread=DelThread(self.fmail,self.password,dpsd)
                self.delthread.delfunc=self.delFinished
                self.delthread.delfailfunc=self.delFailed
                self.delthread.sync=self.delsync
                self.delthread.setDaemon(True)
                self.delthread.start()
                self.accepted=False
        else:
            msgBox=QMessageBox(QMessageBox.NoIcon,'啊哦','没有可以删除的邮件了')
            msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgBox.exec()

    def delFinished(self):
        if self.delfunc:
            self.delfunc()

    def delFailed(self):
        if self.delfailfunc:
            self.delfailfunc()

    def msaveClicked(self):
        #邮件另存为按钮功能实现
        if len(self.parsedictlist)>0:
            cpsd=self.parsedictlist[self.currentpsd]
            #文件保存路径选择框
            msgBox = QWidget()
            fileName2, ok2 = QFileDialog.getSaveFileName(msgBox, "文件保存", "C:/" + cpsd['subject'],
                                                         '(*.txt)')
            path = fileName2
            name = fileName2.split('/')[-1]
            self.accepted=True
            if self.accepted :
                #保存文件
                fp=open(path,'w')
                fp.write('subject:'+cpsd['subject']+'\n')
                fp.write('from:' + cpsd['from'] + '\n')
                fp.write('to:' + cpsd['to'] + '\n')
                fp.write('date:' + cpsd['date'] + '\n')
                for n in range(0,cpsd['payload']['num']):
                    fp.write('content'+str(n)+':\n')
                    fp.write(cpsd['payload']['content'+str(n)])
                fp.write('append_filename:\n')
                if cpsd['file']['filename'] is not []:
                    for fn in cpsd['file']['filename']:
                        fp.write(fn+'\n')
                fp.close()
                #print('saved')
            else:
                pass
                #print('rejected')
        else:
            msgBox = QMessageBox(QMessageBox.NoIcon, '啊哦', '没有可以保存的邮件了')
            msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
            msgBox.exec()

    def renewClicked(self):
        #刷新按钮功能实现
        if self.renewfunc:
            self.renewfunc()
        else:
            pass
            #print('renewfunc=None')
    #用于确认框的函数
    def msgAccepted(self):
        self.accepted=True

    def msgRejected(self):
        self.accepted=False

    def saveClicked(self):
        #附件保存按钮功能实现
        if self.downloadfile==[]:
            self.caution(text='没选择附件呢')
        else:
            for filename in self.downloadfile:
                #文件保存路径选择框
                msgBox=QWidget()
                fileName2, ok2 = QFileDialog.getSaveFileName(msgBox, "文件保存", "C:/"+filename, '(*.'+filename.split('.')[-1]+')')
                path = fileName2
                name = fileName2.split('/')[-1]
                seqnum=self.parsedictlist[self.currentpsd]['file']['filename'].index(filename)
                #print(seqnum)
                savestate=saveParsedFile(filename,self.parsedictlist[self.currentpsd]['file']['filedata'][seqnum],path,name)
                #print(savestate)
        #print(self.downloadfile)

    def setHeader(self,sender,reciever,subject,time):
        #设置邮件头信息（发件人，收件人，主题，时间）
        self.sender=sender if sender else '-'
        self.reciever=reciever if reciever else '-'
        self.subject=subject if subject else '-'
        self.time=time if time else '-'

    def showHeader(self):
        #显示邮件头信息
        hanzi_regex = compile(r'[\u4E00-\u9FA5]')#汉字正则表达式，用于左对齐
        if len(self.reciever)<85:
            self.breciever.setText(self.reciever+" "*(85-len(self.reciever)-len(hanzi_regex.findall(self.reciever))))
            self.breciever.setToolTip('')
        else:
            self.breciever.setText(self.reciever[0:80]+'....')
            self.breciever.setToolTip(self.reciever)
        self.bsender.setText(self.sender+" "*(85-len(self.sender)-len(hanzi_regex.findall(self.sender))))
        if len(self.subject)<85:
            self.bsubject.setText(self.subject+" "*(85-len(self.subject)-len(hanzi_regex.findall(self.subject))))
            self.bsubject.setToolTip('')
        else:
            self.bsubject.setText(self.subject[0:80]+'....')
            self.bsubject.setToolTip(self.subject)
        self.btime.setText(self.time+" "*(85-len(self.time)-len(hanzi_regex.findall(self.time))))

    def closeFilepart(self):
        #附件部分隐藏（不删除）
        self.lfile.close()
        self.save.close()
        self.line_2.close()
        for fb in self.file:
            fb.close()

    def showFilepart(self):
        #附件部分显示
        self.lfile.show()
        self.save.show()
        self.line_2.show()
        for fb in self.file:
            fb.show()

    def addFileButton(self,filename):
        #添加附件按钮（根据收到邮件的附件数目添加按钮）
        self.file.append(QtWidgets.QPushButton())
        self.file[-1].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.file[-1].setFlat(True)
        self.file[-1].setObjectName("file"+str(len(self.file)))
        self.file[-1].setText(filename)
        self.file[-1].setCheckable(True)
        self.file[-1].setChecked(False)
        self.file[-1].toggled.connect(self.fileButtonPress)

    def fileButtonPress(self):
        #点击附件按钮的功能实现
        for fb in self.file:
            if fb.isChecked():
                if fb.text() in self.downloadfile:
                    pass
                else:
                    self.downloadfile.append(fb.text())
            else:
                try:
                    self.downloadfile.remove(fb.text())
                except:
                    pass
        #根据是否选择来决定附件保存列表里面的内容
        #print(self.downloadfile)

    def showFileButton(self):
        #显示附件按钮
        layout=QGridLayout()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        #n/m用于根据附件数目控制显示排布
        n=0
        m=0
        maxbutton=6 if len(self.file)<12 else 12
        for fb in self.file:
            layout.addWidget(fb,m,n)
            n+=1
            if n%maxbutton==0:
                m+=1
                n=0
        self.filepart.addLayout(layout)

    def showParseDict(self,psd):
        #显示邮件（字典）
        self.setHeader(psd['from'],psd['to'],psd['subject'],psd['date'])
        #优先显示content1（如果有，这是其HTML版本）
        try:
            self.contenttext=psd['payload']['content1']
        except:
            try:
                self.contenttext=psd['payload']['content0']
            except:
                self.contenttext=''
        #针对正文含有图片的邮件，图片URL需要做本地化处理
        cidpart=compile('\"(cid:[^\"]*[jpg|png|bmp|gif])\"')
        cidlist=cidpart.findall(self.contenttext)
        for cid in cidlist:
            cid2='file:///'+getcwd().replace('\\','/')+'/user/user_maildata/'+self.username+'/'+cid.strip('cid:')
            self.contenttext=self.contenttext.replace(cid,cid2)
            self.contentph=True
        #根据该邮件的附件数目显示附件部分内容
        self.closeFilepart()
        self.file = []
        if psd['file']['filename'] != []:
            for fn in psd['file']['filename']:
                self.addFileButton(fn)
            self.showFileButton()
            self.showFilepart()
        else:
            pass
        self.showHeader()
        self.checkBoxChecked()

    def caution(self,title='啊哦',text='稍等'):
        #提示框
        msgBox = QMessageBox(QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))
        msgBox.setWindowOpacity(0.9)
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.exec()

class MsgDialog(QWidget):
    #该类为自定义对话框，用于部分需要临时生成自定义对话框的地方
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(409, 246)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.uplabel = QtWidgets.QLabel(Dialog)
        self.uplabel.setObjectName("uplabel")
        self.gridLayout.addWidget(self.uplabel, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(305, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.upinput = QtWidgets.QLineEdit(Dialog)
        self.upinput.setObjectName("upinput")
        self.gridLayout.addWidget(self.upinput, 1, 0, 1, 2)
        self.downlabel = QtWidgets.QLabel(Dialog)
        self.downlabel.setObjectName("downlabel")
        self.gridLayout.addWidget(self.downlabel, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(305, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.downinput = QtWidgets.QLineEdit(Dialog)
        self.downinput.setObjectName("downinput")
        self.gridLayout.addWidget(self.downinput, 3, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(384, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "另存为"))
        self.uplabel.setText(_translate("Dialog", "文件路径"))
        self.downlabel.setText(_translate("Dialog", "文件名"))

class DelThread(Thread):
    #删除线程，用于删除邮件
    def __init__(self,fmail,password,dpsd):
        super().__init__()
        self.fmail=fmail
        self.password=password
        self.dpsd=dpsd
        self.maildir='INBOX'
        #留给外部函数的接口（决定删除成功或失败时的动作）
        self.delfunc=None
        self.delfailfunc=None
        #是否删除在线数据（本程序中一直是True)
        self.sync=True

    def run(self):
        if not self.sync:
            if self.delfailfunc:
                self.delfailfunc()
            return
        try:
            delstate=False
            if type(self.dpsd)==type([]):
                #print('listd')
                for dps in self.dpsd:
                    #print('ready',self.fmail,self.password)
                    dstate = deleteEmailIMAP4(self.fmail, self.password, dps, self.maildir)
                    #print(dstate)
            else:
                dstate=deleteEmailIMAP4(self.fmail,self.password,self.dpsd,self.maildir)
            #print(dstate)
            if dstate:
                #print('online del fin')
                delstate=True
                if self.delfunc:
                    self.delfunc()
            else:
                delstate=False
                #print('online del failed')
                if self.delfailfunc:
                    self.delfailfunc()
        except:
            #print('error')
            if not delstate:
                if self.delfailfunc:
                    self.delfailfunc()
            pass

class DCbutton(QPushButton):
    #有双击功能的按钮
    def __init__(self,parent=None):
        super(DCbutton,self).__init__(parent)
        self.doubleclick=None

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.doubleclick:
            self.doubleclick()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    psdl=readWellmailDir('D:\works\ptest\email_proj2018','well_test')
    psdt={'subject':'-','from':'-','to':'-','date':'-','payload':{'content0':'-'},'file':{'filename':[]},'flag':'Empty'}
    psdt['file']['filename']=['1','2','3','4','5']
    win = MailBrowser()
    mw = QWidget()
    mw.setWindowTitle('收件')
    win.parsedictlist=psdl
    win.parsedictlist.append(psdt)
    win.username='well_test6'
    win.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
