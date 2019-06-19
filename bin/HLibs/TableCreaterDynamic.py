import DataStructureManager
import FileWriter

"""This code generates table dynamically when the framework is still executing. If the user executes 'commit' command then the
table data in the memory is written to a file"""


class TableCreaterDynamic(object):
    def __init__(self, governor):
        self.governor = governor
        self.table = {}
        self.table_metadata = {}
        self.key_index = {}
        self.data_index = {}
        self.index = {}
        self.file_writer = FileWriter.FileWriter()

    def __getitem__(self, item):
        return self.table[item]

    def create_table(self, table_name):
        table = DataStructureManager.DataStructureManager()
        table.insert("RecordName: " + table_name, 0, 0)
        self.table[table_name] = table
        self.key_index[table_name] = {}
        self.table_metadata[table_name] = []
        self.data_index[table_name] = {}
        self.index[table_name] = 0

    def insert_key(self, table_name, key):
        table = self.table[table_name]
        self.table_metadata[table_name].append(key)
        self.index[table_name] += 1
        self.key_index[table_name][key] = self.index[table_name]
        table.insert(key, self.index[table_name], 0)
        self.data_index[table_name][key] = 1

    def insert_data(self, data, table_name, key):
        if self.search(self.table_metadata[table_name], key):
            table = self.table[table_name]
            try:
                table.insert(data, self.key_index[table_name][key], self.data_index[table_name][key])
            except KeyError:
                print "Error"
            finally:
                self.data_index[table_name][key] += 1

    def delete_key(self, table_name, key):
        index = self.key_index[table_name]
        data_index = self.data_index[table_name]
        i = 0
        while i < data_index[key]:
            self.table[table_name].remove(index[key], i)
            i += 1

    def delete_entry_metadata(self, data, table_name, key):
        index = self.key_index[table_name]
        i = 1
        while i < self.data_index[table_name][key]:
            if self.table[table_name].getdata(index[key], i) is data:
                self.table[table_name].remove(index[key], i)
                self.data_index[table_name][key] -= 1
                break
            i += 1

    def get_row(self, table_name, key):
        index = self.key_index[table_name][key]
        column = self.data_index[table_name][key]
        i = 1
        data = []
        while i < column:
            temp = self.table[table_name].getdata(index, i)
            if temp != "" or temp != " ":
                data.append(temp)
            i += 1
        return data

    def search(self, list_name, item):
        for name in list_name:
            if name == item:
                return True
        return False

    def commit(self, table_name):
        self.file_writer.write(self.governor.DataStore_name,
                               self.table[table_name], self.key_index[table_name], self.data_index[table_name])
    def write_metadata(self, database_name, flag=False):
        file = None
        try:
            if not flag:
                file = open("..\\..\\datastore\\metadata", "r+")
            else:
                file = open("..\\..\\datastore\\" + database_name + "\\meta_data_" + database_name, "r+")
        except IOError:
            if not flag:
                file = open("..\\..\\datastore\\metadata", "w+")
            else:
                file = open("..\\..\\datastore\\" + database_name + "\\meta_data_" + database_name, "w+")
        finally:
            if not flag:
                self.file_writer.write("meta_data", self.table["meta_data"],
                                       self.key_index["meta_data"], self.data_index["meta_data"], file, True)
            else:
                self.file_writer.write("meta_data_" + database_name, self.table["meta_data_" + database_name],
                                       self.key_index["meta_data_" + database_name], self.data_index["meta_data_"+database_name], file, True)


    def print_all(self, table_name):
        return self.table[table_name].print_block()



