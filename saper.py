#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
import xml.dom.minidom
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QMouseEvent


class QMyPushButton(QPushButton):
    leftClick = QtCore.pyqtSignal()
    rightClick = QtCore.pyqtSignal()
    coordRow = -1
    coordCol = -1
    value = -1

    def __init__(self, parent):
        QPushButton.__init__(self, parent)
        self.setFlat(True)

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.leftClick.emit()
        else:
            if event.button() == 2:
                self.rightClick.emit()

    def getCoord(self):
        return self.coordRow, self.coordCol

    def setCoord(self, row, col):
        self.coordRow = row
        self.coordCol = col

    def setIconS(self, icon):
        self.setIcon(QIcon(icon))
        self.setIconSize(self.size())

    def bclick(self, lc, rc):
        self.leftClick.connect(lc)
        self.rightClick.connect(rc)


class Saper(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global mRow, mCol, mCel, bS, bH, btn, target

        for i in range(mRow):
            for j in range(mCol):
                btnx = QMyPushButton(self)
                btnx.setText('')
                btnx.setCoord(i, j)
                btnx.setGeometry(bH + j*(bS+bH), bH + i*(bS+bH), bS, bS)
                btnx.setIconS('img\\b0.jpg')
                btnx.bclick(self.btnLClick, self.btnRClick)
                btn.append(btnx)

        self.newGame()
        btnNG = QPushButton('NEW GAME', self)
        btnNG.setGeometry(int((mCol*(bS + bH) + bH)/2 - 2.5*bS), mRow*(bS + bH) + bH, 5*bS, bS)
        btnNG.clicked.connect(self.newGame)

        self.setGeometry(300, 300, mCol*(bS + bH) + bH, (mRow + 1)*(bS + bH) + bH)
        self.setWindowTitle('SAPER')
        self.setWindowIcon(QIcon('img\\bomb.jpg'))
        self.show()


    def newGame(self):
        global btn, target, mRow, mCol

        for i in range(mRow*mCol):
            btn[i].value = ''
            btn[i].setEnabled(True)
            btn[i].setIcon(QIcon('img\\b0.jpg'))
            target[i] = 0

        k = 0
        while k < mCel:
            i = random.randint(0, mRow*mCol-1)
            if target[i] != 9:
                target[i] = 9
                k = k + 1

        for i in range(mRow):
            for j in range(mCol):
                if target[i*mCol+j] != 9:
                    if i > 0 and j > 0:
                        if target[(i-1)*mCol+j-1] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1
                    if i > 0:
                        if target[(i-1)*mCol+j] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1
                    if i > 0 and j < (mCol-1):
                        if target[(i-1)*mCol+j+1] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1
                    if j > 0:
                        if target[i*mCol+j-1] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1
                    if j < (mCol-1):
                        if target[i*mCol+j+1] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1
                    if i < (mRow-1) and j > 0:
                        if target[(i+1)*mCol+j-1] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1
                    if i < (mRow-1):
                        if target[(i+1)*mCol+j] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1
                    if i < (mRow-1) and j < (mCol-1):
                        if target[(i+1)*mCol+j+1] == 9:
                            target[i*mCol+j] = target[i*mCol+j] + 1


    def btnLClick(self):
        global mRow, mCol

        row, col = self.sender().getCoord()
        coord = row*mCol+col

        if btn[coord].value == '':
            self.brokeBlock(row, col)
        else:
            if btn[coord].value != 'F':
                flag = 0
                if row > 0 and col > 0:
                    if btn[(row-1)*mCol+col-1].value == 'F':
                        flag = flag + 1
                if row > 0:
                    if btn[(row-1)*mCol+col].value == 'F':
                        flag = flag + 1
                if row > 0 and col < (mCol-1):
                    if btn[(row-1)*mCol+col+1].value == 'F':
                        flag = flag + 1
                if col > 0:
                    if btn[row*mCol+col-1].value == 'F':
                        flag = flag + 1
                if col < (mCol-1):
                    if btn[row*mCol+col+1].value == 'F':
                        flag = flag + 1
                if row < (mRow-1) and col > 0:
                    if btn[(row+1)*mCol+col-1].value == 'F':
                        flag = flag + 1
                if row < (mRow-1):
                    if btn[(row+1)*mCol+col].value == 'F':
                        flag = flag + 1
                if row < (mRow-1) and col < (mCol-1):
                    if btn[(row+1)*mCol+col+1].value == 'F':
                        flag = flag + 1
                if flag == btn[coord].value:
                    if row > 0 and col > 0:
                        if btn[(row-1)*mCol+col-1].value != 'F':
                            self.brokeBlock(row-1, col-1)
                    if row > 0:
                        if btn[(row-1)*mCol+col].value != 'F':
                            self.brokeBlock(row-1, col)
                    if row > 0 and col < (mCol-1):
                        if btn[(row-1)*mCol+col+1].value != 'F':
                            self.brokeBlock(row-1, col+1)
                    if col > 0:
                        if btn[row*mCol+col-1].value != 'F':
                            self.brokeBlock(row, col-1)
                    if col < (mCol-1):
                        if btn[row*mCol+col+1].value != 'F':
                            self.brokeBlock(row, col+1)
                    if row < (mRow-1) and col > 0:
                        if btn[(row+1)*mCol+col-1].value != 'F':
                            self.brokeBlock(row+1, col-1)
                    if row < (mRow-1):
                        if btn[(row+1)*mCol+col].value != 'F':
                            self.brokeBlock(row+1, col)
                    if row < (mRow-1) and col < (mCol-1):
                        if btn[(row+1)*mCol+col+1].value != 'F':
                            self.brokeBlock(row+1, col+1)

        self.check()


    def btnRClick(self):
        global mCol

        row, col = self.sender().getCoord()
        coord = row*mCol+col

        if btn[coord].value == '':
            btn[coord].setIcon(QIcon('img\\flag.jpg'))
            btn[coord].value = 'F'
        else:
            if btn[coord].value == 'F':
                btn[coord].setIcon(QIcon('img\\b0.jpg'))
                btn[coord].value = ''

        self.check()


    def brokeBlock(self, row, col):
        global mRow, mCol
        coord = row*mCol+col

        if btn[coord].value == '':
            if target[coord] == 0:
                btn[coord].setEnabled(False)
                btn[coord].value = ' '
                if row > 0 and col > 0:
                    self.brokeBlock(row-1, col-1)
                if row > 0:
                    self.brokeBlock(row-1, col)
                if row > 0 and col < (mCol-1):
                    self.brokeBlock(row-1, col+1)
                if col > 0:
                    self.brokeBlock(row, col-1)
                if col < (mCol-1):
                    self.brokeBlock(row, col+1)
                if row < (mRow-1) and col > 0:
                    self.brokeBlock(row+1, col-1)
                if row < (mRow-1):
                    self.brokeBlock(row+1, col)
                if row < (mRow-1) and col < (mCol-1):
                    self.brokeBlock(row+1, col+1)
            else:
                if target[coord] == 9:
                    for i in range(mRow*mCol):
                        btn[i].setIcon(QIcon('img\\bomb.jpg'))
                        btn[i].setEnabled(True)
                else:
                    btn[coord].value = target[coord]
                    btn[coord].setIcon(QIcon(self.getIcon(target[coord])))


    def check(self):
        global mCel, mRow, mCol
        use = 0

        for i in range(mRow*mCol):
            if btn[i].value == '':
                use = use + 1

        if use == 0:
            flag = mCel
            for i in range(mRow*mCol):
                if btn[i].value == 'F' and target[i] == 9:
                    flag = flag - 1

            if flag == 0:
                for i in range(mRow*mCol):
                    btn[i].setIcon(QIcon('img\\flag.jpg'))
                    btn[i].setEnabled(True)


    def getIcon(self, trg):
        a = { 0: 'b0', 1: 'b1', 2: 'b2', 3: 'b3', 4: 'b4', 5: 'b5', 6: 'b6', 7: 'b7', 8: 'b8', 9: 'bomb', '': 'b0', 'F': 'flag', }
        return 'img\\' + a[trg] + '.jpg'


if __name__ == '__main__':
    defaultSettings = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<saper>',
        '    <row>5</row>',
        '    <col>8</col>',
        '    <dif>7</dif>',
        '</saper>',
    ]
    app = QApplication(sys.argv)

    try:
        dom = xml.dom.minidom.parse("saper.xml")
    except:
        f = open('saper.xml', 'w')
        for i in range(6):
            f.write(str(defaultSettings[i]))
        dom = xml.dom.minidom.parse("saper.xml")

    dom.normalize()
    xmlRow = int((dom.getElementsByTagName("row")[0]).childNodes[0].nodeValue)
    xmlCol = int((dom.getElementsByTagName("col")[0]).childNodes[0].nodeValue)
    xmlDif = int((dom.getElementsByTagName("dif")[0]).childNodes[0].nodeValue)

    mRow = xmlRow
    mCol = xmlCol
    mDif = 1/xmlDif
    mCel = int(mRow*mCol*mDif)
    bS, bH = 38, 7
    btn = []
    target = []
    for i in range(mRow):
        for j in range(mCol):
            target.append(0)

    w = Saper()
    sys.exit(app.exec_())
