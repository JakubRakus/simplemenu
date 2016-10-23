#! /usr/bin/env python3

from exordereddict import ExOrderedDict

allowedMenuTypes = ('main','sub')
allowedElementTypes = ('s','c','m')

class simpleMenu:

    def __init__(self,mTitle,mType='main',vLines=4,bCaption='Back',eCaption='Exit'):
        if mType not in allowedMenuTypes:
            raise ValueError('Invalid mType, allowed types: {0}'.format(allowedMenuTypes))
        self.menuType = mType
        self.menuTitle = mTitle
        if vLines < 1:
            raise ValueError('vLines should be greater than 0')
        self.visibleLines = vLines
        self.elementDict = ExOrderedDict()
        if self.menuType == 'sub':
            self.elementDict.update({'back':[bCaption,'s']})
        self.elementDict.update({'exit':[eCaption,'s']})

    def addElement(self,eName,eCaption,eType):
        if eType not in allowedElementTypes:
            raise ValueError('invalid eType, allowed types: {0}'.format(allowedElementTypes))
        bElement = 'back' if self.menuType == 'sub' else 'exit'
        self.elementDict.insert({eName:[eCaption,eType]},before=bElement)

    def delElement(self,eName):
        del self.elementDict[eName]

    def getMenu(self):
        return list(i for i in self.elementDict.items())

if __name__ == '__main__':
    menu = simpleMenu('Title')
    menu.addElement('com1','Command 1','c')
    menu.addElement('com2','Command 2','c')
    menu.addElement('sub1','Submenu 1','m')
    print(menu.getMenu())
