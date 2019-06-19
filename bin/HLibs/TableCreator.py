import DataStructureManager
import FileLoader
import TableCreaterDynamic


class TableCreator(object):
    def __init__(self, governer):
        self.no_of_table = 0
        self.fileLoader = FileLoader.FileLoader()
        self.data = None
        self.TableList = {}
        self.table_creator = TableCreaterDynamic.TableCreaterDynamic(governer)

    def data_parser(self, file_address):
        self.fileLoader.load(file_address)
        self.data = self.fileLoader.data
        Records = []
        for data in self.data:
            if data != "\n":
                if data[0] is not '%' and data[1] is not '%' and data[0] is not '%':
                    Records.append(data)
                else:
                    Records.append(data)
                    Manager = DataStructureManager.DataStructureManager()
                    self.table_parse(Manager, Records)
                    Records = []

    def printall(self):
        for table in self.TableList:
            self.TableList[table].print_block()
            print ""

    def showPerticular(self, index):
        self.TableList[index].print_block()

    def table_parse(self, manager, record):
        tablename = record[0].split("[]")[1].strip("\n")
        self.table_creator.create_table(tablename)
        self.TableList[tablename[1].strip("\n")] = manager
        i = 0
        j = 0
        flag = False
        key = ""
        for entry in record:
            temp = entry.split("[]")
            for parts in temp:
                if parts.find("&&&") is not -1:
                    flag = True
                    continue
                if flag:
                    flag = False
                    manager.insert("RecordName: " + parts.strip('\n'), 0, 0)
                    continue
                if self.check_key(parts) is True:
                    key = parts.strip("{{").strip('\n')
                    self.table_creator.insert_key(tablename, key)
                    j = 0
                    i += 1
                    manager.insert(parts.strip("{{").strip('\n'), i, j)
                    j = 1
                elif self.check_key(parts) is False:
                    self.table_creator.insert_data(parts.strip('\n'), tablename, key)
                    manager.insert(parts.strip('\n'), i, j)
                    j += 1

    def check_key(self, key):
        if key.find("{{") is not -1:
            return True
        elif key.find("%%%") is not -1:
            return -10
        else:
            return False
