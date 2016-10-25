#! /usr/bin/env python3

from exordereddict import ExOrderedDict

class SMCommand:

    def __init__(self,comCaption,comFunc=None):
        self.caption = comCaption
        self.func = comFunc

class SMRadio:

    def __init__(self,radioCaption,radioGroup,radioFunc=None,radioChecked=False):
        self.caption = radioCaption
        self.group = radioGroup
        self.func = radioFunc
        self.checked = radioChecked

class SMCheckBox:

    def __init__(self,cbCaption,cbFunc=None,cbChecked=False):
        self.caption = cbCaption
        self.func = cbFunc
        self.checked = cbChecked

class SMSpecial(SMCommand): pass

class SimpleMenu:

    def __init__(self,mTitle,vLines=4,bCaption='Back'):
        self.title = mTitle
        if vLines < 1:
            raise ValueError('vLines should be greater than 0')
        self.lines = vLines
        self.elems = ExOrderedDict()
        self.elems['back'] = SMSpecial(bCaption)

    def addElement(self,eName,eType,*args,**kwargs):
        self.elems.insert({eName:eType(*args,**kwargs)},before='back')

    def delElement(self,eName):
        del self.elems[eName]

    def getMenu(self):
        return list(self.elems.items())

    def showTree(self,prefix=''):
        for key, value in self.elems.items():
            print("{0} |-- {1}: {2}".format(prefix,key,value))
            if type(value) is SimpleMenu:
                self.elems[key].showTree(prefix+'    ')

if __name__ == '__main__':
    menu = SimpleMenu('Title')
    menu.addElement('com1',SMCommand,'Command 1')
    menu.addElement('com2',SMCommand,'Command 2')
    menu.addElement('sub1',SimpleMenu,'Submenu 1')
    menu.elems['sub1'].addElement('com3',SMCommand,'Command 3')
    menu.elems['sub1'].addElement('sub2',SimpleMenu,'Submenu 2')
    menu.showTree()
