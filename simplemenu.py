#! /usr/bin/env python3

from sortedcontainers import SortedDict

class simpleMenu:

	def __init__(self,mtitle,mtype='main',vlines=4,bcaption='Back'):
		self.menuType = mtype
		self.menuTitle = mtitle
		self.visibleLines = vlines
		self.elementDict = SortedDict()
		self.addElement('back',bcaption,'s')

	def addElement(self,ename,ecaption,etype):
		self.elementDict[ename]=[ecaption,etype]

	def delElement(self,ename):
		del self.elementDict[ename]

	def getMenu(self):
		return list(i for i in self.elementDict.values())

if __name__ == '__main__':
	menu = simpleMenu('Title')
	menu.addElement('com1','Command 1','c')
	menu.addElement('com2','Command 2','c')
	menu.addElement('sub1','Submenu 1','m')
	print(menu.getMenu())
