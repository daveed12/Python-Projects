#David De La Cruz
import pickle
class Table:
    def __init__(self,name="",fields=tuple(), tups=None):
        self.__name = name
        self.__fields = fields
        self.__tups = tups

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def fields(self):
        return self.__fields

    @property
    def tups(self):
        return self.__tups

    # Relational operations:
    def select(self,field,val):
        return Table("result", self.__fields, [row for row in self.__tups if row[self.__fields.index(field)] == val])

    def project(self, *fields):
        indexes = [self.__fields.index(field) for field in fields]
        return Table("result", fields, set([tuple([row[i] for i in indexes]) for row in self.__tups]))

    @staticmethod
    def join(tab1, tab2):
        intersection = list(set.intersection(set(tab1.fields),set(tab2.fields)))[0]
        tmp1 = list(tab1.fields)
        tmp2 = list(tab2.fields)
        tmp2.remove(intersection)
        columns = tmp1 + tmp2
        joined = list()
        for rows in tab1.tups:
            for rows2 in tab2.tups:
                for entry in rows2:
                    if rows[0] == entry:
                        rows2 = list(rows2)
                        rows2.remove(rows[0])
                        joined.append(list(rows) + rows2)

        return Table("result",columns, set([tuple(lists) for lists in joined]))

    def insert(self, *tup):
        if (len(self.__fields) == len(tup)):
            self.__tups = list(self.__tups)
            self.__tups.append(tup)
            self.__tups = set(self.__tups)

    def remove(self, field, val):
        self.__tups = list(self.__tups)
        for row in self.__tups:
            if row[self.__fields.index(field)] == val:
                self.__tups.remove(row)

    def __str__(self):
        output = self.__name + str(self.__fields) + "\n" + ('=' * len(self.__name) + "\n")
        for tuples in self.__tups:
            output = output + str(tuples) + "\n"
        return output

    # Serialization and text backup
    def store(self):
        fileobject = open(self.__name + ".db", 'wb')
        pickle.dump(self, fileobject)
        fileobject.close()

    @staticmethod
    def restore(fname):
        fileobject = open(fname,'rb')
        return pickle.load(fileobject)

    @staticmethod
    def read(fname):
        file = open(fname,'r')
        lines = file.read().splitlines()
        return Table(lines[0], tuple(lines[1].split(',')), set([tuple(lists.split(',')) for lists in lines[2:len(lines)]]))

    def write(self, fname):
        file = open(fname, 'w')
        file.write(str(self))
        file.close()

