#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
import xml.dom.minidom
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QMouseEvent
#from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot				наверное не нужно

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#	класс кнопки на основе qpushbutton
#	добавлены возможность нажатия правой кнопки мыши 
#	и свойства координат и установленного значения
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

class QMyPushButton(QPushButton):
	#mouseReleaseEvent = pyqtSignal(bool)						наверное не нужно
	leftClick = QtCore.pyqtSignal()
	rightClick = QtCore.pyqtSignal()
	coordRow = -1
	coordCol = -1
	value = -1
	   	
	def __init__(self, parent):
		QPushButton.__init__(self, parent)
		self.setFlat(True)								#	плоская кнопка
	
	def mouseReleaseEvent(self, event):					#	определения нажатой кнопки
		if event.button() == 1:							#	левая кнопка мыши
			self.leftClick.emit()
		else:
			if event.button() == 2:						#	правая кнопка мыши
				self.rightClick.emit()
				
	def getCoord(self):									#	получить координаты кнопки
		return self.coordRow, self.coordCol
		
	def setCoord(self, row, col):						#	установить координаты кнопки
		self.coordRow = row
		self.coordCol = col
		
	def setIconS(self, icon):							#	установить иконку и размер
		self.setIcon(QIcon(icon))						#	иконка
		self.setIconSize(self.size())					#	размер
		
	def bclick(self, lc, rc):
		self.leftClick.connect(lc)						#	действие по нажатию ЛКМ
		self.rightClick.connect(rc)						#	действие по нажатию ПКМ
	
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#	класс реализации окна программы
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

