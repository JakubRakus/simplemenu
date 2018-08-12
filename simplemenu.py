#! /usr/bin/env python3


from exordereddict import ExOrderedDict
from abc import ABC, abstractmethod
import weakref


class SMElement(ABC):

    @abstractmethod
    def __init__(self, elemCaption, elemFunction):
        self.caption = elemCaption
        self.function = elemFunction


class SMCommand(SMElement):

    def __init__(self, comCaption, comFunc=None):
        super().__init__(comCaption, comFunc)


class SMRadio(SMElement):

    def __init__(self, radioCaption, radioGroup, radioFunc=None, radioChecked=False):
        super().__init__(radioCaption, radioFunc)
        self.group = radioGroup
        self.checked = radioChecked


class SMCheckBox(SMElement):

    def __init__(self, cbCaption, cbFunc=None, cbChecked=False):
        super().__init__(cbCaption, cbFunc)
        self.checked = cbChecked


class SMSpecial(SMCommand): pass


class SimpleMenu(SMElement):

    def __init__(self, mTitle, mFunc=None, vLines=4, bCaption='Back'):
        super().__init__(mTitle, mFunc)
        if vLines < 1:
            raise ValueError('vLines should be greater than 0')
        self.lines = vLines
        self.__elements = ExOrderedDict()
        self.__elements['back'] = SMSpecial(bCaption)
        self.__focused = 0
        self.__firstToShow = 0
        self.__actualLevel = True
        self.__parentMenu = None

    def __getattr__(self, name):
        if hasattr(self, '_SimpleMenu__elements') and name in self.__elements.keys():
            return self.__elements[name]
        else:
            raise AttributeError

    def __delattr__(self, name):
        if hasattr(self, '_SimpleMenu__elements') and name in self.__elements.keys():
            self.delElement(name)
        else:
            self.__delattr__(name)

    def addElement(self, eName, eType, *args, **kwargs):
        self.__elements.insert({eName:eType(*args, **kwargs)}, before='back')
        #if new element is submenu, tell him 'Submenu, I'm Your father'
        if eType is SimpleMenu:
            self.__elements[eName].__parentMenu = weakref.ref(self)
            self.__elements[eName].__actualLevel = False
        self.__firstToShow = 0
        self.__focused = 0

    def delElement(self, eName=None):
        del self.__elements[eName]
        self.__firstToShow = 0
        self.__focused = 0

    def getActualLevel(self):
        if self.__actualLevel: #ok, I'm the active level
            return self
        else: #no, I'm not the active level, search my submenus
            for key, value in self.__elements.items():
                if type(value) is SimpleMenu:
                    return self.__elements[key].getActualLevel()

    def getActualView(self):
        level = self.getActualLevel()
        return list(level.__elements.items())[level.__firstToShow:(level.__firstToShow+level.lines)]

    def moveUp(self):
        level = self.getActualLevel()
        #we are at the first item, wrap around
        if level.__focused <= 0:
            level.__focused = len(level.__elements) - 1
            level.__firstToShow = level.__focused - level.lines + 1
            if level.__firstToShow < 0:
                level.__firstToShow = 0
        #not the first item, just move up
        else:
            level.__focused -= 1
            if level.__focused < level.__firstToShow:
                level.__firstToShow = level.__focused

    def moveDown(self):
        level = self.getActualLevel()
        #we are at the last item, wrap around
        if level.__focused >= (len(level.__elements) - 1):
            level.__focused = 0
            level.__firstToShow = 0
        #not the last item, just move down
        else:
            level.__focused += 1
            if level.__focused >= (level.__firstToShow + level.lines):
                level.__firstToShow += 1

    #only one level down in hierarchy
    def moveInside(self, submenu):
        level = self.getActualLevel()
        #we have to go deeper, change active level
        if type(submenu) is str:
            if submenu in level.__elements.keys():
                level.__elements[submenu].__actualLevel = True
                level.__actualLevel = False
            else:
                raise AttributeError('There is no \'{0}\' submenu at active level'.format(submenu))
        else:
            raise TypeError('Provided argument \'{0}\' is not a name of menu element'.format(submenu))

    #go to arbitrary chosen submenu
    def moveToSubmenu(self, submenu):
        level = self.getActualLevel()
        if type(submenu) is SimpleMenu:
            submenu.__actualLevel = True
            level.__actualLevel = False
        else:
            raise TypeError('Element \'{0}\' is not a submenu'.format(submenu))

    #only one level up in hierarchy
    def moveBack(self):
        level = self.getActualLevel()
        level.__actualLevel = False
        #call __parentMenu like a method() because of weak reference
        level.__parentMenu().__actualLevel = True

    def getElemProperties(self, element):
        return {k:v for k, v in vars(element).items() if not k.startswith('_')}

    def showTree(self, showProp=False, first=True, prefix=''):
        if first:
            print("{0}{1}".format(type(self).__name__, self.getElemProperties(self) if showProp else ''))
        elementsCount = len(self.__elements)
        for key, value in self.__elements.items():
            elementsCount -= 1
            if elementsCount:
                bars = '\u251c\u2500\u2574'
            else:
                bars = '\u2514\u2500\u2574'
            print("{0}{1}{2}:{3}{4}".format(prefix, bars, key, type(value).__name__, self.getElemProperties(value) if showProp else ''))
            if type(value) is SimpleMenu:
                self.__elements[key].showTree(showProp, False, prefix+'\u2502   ')

