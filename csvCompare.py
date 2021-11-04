# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compare.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import csv
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectDbButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectDbButton.setGeometry(QtCore.QRect(20, 20, 101, 25))
        self.selectDbButton.setObjectName("selectDbButton")
        self.listDb = QtWidgets.QListWidget(self.centralwidget)
        self.listDb.setGeometry(QtCore.QRect(20, 170, 161, 241))
        self.listDb.setObjectName("listDb")
        self.selectHqbutton = QtWidgets.QPushButton(self.centralwidget)
        self.selectHqbutton.setGeometry(QtCore.QRect(20, 60, 101, 25))
        self.selectHqbutton.setObjectName("selectHqbutton")
        self.selectDbPath = QtWidgets.QTextEdit(self.centralwidget)
        self.selectDbPath.setGeometry(QtCore.QRect(130, 20, 481, 25))
        self.selectDbPath.setObjectName("selectDbPath")
        self.beginButton = QtWidgets.QPushButton(self.centralwidget)
        self.beginButton.setGeometry(QtCore.QRect(270, 230, 91, 51))
        self.beginButton.setObjectName("beginButton")
        self.selectHqPath = QtWidgets.QTextEdit(self.centralwidget)
        self.selectHqPath.setGeometry(QtCore.QRect(130, 60, 481, 25))
        self.selectHqPath.setObjectName("selectHqPath")
        self.exportButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportButton.setGeometry(QtCore.QRect(20, 100, 101, 25))
        self.exportButton.setObjectName("exportButton")
        self.exportPath = QtWidgets.QTextEdit(self.centralwidget)
        self.exportPath.setGeometry(QtCore.QRect(130, 100, 481, 25))
        self.exportPath.setObjectName("exportPath")
        self.listHq = QtWidgets.QListWidget(self.centralwidget)
        self.listHq.setGeometry(QtCore.QRect(450, 170, 161, 241))
        self.listHq.setObjectName("listHq")
        # self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        # self.progressBar.setGeometry(QtCore.QRect(270, 320, 118, 23))
        # self.progressBar.setProperty("value", 24)
        # self.progressBar.setObjectName("progressBar")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(20, 150, 131, 16))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(450, 150, 131, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.selectDbButton.clicked.connect(self.setSelectDbPath)
        self.selectHqbutton.clicked.connect(self.setSelectHqpath)
        self.exportButton.clicked.connect(self.setExportPath)
        self.beginButton.clicked.connect(self.beginCompare)
        # self.listDb.clicked.connect(self.itemClickDb)
        # self.listHq.clicked.connect(self.itemClickHq)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "目录文件检索工具"))
        self.selectDbButton.setText(_translate("MainWindow", "选择营业部文件"))
        self.selectHqbutton.setText(_translate("MainWindow", "选择总部文件"))
        self.beginButton.setText(_translate("MainWindow", "开始比较"))
        self.exportButton.setText(_translate("MainWindow", "结果保存路径"))
        self.label_1.setText(_translate("MainWindow", "营业部文件"))
        self.label_2.setText(_translate("MainWindow", "总部文件"))

    def setSelectDbPath(self):
        try:
            # 调用QtWidgets.QFileDialog选择目录文件并赋予self.tempSelectDbPath，此处写死只要CSV文件
            self.tempSelectDbPath = QtWidgets.QFileDialog.getOpenFileNames(None, '选择需要检索的文件目录', os.getcwd(),
                                                                           '文档文件(*.csv)')
            # textedit里面填入路径
            self.selectDbPath.setText(self.tempSelectDbPath[0][0].rsplit('/', 1)[0])
            # 在list里填入该目录下所有文件的列表
            self.fileListDb = self.tempSelectDbPath[0]
            # print(self.fileList)
            num = 0  # 统计总数用
            self.listDb.clear()  # 清空列表内容
            for i in range(0, len(self.fileListDb)):
                filePath = self.fileListDb[i]  # 获取每个文件的具体路径
                if os.path.isfile(filePath):  # 判断是不是文件
                    num += 1
                    self.itemDb = QtWidgets.QListWidgetItem(self.listDb)  # 创建列表
                    self.itemDb.setText(self.fileListDb[i].split('/')[-1])
                    # print(self.fileList[i])
                    # print(self.item.text())
            self.statusbar.showMessage('营业部目录共有文件 ”' + str(num) + '“ 个')
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, '警告', '请选择一个有效路径或有效文件', QtWidgets.QMessageBox.Ok)
            print(e)

    def setSelectHqpath(self):
        try:
            # 调用QtWidgets.QFileDialog选择目录文件并赋予self.tempSelectHqPath，此处写死只要CSV文件
            self.tempSelectHqPath = QtWidgets.QFileDialog.getOpenFileNames(None, '选择需要检索的文件目录', os.getcwd(),
                                                                           '文档文件(*.csv)')
            # textedit里面填入路径
            self.selectHqPath.setText(self.tempSelectHqPath[0][0].rsplit('/', 1)[0])
            # 在list里填入该目录下所有文件的列表
            self.fileListHq = self.tempSelectHqPath[0]
            # print(self.fileList)
            num = 0  # 统计总数用
            self.listHq.clear()  # 清空列表内容
            for i in range(0, len(self.fileListHq)):
                filePath = self.fileListHq[i]  # 获取每个文件的具体路径
                if os.path.isfile(filePath):  # 判断是不是文件
                    num += 1
                    self.itemHq = QtWidgets.QListWidgetItem(self.listHq)  # 创建列表
                    self.itemHq.setText(self.fileListHq[i].split('/')[-1])
                    # print(self.fileList[i])
                    # print(self.item.text())
            self.statusbar.showMessage('总部目录共有文件 ”' + str(num) + '“ 个')
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, '警告', '请选择一个有效路径或有效文件', QtWidgets.QMessageBox.Ok)
            print(e)

    def setExportPath(self):
        try:
            self.tempExportPath = QtWidgets.QFileDialog.getExistingDirectory(None, '选择检索结果保存的目录', os.getcwd())
            self.exportPath.setText(self.tempExportPath)
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, '警告', '请选择一个有效路径', QtWidgets.QMessageBox.Ok)
            print(e)

    def beginCompare(self):
        db_list = self.tempSelectDbPath[0]
        # print(db_list)
        hq_list = self.tempSelectHqPath[0]
        for hq_file in hq_list:
            # print(hq_file)
            for db_file in db_list:
                self.csvParse(hq_file, db_file)
        QtWidgets.QMessageBox.information(None, '提示', '分析导出完成', QtWidgets.QMessageBox.Ok)

    def csvParse(self, hq_file, db_file):
        hq_list = []
        result_list = []
        try:
            with open(hq_file, 'r', newline='') as csv_hq:
                for hq in csv_hq:
                    hq_list.append(hq)
            with open(db_file, 'r', newline='') as csv_db:
                for db in csv_db:
                    if db not in hq_list:
                        result_list.append(db)
            if os.path.isdir(self.selectDbPath.toPlainText()) and os.path.isdir(self.selectHqPath.toPlainText()):
                if os.path.isdir(self.exportPath.toPlainText()):
                    with open(os.path.join(self.exportPath.toPlainText(),
                                           db_file.rsplit('.csv', 1)[0].rsplit('_', 1)[-1] + '_对比结果.csv'), 'w',
                              newline='') as f:
                        writer = csv.writer(f, dialect='excel')
                        for i in result_list:
                            writer.writerow([i])
                else:
                    QtWidgets.QMessageBox.information(None, '提示', '请检查导出目录是否正确', QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.warning(None, '警告', '请检查2个对比文件的目录是否正确', QtWidgets.QMessageBox.Ok)
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, '警告', '请检查以上三个选项是否都填写正确', QtWidgets.QMessageBox.Ok)
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())