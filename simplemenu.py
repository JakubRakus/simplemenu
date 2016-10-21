#! /usr/bin/env python3

from exordereddict import ExOrderedDict

class simpleMenu:

	def __init__(self,mTitle,mType='main',vLines=4,bCaption='Back'):
		self.menuType = mType
		self.menuTitle = mTitle
		self.visibleLines = vLines
		self.elementDict = ExOrderedDict()
		self.elementDict.update({'back':[bCaption,'s']})

	def addElement(self,eName,eCaption,eType):
		self.elementDict.insert({eName:[eCaption,eType]},before='back')

	def delElement(self,eName):
		del self.elementDict[eName]

	def getMenu(self):
		return list(i for i in self.elementDict.values())

if __name__ == '__main__':
	menu = simpleMenu('Title')
	menu.addElement('com1','Command 1','c')
	menu.addElement('com2','Command 2','c')
	menu.addElement('sub1','Submenu 1','m')
	print(menu.getMenu())
