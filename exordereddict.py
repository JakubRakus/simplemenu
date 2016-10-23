#! /usr/bin/env python3

from collections import OrderedDict

class ExOrderedDict(OrderedDict):

    def insert(self,newElement,after=None,before=None):
        dictKeys = list(self.keys())
        if after is not None and before is None:
            insPoint = dictKeys.index(after)+1
        elif after is None and before is not None:
            insPoint = dictKeys.index(before)
        else:
            raise SyntaxError('after or before should be set, but not simultanously')
        firstPart = ExOrderedDict((k,self[k]) for k in dictKeys[:insPoint])
        secondPart = ExOrderedDict((k,self[k]) for k in dictKeys[insPoint:])
        self.clear()
        for elem in [firstPart, newElement, secondPart]:
            self.update(elem)

if __name__ == '__main__':
    exDict = ExOrderedDict([('a',1),('c',3),('e',5)])
    print("original dict: ",exDict)
    exDict.insert({'b':2},after='a')
    print("b inserted AFTER a: ",exDict)
    exDict.insert({'d':4},before='e')
    print("d inserted BEFORE e: ",exDict)
