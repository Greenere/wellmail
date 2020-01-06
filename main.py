# -*- coding: utf-8 -*-

#主界面

#Main entrance
#Written by Haoyang Li

from UIMain import MainUi
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys

app = QApplication(sys.argv)
#设置窗口
window=QWidget()
window.setWindowIcon(QtGui.QIcon('img/wellicon.ico'))#图标
window.setWindowTitle('WELLMAIL邮箱')#标题
#加载主界面
mainform=MainUi()
mainform.setupUi(window)
mainform.setUser()
window.show()
sys.exit(app.exec_())
