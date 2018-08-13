#! /usr/bin/env python3


from collections import OrderedDict


class ExOrderedDict(OrderedDict):

    def insert(self, new_element, after=None, before=None):
        dict_keys = list(self.keys())
        if after is not None and before is None:
            ins_point = dict_keys.index(after) + 1
        elif after is None and before is not None:
            ins_point = dict_keys.index(before)
        else:
            raise SyntaxError('after or before should be set, but not simultaneously')
        first_part = ExOrderedDict((k,self[k]) for k in dict_keys[:ins_point])
        second_part = ExOrderedDict((k,self[k]) for k in dict_keys[ins_point:])
        self.clear()
        for elem in [first_part, new_element, second_part]:
            self.update(elem)


if __name__ == '__main__':
    exDict = ExOrderedDict([('a',1), ('c',3), ('e',5)])
    print("original dict: ",exDict)
    exDict.insert({'b':2}, after='a')
    print("b inserted AFTER a: ",exDict)
    exDict.insert({'d':4}, before='e')
    print("d inserted BEFORE e: ",exDict)
