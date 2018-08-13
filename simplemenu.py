#! /usr/bin/env python3


from exordereddict import ExOrderedDict
from abc import ABC, abstractmethod
import weakref


class SMElement(ABC):

    @abstractmethod
    def __init__(self, elem_caption, elem_function):
        self.caption = elem_caption
        self.function = elem_function


class SMCommand(SMElement):

    def __init__(self, com_caption, com_func=None):
        super().__init__(com_caption, com_func)


class SMRadio(SMElement):

    def __init__(self, radio_caption, radio_group, radio_func=None, radio_checked=False):
        super().__init__(radio_caption, radio_func)
        self.group = radio_group
        self.checked = radio_checked


class SMCheckBox(SMElement):

    def __init__(self, cb_caption, cb_func=None, cb_checked=False):
        super().__init__(cb_caption, cb_func)
        self.checked = cb_checked


class SMSpecial(SMCommand):
    pass


class SimpleMenu(SMElement):

    def __init__(self, menu_title, menu_func=None, menu_lines=4, back_caption='Back'):
        super().__init__(menu_title, menu_func)
        if menu_lines < 1:
            raise ValueError('menu_lines should be greater than 0')
        self.lines = menu_lines
        self.__elements = ExOrderedDict()
        self.__elements['back'] = SMSpecial(back_caption)
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
            self.del_element(name)
        else:
            self.__delattr__(name)

    def add_element(self, elem_name, elem_type, *args, **kwargs):
        self.__elements.insert({elem_name: elem_type(*args, **kwargs)}, before='back')
        # if new element is submenu, tell him 'Submenu, I'm Your father'
        if elem_type is SimpleMenu:
            self.__elements[elem_name].__parentMenu = weakref.ref(self)
            self.__elements[elem_name].__actualLevel = False
        self.__firstToShow = 0
        self.__focused = 0

    def del_element(self, elem_name=None):
        del self.__elements[elem_name]
        self.__firstToShow = 0
        self.__focused = 0

    def get_active_level(self):
        if self.__actualLevel:  # ok, I'm the active level
            return self
        else:  # no, I'm not the active level, search my submenus
            for key, value in self.__elements.items():
                if type(value) is SimpleMenu:
                    return self.__elements[key].get_active_level()

    def get_active_view(self):
        level = self.get_active_level()
        return list(level.__elements.items())[level.__firstToShow:(level.__firstToShow + level.lines)]

    def move_up(self):
        level = self.get_active_level()
        # we are at the first item, wrap around
        if level.__focused <= 0:
            level.__focused = len(level.__elements) - 1
            level.__firstToShow = level.__focused - level.lines + 1
            if level.__firstToShow < 0:
                level.__firstToShow = 0
        # not the first item, just move up
        else:
            level.__focused -= 1
            if level.__focused < level.__firstToShow:
                level.__firstToShow = level.__focused

    def move_down(self):
        level = self.get_active_level()
        # we are at the last item, wrap around
        if level.__focused >= (len(level.__elements) - 1):
            level.__focused = 0
            level.__firstToShow = 0
        # not the last item, just move down
        else:
            level.__focused += 1
            if level.__focused >= (level.__firstToShow + level.lines):
                level.__firstToShow += 1

    # only one level down in hierarchy
    def move_inside(self, submenu):
        level = self.get_active_level()
        # we have to go deeper, change active level
        if type(submenu) is str:
            if submenu in level.__elements.keys():
                level.__elements[submenu].__actualLevel = True
                level.__actualLevel = False
            else:
                raise AttributeError('There is no \'{0}\' submenu at active level'.format(submenu))
        else:
            raise TypeError('Provided argument \'{0}\' is not a name of menu element'.format(submenu))

    # go to arbitrary chosen submenu
    def move_to_submenu(self, submenu):
        level = self.get_active_level()
        if type(submenu) is SimpleMenu:
            submenu.__actualLevel = True
            level.__actualLevel = False
        else:
            raise TypeError('Element \'{0}\' is not a submenu'.format(submenu))

    # only one level up in hierarchy
    def move_back(self):
        level = self.get_active_level()
        level.__actualLevel = False
        # call __parentMenu like a method() because of weak reference
        level.__parentMenu().__actualLevel = True

    @staticmethod
    def get_elem_properties(element):
        return {k: v for k, v in vars(element).items() if not k.startswith('_')}

    def show_tree(self, show_prop=False, first=True, prefix=''):
        if first:
            print("{0}{1}".format(type(self).__name__, self.get_elem_properties(self) if show_prop else ''))
        elements_count = len(self.__elements)
        for key, value in self.__elements.items():
            elements_count -= 1
            if elements_count:
                bars = '\u251c\u2500\u2574'
            else:
                bars = '\u2514\u2500\u2574'
            print("{0}{1}{2}:{3}{4}".format(prefix, bars, key, type(value).__name__,
                                            self.get_elem_properties(value) if show_prop else ''))
            if type(value) is SimpleMenu:
                self.__elements[key].show_tree(show_prop, False, prefix + '\u2502   ')
