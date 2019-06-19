import HLinked


class DataStructureManager(object):
    def __init__(self):
        self.repository = HLinked.HLinked()
        self.NodeIndex = 0
        self.metadata = {}
        self.row_meta_data = []
        self.column_meta_data = []

    def insert(self, data, row, column):
        self.metadata.update({str(row) + " " + str(column): self.NodeIndex})
        self.repository.add_node_indexed(data, self.NodeIndex)
        self.NodeIndex += 1

    def getdata(self, row, column):
        index = self.metadata[str(row) + " " + str(column)]
        return self.repository.get_node(index)

    def print_block(self):
        keys = self.metadata.keys()
        listofkeys = []
        for key in keys:
            listofkeys.append(key.split())
        length = len(listofkeys)
        i = 0
        sorted_key_list = sorted(listofkeys)
        prev = sorted_key_list[0][0]
        curr = prev
        return_data = []
        while i < length:
            curr = sorted_key_list[i][0]
            data = str(self.getdata(sorted_key_list[i][0], sorted_key_list[i][1]))
            if curr is prev:
                space = self.create_space(data)
                print data + space,
                return_data.append(data + space)
            else:
                return_data.append("\n")
                print ""
                print data + self.create_space(data),
                return_data.append(data + self.create_space(data))
                prev = curr

            i += 1
        return return_data

    def create_space(self, data):
        length = len(data)
        str = ""
        while length < 12:
            str += " "
            length += 1
        return str

    def remove(self, row, column):
        index = self.metadata[str(row) + " " + str(column)]
        listofkeys = []
        keys = self.metadata.keys()
        for key in keys:
            listofkeys.append(key.split())
        sorted_key_list = sorted(listofkeys)
        max = column
        for key in sorted_key_list:
            if key[0] is str(row):
                if max < int(key[1]):
                    max = int(key[1])

        self.repository.del_node(index)
        self.NodeIndex -= 1
        del self.metadata[str(row) + " " + str(max)]


