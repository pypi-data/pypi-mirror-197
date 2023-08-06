# -*- coding: utf-8 -*-
from collections import defaultdict, namedtuple
from qtemplate import log, utils

Sync = namedtuple('Sync', 'qtmpl, expr, context, callback')


class DataStore(utils.Bunch):
    """ Datastore used to auto update widget values. """

    def __init__(self, *args, **kwargs):
        super(DataStore, self).__init__(*args, **kwargs)
        self._registry = defaultdict(list)  # Dict of {token: [Callbacks]}
    
    def register(self, qtmpl, token, callback, expr, context):
        """ Register a new value to this DataStore. """
        log.debug(f'Registering {token} -> {callback.__self__.__class__.__name__}.{callback.__name__}()')
        self._registry[token].append(Sync(qtmpl, expr, context, callback))

    def setValue(self, item, value):
        """ Update the specified value. This will additionally look up any registered
            sync values, and execute its callback function with the new data in place.
        """
        utils.rset(self, item, value)
        for token in sorted(k for k in self._registry.keys() if k.startswith(item)):
            for sync in self._registry[token]:
                value = sync.qtmpl._apply(sync.expr, sync.context, sync.callback)
    
    def listValues(self, root, path=''):
        """ Retutns a flattened list containing (key, value, type) for
            all values in this DataStore.
        """
        if getattr(root, 'items', None) is None:
            return [(path, str(root), utils.typeStr(root))]
        values = []
        for key, value in root.items():
            if key.startswith('_'): continue
            subpath = f'{path}.{key}'.lstrip('.')
            vtype = utils.typeStr(value)
            if isinstance(value, dict):
                values += self.listValues(value, subpath)
            elif isinstance(value, (tuple, list)):
                if len(str(value)) <= 20:
                    values.append((subpath, str(value), vtype))
                    continue
                for i in range(len(value)):
                    values += self.listValues(value[i], f'{subpath}.{i}')
            else:
                values.append((subpath, str(value), vtype))
        return sorted(values, key=lambda x: x[0])
    
    def printValues(self):
        """ Pretty print the values to console. """
        for row in self.listValues():
            print(row)
