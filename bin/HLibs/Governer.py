import TableCreator
import TableCreaterDynamic
import DataBaseLoader
import os


class Governor(object):
    def __init__(self):
        self.selected_data_bank = None
        self.DataStore_name = None
        self.loaded_database = None
        self.loaded_Table = []
        self.tablecreator = TableCreator.TableCreator(self)
        self.dyanmictablecreator = TableCreaterDynamic.TableCreaterDynamic(self)
        self.dyanmictablecreator.create_table("meta_data")
        self.database_loader = DataBaseLoader.DatabaseLoader(self)
        self.data_bases = self.database_loader.read_metadata()
        self.dyanmictablecreator.insert_key("meta_data", "DataBase:")
        for db in self.data_bases:
            if db != "":
                self.dyanmictablecreator.insert_data(db, "meta_data", "DataBase:")
        self.selected_database = None

    def initialize(self, database_name):
        self.tablecreator.data_parser("..\\..\\" + database_name)

    def create_database(self, database_name):
        try:
            flag = self.dyanmictablecreator.search(self.data_bases, database_name)
            if not flag:
                os.makedirs("..\\..\\datastore\\" + database_name)
            else:
                print "DataBase already exist"
        except WindowsError:
            print "DataBase already exist"
        except IOError:
            print "DataBase already exist"
        finally:
            if not flag:
                self.dyanmictablecreator.search(self.data_bases, database_name)
                self.dyanmictablecreator.create_table("meta_data_" + database_name)
                self.dyanmictablecreator.insert_key("meta_data_" + database_name, "Files:")
                self.dyanmictablecreator.write_metadata(database_name, True)
                self.data_bases.append(database_name)
                self.dyanmictablecreator.insert_data(database_name, "meta_data", "DataBase:")
                self.dyanmictablecreator.write_metadata(self.dyanmictablecreator.table["meta_data"])
                return "DATABASE CREATED"

    def delete_database(self, database_name):
        self.dyanmictablecreator.delete_entry_metadata(database_name, "meta_data", "DataBase:")
        self.dyanmictablecreator.write_metadata(self.dyanmictablecreator.table["meta_data"])
        #self.dyanmictablecreator.file_writer.delete_folder()

    def select_database(self, database_name):
        if self.dyanmictablecreator.search(self.data_bases, database_name):
            self.DataStore_name = database_name
            self.loaded_database = self.database_loader.load_database(database_name)
            self.loaded_Table = self.database_loader.read_metadata_database(database_name)
            return "Database loaded"
        else:
            print "NO SUCH DATABASE"

    def create_table(self, table_name):
        if self.loaded_database is None:
            return "DATABASE IS NOT LOADED"
        else:
            print self.dyanmictablecreator.search(self.loaded_Table, table_name)
            if not self.dyanmictablecreator.search(self.loaded_Table, table_name):
                self.database_loader.insert_metadata(table_name)
                self.database_loader.write_metadata_database("meta_data_"+table_name)
                self.loaded_database.create_table(table_name)
                self.loaded_database.commit(table_name)

    def display_all(self, table_name):
        if self.loaded_database is None:
            return "DATABASE IS NOT LOADED"
        else:
            data = self.loaded_database.print_all(table_name)
            str = ""
            for d in data:
                str += d
            return str

    def insert_key(self, table_name, key):
        if self.loaded_database is None:
            return "DATABASE IS NOT LOADED"
        else:
            if not self.loaded_database.key_index[table_name].has_key(key):
                self.loaded_database.insert_key(table_name, key)
                return "KEY INSERTED"

    def insert_data(self, data, table_name, key):
        if self.loaded_database is None:
            return "DATABASE IS NOT LOADED"
        else:
            self.loaded_database.insert_data(data, table_name, key)
            return "DATA IS INSERTED"

    def delete_key(self, table_name, key):
        if self.loaded_database is None:
            return False
        else:
            self.loaded_database.delete_key(table_name, key)

    def get_row(self, table_name, key):
        if self.loaded_database is None:
            return False
        else:
            return self.loaded_database.get_row(table_name, key)

    def commit(self, table_name):
        if self.loaded_database is None:
            return False
        else:
            self.loaded_database.commit(table_name)
            return "Table written"

