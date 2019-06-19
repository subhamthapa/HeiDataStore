import TableCreaterDynamic
import TableCreator


class DatabaseLoader:
    def __init__(self, governer):
        self.TableCreator = {}
        self.database_name = ""
        self.data_reader = TableCreator.TableCreator(governer)
        self.databases = {}

    def read_metadata(self):
        self.data_reader.data_parser("..\\..\\datastore\\metadata")
        return self.data_reader.table_creator.get_row("meta_data", "DataBase:")

    def read_metadata_database(self, database_name):
        self.data_reader.data_parser("..\\..\\datastore\\" + database_name + "\\meta_data_" + database_name)
        return self.data_reader.table_creator.get_row("meta_data_"+database_name, "Files:")

    def load_database(self, database_name):
        self.database_name = database_name
        listoffiles = self.read_metadata_database(database_name)
        length = len(listoffiles)
        if listoffiles[length - 1] is "":
            del listoffiles[length - 1]
        for files in listoffiles:
            if files is not "":
                self.data_reader.data_parser("..\\..\\datastore\\" + database_name + "\\" + files)
        return self.data_reader.table_creator

    def insert_metadata(self, file_name):
        self.data_reader.table_creator.insert_data(file_name, "meta_data_" + self.database_name
                                                   , "Files:")

    def write_metadata_database(self, table_name):
        self.data_reader.table_creator.commit("meta_data_" + self.database_name)

    def __getitem__(self, item):
        return self.TableCreator[item]
