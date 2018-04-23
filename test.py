import unittest

from key_value_storage import KeyValueStorage

OPS = ['put', 'put', 'put', 'put', 'get', 'get', 'get', 'delete', ]
PARAMETERS = [('A', 'c'), ('A', 'd'), ('A', 'c'), ('A', 'e'), ('A'), ('A', 2), ('B', 0, 10), ('A', 'c')]


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.storage = KeyValueStorage()

    def __execute(self, ops, params, expects):
        res = ''
        for i, op in enumerate(ops):
            func = getattr(self.storage, op)
            param = params[i]
            res = func(*param)
        self.assertEqual(res, expects)

    def test_put(self):
        ops = ['put']
        params = [('A', 'c')]
        expects = ['c']
        self.__execute(ops, params, expects)

    def test_get(self):
        ops = ['put', 'get']
        params = [('A', 'c'), ('A')]
        expects = ['c']
        self.__execute(ops, params, expects)

    def test_del(self):
        ops = ['put', 'delete', 'get']
        params = [('A', 'c'), ('A'), ('A')]
        expects = None
        self.__execute(ops, params, expects)

    def test_del_duplicate(self):
        ops = ['put', 'put', 'put', 'delete', 'get']
        params = [('A', 'c'), ('A', 'd'), ('A', 'c'), ('A', 'c'), ('A')]
        expects = ['d']
        self.__execute(ops, params, expects)

    def test_del_with_value(self):
        ops = ['put', 'put', 'delete', 'get']
        params = [('A', 'c'), ('A', 'd'), ('A', 'c'), ('A')]
        expects = ['d']
        self.__execute(ops, params, expects)

    def test_get_with_time(self):
        ops = ['put', 'put', 'put', 'get']
        params = [('A', 'c'), ('A', 'd'), ('A', 'e'), ('A', 1)]
        expects = ['c', 'd']
        self.__execute(ops, params, expects)

    def test_diff(self):
        ops = ['put', 'put', 'put', 'put', 'diff']
        params = [('A', 'c'), ('A', 'd'), ('A', 'e'), ('A', 'f'), ('A', 0, 2)]
        expects = ['d', 'e']
        self.__execute(ops, params, expects)

    def test_diff_after_del(self):
        ops = ['put', 'put', 'put', 'put', 'delete', 'diff']
        params = [('A', 'c'), ('A', 'd'), ('A', 'e'), ('A', 'f'), ('A'), ('A', 4, 5)]
        expects = None
        self.__execute(ops, params, expects)

    def test_diff_during_not_exist(self):
        ops = ['put', 'put', 'put', 'diff']
        params = [('A', 'c'), ('A', 'd'), ('B', 'e'), ('B', 0, 1)]
        expects = []
        self.__execute(ops, params, expects)

    def test_diff_after_del_and_put(self):
        ops = ['put', 'put', 'put', 'put', 'delete', 'put', 'diff']
        params = [('A', 'c'), ('A', 'd'), ('A', 'e'), ('A', 'f'), ('A'), ('A', 'g'), ('A', 4, 5)]
        expects = ['g']
        self.__execute(ops, params, expects)

    def test_diff_with_remove_and_add(self):
        ops = ['put', 'put', 'put', 'put', 'delete', 'put', 'diff']
        params = [('A', 'c'), ('A', 'd'), ('A', 'e'), ('A', 'f'), ('A', 'f'), ('A', 'g'), ('A', 4, 5)]
        expects = ['g']
        self.__execute(ops, params, expects)

    def test_get_not_exist(self):
        ops = ['get']
        params = [('A')]
        expects = None
        self.__execute(ops, params, expects)

    def test_del_not_exist(self):
        ops = ['delete']
        params = [('A')]
        expects = None
        self.__execute(ops, params, expects)

    def test_diff_not_exist(self):
        ops = ['diff']
        params = [('A', 2, 3)]
        expects = None
        self.__execute(ops, params, expects)


suite = unittest.TestLoader().loadTestsFromTestCase(StorageTests)
unittest.TextTestRunner(verbosity=2).run(suite)
