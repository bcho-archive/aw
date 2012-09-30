#coding: utf-8

from utils import expand, real_len, TAB_WIDTH


class Desc(object):
    '''Column description.

    :param name: the name of the column.
    :param random_generator: A random geneartor, which returns somethings
                             randomly basic on given dataset and previous
                             generated data.
    :param dataset: dataset for generating random data.
    :param children: declares and gives the descriptions for the sub dataset.
    :param unique: declares whether the column is unique.
    '''

    def __init__(self, name, random_generator, dataset=None, children=None,
                 unique=None):
        self.name = name
        self.random_generator = random_generator
        self.dataset = dataset
        self.children = children
        self.unique = True if unique else False

    def __str__(self):
        if self.unique:
            return '<Desc(%s unique)>' % (self.name)
        else:
            return '<Desc(%s)>' % (self.name)

    def __repr__(self):
        return self.__str__()


class Data(dict):
    '''A data row in the dataset. Just like a dict object, but the key order is
    fixed rather than sort by hash.'''
    def __init__(self, header):
        self.header = header
        for key in header:
            self[key] = None

    def __str__(self):
        return self.table

    def __repr__(self):
        return self.__str__()

    def keys(self):
        #: Fix key's order rather than base on hash
        return self.header

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    @property
    def table(self):
        '''Generate a mysql like result table'''
        # more pythonic approach for assigning value to multi vars?
        header, body, sep = [''], [''], ['']
        for key, value in self.items():
            if isinstance(value, Dataset):
                value = value.summarize()
            value = str(value)
            width = real_len(max(len(key), len(value)))
            header.append(expand(key, width))
            body.append(expand(value, width))
            sep.append('-' * (width + TAB_WIDTH))
        for i in (header, body, sep):
            i.append('')
        header = '|'.join(header)
        body = '|'.join(body)
        sep = '+'.join(sep)
        return '\n'.join((sep, header, sep, body, sep))


class Dataset(object):
    '''A dataset.'''
    def __init__(self, header, body):
        self.header = header
        self.body = body

    def __len__(self):
        return len(self.body)

    def __getitem__(self, idx):
        return self.body[idx]

    def __setitem__(self, idx, value):
        self.body[idx] = value

    def __delitem__(self, idx):
        del self.body[idx]

    def __str__(self):
        return self.table

    def __repr__(self):
        return self.__str__()

    @property
    def table(self):
        '''Generate a mysql like result table'''
        header, body, sep = [''], [], ['']

        #: find out the max length of word of each column
        max_len = {}
        for key in self.header:
            width = len(str(key))
            for line in self.body:
                if isinstance(line[key], Dataset):
                    value = line[key].summarize()
                else:
                    value = str(line[key])
                width = max(width, len(value))
            max_len[key] = real_len(width)
            #: build the header and sep in the same time
            header.append(expand(key, max_len[key]))
            sep.append('-' * (max_len[key] + TAB_WIDTH))
        for i in (header, sep):
            i.append('')
        header = '|'.join(header)
        sep = '+'.join(sep)

        #: build body
        for line in self.body:
            b = ['']
            for key, value in line.items():
                if isinstance(value, Dataset):
                    value = value.summarize()
                else:
                    value = str(value)
                width = max_len[key]
                b.append(expand(value, width))
            b.append('')
            body.append('|'.join(b))

        #: build table
        table = [sep, header, sep]
        for line in body:
            table.append(line)
            table.append(sep)
        return '\n'.join(table)
    
    def append(self, item):
        self.body.append(item)

    @property
    def count(self):
        return len(self)

    @staticmethod
    def fromheader(header):
        return Dataset(header, [])

    @staticmethod
    def fromdescs(descs, count):
        '''Build dataset from given descriptions'''
        header = [desc.name for desc in descs]
        dataset = Dataset.fromheader(header)

        for i in xrange(0, count):
            d = Data(header)
            for desc in descs:
                if desc.children:
                    #: build sub dataset
                    d[desc.name] = Dataset.fromdescs(
                                    desc.children, desc.random_generator())
                else:
                    data = desc.random_generator(desc.dataset, d)
                    if desc.unique:
                        while not dataset.is_unique(desc.name, data):
                            data = desc.random_generator(desc.dataset, d)
                    d[desc.name] = data
            dataset.append(d)

        return dataset

    def get_column(self, row_name):
        '''Get specific column'''
        return [i[row_name] for i in self]

    def is_unique(self, name, data):
        '''Check is the data in the row'''
        return not (data in self.get_column(name))

    def show(self):
        print 'count: %d\n%s' % (self.count, self.table)

    def summarize(self):
        '''Generate summary'''
        return '[%d]' % len(self)
