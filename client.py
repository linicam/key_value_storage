import requests

URL = "http://localhost:5000/"

OPS = ['put', 'put', 'put', 'put', 'get', 'get', 'get', 'delete', 'get', 'put', 'get', 'put', 'get', 'delete', 'get',
       'put', 'get', 'get', 'delete', 'get']
PARAMS = [('A', {'value': 'c'}), ('A', {'value': 'd'}), ('A', {'value': 'c'}), ('A', {'value': 'e'}), ('A'),
          ('A', {'time': 2}),
          ('B', {'time1': 0, 'time2': 10}), ('A', {'value': 'c'}), ('A'), ('B'), ('A', {'time1': 0, 'time2': 2}),
          ('B', {'value': 'Ae'}), ('B', {'time1': 1, 'time2': 10}), ('B'), ('B'), ('C', {'value': 'cE'}),
          ('C', {'time1': 0, 'time2': 13}), ('C', {'time1': 1, 'time2': 16}), ('C'), ('C')]


def _execute(ops, params):
    for i, op in enumerate(ops):
        # notice when i == 9, which is put('B'), the server returns 400, so no count added in the storage
        func = getattr(requests, op)
        param = params[i]
        uri = URL + param[0]
        data = param[1] if len(param) > 1 else None
        print i, func(uri, data=data).content


if __name__ == '__main__':
    _execute(OPS, PARAMS)