class Saper(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()
		
	#------------------------------------------------------------------------------------
	#	инициализация пользовательского интерфейса
	#------------------------------------------------------------------------------------
		
	def initUI(self):
		
		#	использование глобальных переменных	
		global mRow, mCol, mCel, bS, bH, btn, target
		
		#	создание кнопок
		for i in range(mRow):
			for j in range(mCol):
				btnx = QMyPushButton(self)
				btnx.setText('')											#	текст пустой
				btnx.setCoord(i, j)											#	координаты
				btnx.setGeometry(bH + j*(bS+bH), bH + i*(bS+bH), bS, bS)	#	расположение и размеры
				btnx.setIconS('img\\b0.jpg')								#	иконка
				btnx.bclick(self.btnLClick, self.btnRClick)					#	действия по нажатию кнопок мыши
				btn.append(btnx)											#	добавить кнопку в массив
		
		#	новая игра
		self.newGame()
		
		#	кнопка начала новой игры
		btnNG = QPushButton('NEW GAME', self)														#	кнопка с текстом "NEW GAME"
		btnNG.setGeometry(int((mCol*(bS + bH) + bH)/2 - 2.5*bS), mRow*(bS + bH) + bH, 5*bS, bS)		#	размер и расположение кнопки
		btnNG.clicked.connect(self.newGame)															#	действие по нажатию
		
		self.setGeometry(300, 300, mCol*(bS + bH) + bH, (mRow + 1)*(bS + bH) + bH)	#	размер и расположение окна
		self.setWindowTitle('SAPER')												#	заголовок окна
		self.setWindowIcon(QIcon('img\\bomb.jpg'))									#	иконка
		self.show()																	#	отобразить окно
		
	#------------------------------------------------------------------------------------
	#	реализация начала новой игры
	#------------------------------------------------------------------------------------
	
	def newGame(self):
		
		# 	использование глобальных переменных
		global btn, target, mRow, mCol
		
		# 	установка нулевых значений
		for i in range(mRow*mCol):
			btn[i].value = ''
			btn[i].setEnabled(True)
			btn[i].setIcon(QIcon('img\\b0.jpg'))
			target[i] = 0
		
		# 	создание задачи
		k = 0
		while k < mCel:
			i = random.randint(0, mRow*mCol-1)
			if target[i] != 9:
				target[i] = 9
				k = k + 1
				
		# 	установка подсказок
		for i in range(mRow):
			for j in range(mCol):
				if target[i*mCol+j] != 9:
					if i > 0 and j > 0:									# 	кнопка слева сверху (ЛВ)
						if target[(i-1)*mCol+j-1] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
					if i > 0:											# 	кнопка слева (Л)
						if target[(i-1)*mCol+j] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
					if i > 0 and j < (mCol-1):							# 	кнопка слева снизу (ЛН)
						if target[(i-1)*mCol+j+1] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
					if j > 0:											# 	кнопка сверху (В)
						if target[i*mCol+j-1] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
					if j < (mCol-1):									# 	кнопка снизу (Н)
						if target[i*mCol+j+1] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
					if i < (mRow-1) and j > 0:							# 	кнопка справа сверху (ПВ)
						if target[(i+1)*mCol+j-1] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
					if i < (mRow-1):									# 	кнопка справа (П)
						if target[(i+1)*mCol+j] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
					if i < (mRow-1) and j < (mCol-1):					# 	кнопка справа снизу (ПН)
						if target[(i+1)*mCol+j+1] == 9:
							target[i*mCol+j] = target[i*mCol+j] + 1
	
	#-----------------------------------------------------------------------------
	#	реализация нажатия на левую кнопку мыши
	#-----------------------------------------------------------------------------
	
	def btnLClick(self):
	
		#	использование глобальных переменных
		global mRow, mCol
		
		#	получение координат кнопки из её свойств	
		row, col = self.sender().getCoord()
		
		#	перевод координат двумерного массива в одномерный
		coord = row*mCol+col
		
		#	если кнопка пустая, "взломать" её
		if btn[coord].value == '':
			self.brokeBlock(row, col)
			
		#	иначе, если на кнопке не установлен флаг и установлено значение числа,
		#	считаем, сколько флагов установлено на соседних клетках
		#	и, если количество флагов равно установленному значению,
		#	"взламываем" клетки, не "взломанные" ранее
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
		
		#	проверка на завершение игры победой
		self.check()					
		
	#-----------------------------------------------------------------------------
	#	реализация нажатия на правую кнопку мыши
	#-----------------------------------------------------------------------------
	
	def btnRClick(self):
		
		#	использование глобальных переменных
		global mCol
		
		#	получение координат кнопки из её свойств	
		row, col = self.sender().getCoord()
		
		#	перевод координат двумерного массива в одномерный
		coord = row*mCol+col
		
		#	если кнопка пустая, установить в неё флаг
		if btn[coord].value == '':
			btn[coord].setIcon(QIcon('img\\flag.jpg'))
			btn[coord].value = 'F'
			
		#	иначе, если флаг уже установлен, снять его и сделать кнопку пустой
		else:
			if btn[coord].value == 'F':
				btn[coord].setIcon(QIcon('img\\b0.jpg'))
				btn[coord].value = ''
				
		#	проверка на завершение игры победой
		self.check()
		
	#-----------------------------------------------------------------------------
	#	"взлом" неоткрытой клетки
	#	после чего, если возле указанной клетки бомб нет,
	#	"взламываются" все соседние клетки
	#-----------------------------------------------------------------------------	
		
	def brokeBlock(self, row, col):
		
		#	использование глобальных переменных
		global mRow, mCol
		
		#	перевод координат двумерного массива в одномерный
		coord = row*mCol+col
		
		#	следующие действия производятся только, если раньше никаких действий с клеткой не производилось
		if btn[coord].value == '':
		
			#	если значение равно 0, то кнопка становится недоступна,
			#	ей устанавливается значение ' ' (пробел) и "взламываются" 
			#	все соседние кнопки, при их наличии
			if target[coord] == 0:
				btn[coord].setEnabled(False)
				btn[coord].value = ' '
				if row > 0 and col > 0:					#	ЛВ
					self.brokeBlock(row-1, col-1)
				if row > 0:								#	Л
					self.brokeBlock(row-1, col)
				if row > 0 and col < (mCol-1):			#	ЛН
					self.brokeBlock(row-1, col+1)
				if col > 0:								#	В
					self.brokeBlock(row, col-1)
				if col < (mCol-1):						#	Н
					self.brokeBlock(row, col+1)
				if row < (mRow-1) and col > 0:			#	ПВ
					self.brokeBlock(row+1, col-1)
				if row < (mRow-1):						#	П
					self.brokeBlock(row+1, col)
				if row < (mRow-1) and col < (mCol-1):	#	ПН
					self.brokeBlock(row+1, col+1)
			else:
			
				#	если значение равно 9, то помалась "бомба"
				#	игра завершена
				#	на всех клетках устанавливается иконка "бомба" и предлагается начать новую игру
				
				
				#																							ДОБАВИТЬ ФЛАГ ЗАВЕРШЕННОЙ ИГРЫ И ПРОВЕРЯТЬ ЕГО ПРИ НАЖАТИИ НА КНОПКУ	
				
				
				if target[coord] == 9:
					for i in range(mRow*mCol):
						btn[i].setIcon(QIcon('img\\bomb.jpg'))
						btn[i].setEnabled(True)
				else:
					#	иначе устанавливается иконка соответствующего значения
					btn[coord].value = target[coord]
					btn[coord].setIcon(QIcon(self.getIcon(target[coord])))
		
	#-----------------------------------------------------------------------------
	#	проверка на завершение игры победой
	#-----------------------------------------------------------------------------
	
	def check(self):
	
		#	использование глобальных переменных
		global mCel, mRow, mCol
		
		#	счетчик "невзломанных" кнопок
		use = 0
		for i in range(mRow*mCol):
			if btn[i].value == '':
				use = use + 1
		
		#	если "невзломанных" кнопок не осталось, выполняется подсчет установленных флагов
		if use == 0:
			flag = mCel
			for i in range(mRow*mCol):
				if btn[i].value == 'F' and target[i] == 9:
					flag = flag - 1
			
			#	если количество флагов равно количеству "заминированных" клеток согласно задаче, игра завершена
			#	на всех клетках устанавливается иконка "флаг" и предлагается начать новую игру
			if flag == 0:
				for i in range(mRow*mCol):
					btn[i].setIcon(QIcon('img\\flag.jpg'))
					btn[i].setEnabled(True)
		
	#------------------------------------------------------------------------------------
	#	установка на кнопку рисунка соответствующего её значению
	#------------------------------------------------------------------------------------
		
	def getIcon(self, trg):
		a = { 0: 'b0', 1: 'b1', 2: 'b2', 3: 'b3', 4: 'b4', 5: 'b5', 6: 'b6', 7: 'b7', 8: 'b8', 9: 'bomb', '': 'b0', 'F': 'flag', } 
		return 'img\\' + a[trg] + '.jpg'
		
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

if __name__ == '__main__':

	defaultSettings = ['<?xml version="1.0" encoding="utf-8"?>', '<saper>', '	<row>5</row>', '	<col>8</col>', '	<dif>7</dif>', '</saper>']

	app = QApplication(sys.argv)
	
	#					ДОБАВИТЬ ПРОВЕРКУ НА НАЛИЧИЕ XML, ПРИ ОТСУТСТВИИ СОЗДАТЬ НОВЫЙ СО ЗНАЧЕНИЯМИ ПО УМОЛЧАНИЮ
	
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

	#	глобальные переменные
	mRow = xmlRow					#	количество строк
	mCol = xmlCol					#	количество столбцов
	mDif = 1/xmlDif					#	сложность
	mCel = int(mRow*mCol*mDif)		#	количество "заминированных" клеток устанавливается в зависимости от количества столбцов и строк и сложности
	bS, bH = 38, 7					#	размеры кнопки и просвета между кнопками	
	btn = []						#	пустой массив кнопок
	target = []						#	пустой массив задачи заполняется нулями
	for i in range(mRow):
		for j in range(mCol):
			target.append(0)
		
	w = Saper()
	
	sys.exit(app.exec_())