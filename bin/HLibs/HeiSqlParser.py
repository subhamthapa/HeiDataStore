import Governer


class HeiSqlParser:
    def __init__(self):
        self.governer = Governer.Governor()
        self.tables = []

    def hsql(self, query):
        HSQL = self.query_parser(query)
        try:
            if HSQL[0] == "create":
                if HSQL[1] == "database":
                    return self.governer.create_database(HSQL[2])
                elif HSQL[1] == "table":
                    self.tables = self.governer.loaded_database.get_row("meta_data_" + self.governer.DataStore_name,
                                                                        "Files:")
                    if not self.governer.dyanmictablecreator.search(self.tables, HSQL[2]):
                        self.governer.create_table(HSQL[2])
                    else:
                        return "TABLE ALREADY EXIST"
                    if len(HSQL) is not 3:
                        key = self.get_Keys(query.split("key")[1])
                        print "Yeah", key
                        for k in key:
                            self.governer.insert_key(HSQL[2], k)
                        return "Table created."
                    else:
                        return "Table created"
                else:
                    return "SQL ERROR"
            elif HSQL[0] == "load":
                return self.governer.select_database(HSQL[1])
            elif HSQL[0] == "put":
                semi = query.strip(" ").split(",")
                table_name = semi[0].split()[1].split("(")[0]
                keys = self.get_Keys(query)
                if query.find("val(") is not -1:
                    values = self.get_Keys(query.split("val")[1])
                    i = 0
                    for key in keys:
                        self.governer.insert_data(values[i], table_name, key)
                        i += 1
                    return "Value inserted"
                else:
                    for key in keys:
                        self.governer.insert_key(table_name, key)
                    return "Key inserted"
            elif HSQL[0] == "commit":
                return self.governer.commit(HSQL[1])
            elif HSQL[0] == "from":
                table_name = HSQL[1]
                if HSQL[2] == "show":
                    if HSQL[3] == "all":
                        return self.governer.display_all(table_name)
                    elif HSQL[3].find("avg(") is not -1:
                        temp = query.split("avg(")
                        print temp[1]
                        key = self.get_Keys("(" + temp[1])
                        avg = ""
                        sum = 0
                        no = 0
                        print key
                        for k in key:
                            number = self.governer.loaded_database.get_row(table_name, k)
                            flag = False
                            c = 0
                            for n in number:
                                if n == "":
                                    c += 1
                            if c == len(number):
                                avg += str(k) + " Row Empty" + "\n"
                                continue

                            for n in number:
                                if n.isdigit():
                                    sum += int(n)
                                    no += 1
                            if no != 0:
                                temp = sum * 1.0 / no
                            avg += "avg(" + str(k) + "): " + str(temp) + "\n"
                            sum = 0
                            no = 0
                        return avg
                    elif HSQL[3].find("count(") is not -1:
                        temp = query.split("count(")
                        print temp[1]
                        key = self.get_Keys("(" + temp[1])
                        count = ""
                        count_key = 0
                        for k in key:
                            number = self.governer.loaded_database.get_row(table_name, k)
                            flag = False
                            c = 0
                            for n in number:
                                if n == "":
                                    c += 1
                            if c == len(number):
                                count += str(k) + " 0" + "\n"
                                continue

                            for n in number:
                                if n.isdigit():
                                    count_key += 1
                            count += "avg(" + str(k) + "): " + str(count_key) + "\n"
                            count_key = 0
                        return count
                    i = 3
                    string = ""
                    while i < len(HSQL):
                        print HSQL[i].strip(",") + ":",
                        string += HSQL[i].strip(",") + ": "
                        for item in self.governer.get_row(table_name, HSQL[i].strip(",")):
                            print "ITEM" + item.strip(" "),
                            string += item + " "
                        print ""
                        string += "\n"
                        i += 1
                    return string
            elif HSQL[0] == "list":
                if HSQL[1] == "database":
                    ls = self.governer.data_bases
                    print ls
                    item = "DataBases: "
                    for l in ls:
                        if l != "":
                            item += "| " + l + " | "
                    return item
                elif HSQL[1] == "table":
                    ls = self.governer.loaded_database.get_row("meta_data_" + self.governer.DataStore_name, "Files:")
                    item = "Tables: "
                    for l in ls:
                        if l != "":
                            item += "| " + l + " | "
                    return item
            elif HSQL[0] == "del":
                if len(HSQL) is 1:
                    return "Bad Command:"
                i = 1
                while i < len(HSQL):
                    self.governer.delete_database(HSQL[i])
                    i += 1
            elif HSQL[0] == "current":
                if HSQL[1] == "database":
                    return self.governer.DataStore_name

            else:
                return "SQL not understandable."
        except Exception, e:
            print e
            return "DATABASE error/Wrong SQL/ Try loading a database"

    def substr(self, str, index):
        temp = ""
        for i in range(0, index):
            temp += str[i]
        return temp

    def get_Keys(self, querry):
        keys = []
        print querry
        flag = False
        str = ""
        for c in querry:
            if c == ",":
                keys.append(str)
                str = ""
                continue

            if c == "(":
                flag = True
                continue
            if c == "" or c == " ":
                continue
            if c == ")":
                flag = False
                keys.append(str)
                break
            if flag:
                str += c
                continue
        return keys

    def get_values(self, str):
        values = []
        print str

    def next_parser(self, query, delimiter):
        return query.split(delimiter)

    def query_parser(self, query):
        return query.strip("\n").split()



