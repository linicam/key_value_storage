import bisect
import collections
import time

'''
Use a dictionary for storage, the input key as the key, and a self defined structure StorageNode as the value.
for every StorageNode, it has two variables, __values stores the current values for the key, and __shortcuts stores 
the current value of __values and the time whenever the __values's value is changed, representing the history.

input key and value should be strings, and time should be an integer.
'''


class _StorageNode:
    # use collections.OrderedDict for __shortcuts so that
    # the iteration sequence will be in the same order with the input.
    def __init__(self):
        self.__values = []
        self.__shortcuts = collections.OrderedDict()

    # add a new shortcut, with current time as the key.
    def __add_shortcut(self, t):
        self.__shortcuts[t] = self.__values[:]

    # time complexity: O(n)
    # space complexity: O(1)
    # n is the length of __values.

    # for put() method, add new value to the node and make a shortcut due to the change.
    def add_value(self, value, t):
        self.__values.append(value)
        self.__add_shortcut(t)
        return self.__values

    # time complexity: O(1) if no time inputted; O(n) if time inputted,
    # space complexity: O(1) if no time inputted, O(n) if time inputted
    # n is the length of __shortcuts.
    # in Python3, time complexity could be reduced to O(log n) with inputted time,
    # due to the different implementation of dictionary.keys().

    # for get() method, when argument time is None, it means the input argument only contains key,
    # or else it also contains time.
    def get_values(self, t):
        if t is None:
            return self.__values
        else:
            keys = self.__shortcuts.keys()
            ind = bisect.bisect(keys, t)
            return self.__shortcuts[keys[ind - 1]] if ind > 1 else []

    # time complexity: O(n)
    # space complexity: O(n)
    # n is the length of __values.

    # for del() method, delete all values in __values that are equal to the argument value, and make a shortcut.
    def delete_value(self, value, t):
        self.__values = [v for v in self.__values if v != value]
        self.__add_shortcut(t)
        return self.__values

    # time complexity: O(max(ls, lv))
    # space complexity O(max(ls, lv))
    # ls is the length of __shortcuts, lv is the length of the __values at the specific time.

    # for diff() method, calculate the differences in __values for the input time1 and time2, the compared
    # value is the result __values of the operation took place at time1 or time2.
    # only counts the values added and not removed during this time.
    def diff(self, time1, time2):
        if time1 >= time2:
            return []
        keys = self.__shortcuts.keys()

        # find the index of time1 and time2 in __shortcuts.keys(),
        # if equal value exists, keys[ind - 1] == keys[ind] < keys[ind + 1]
        a, b = [], []
        for i in (time1, time2):
            ind = bisect.bisect(keys, i)
            if i == time1:
                a = collections.Counter(self.__shortcuts[keys[ind - 1]]) if ind != 0 else []
            else:
                b = self.__shortcuts[keys[ind - 1]] if ind != 0 else []

        # filter values in __values at time2 which are not in the overlapped values at time1 and time2.
        res = []
        for v in b:
            if v in a:
                a[v] -= 1
                if a[v] == 0:
                    del a[v]
            else:
                res.append(v)
        return res


class KeyValueStorage:
    def __init__(self):
        self.__storage = collections.defaultdict(_StorageNode)
        self.__time = -1

    # temporarily use self defined time counter here, due to the small number of operations and data,
    # hard to calculate the time difference between them accurately
    def __set_timer(self):
        # self.__time = int(time.time() * (10 ** 9))
        self.__time += 1

    def get(self, key, t=None):
        self.__set_timer()
        print 'get', self.__time, self.__storage.keys()
        return self.__storage[key].get_values(t) if key in self.__storage else None

    def put(self, key, value):
        self.__set_timer()
        return self.__storage[key].add_value(value, self.__time)

    def delete(self, key, value=None):
        self.__set_timer()
        if key not in self.__storage:
            return
        if value is None:
            del self.__storage[key]
            return []
        return self.__storage[key].delete_value(value, self.__time)

    def diff(self, key, time1, time2):
        self.__set_timer()
        print 'diff', self.__time, self.__storage.keys()
        return self.__storage[key].diff(time1, time2) if key in self.__storage else None
