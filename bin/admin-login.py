import os
import socket
import sys


class FileReader:
    def __init__(self):
        self.filename = None

    def commit(self):
        self.filename.close()

    def changeFile(self, admin):
        if admin:
            try:
                self.filename = file("..\\conf\\admin.dat", "rb+")
            except Exception:
                self.filename = file("..\\conf\\admin.dat", "wb+")
        else:
            try:
                self.filename = file("..\\conf\\client.dat", "rb+")
            except Exception:
                self.filename = file(".\\conf\\client.dat", "wb+")

    def read(self):
        return self.filename.read()

    def tell(self):
        return self

    def writeFile(self, path, data):
        try:
            self.filename = file(path, "ab+")
        except Exception:
            self.filename = file(path, "wb+")
        finally:
            self.filename.write(data)

    def next(self):
        return self.filename.next()

    def tell(self):
        return self.filename.tell()

    def getPassword(self, admin, username="admin", path="..\\conf\\admin.dat"):
        if admin:
            self.changeFile(True)
        else:
            self.changeFile(False)
        data = self.filename.readlines()
        password = None
        if admin:
            return data[2].decode('base64', 'strict').split(" ")[1]
        else:
            i = 0
            string = ""
            for d in data:
                string += d.decode('base64', 'strict')
            parsed = string.split(" ")
            while i < len(parsed):
                if parsed[i].strip(" ").strip("\n") == username:
                    password = parsed[i + 2]
                    break
                i += 1
            return password


class Client:
    def __init__(self):
        self.filereader = FileReader()

    def getPassword(self, username, path="..\\conf\\client.dat"):
        password = self.filereader.getPassword(False, username, path)
        if password is None or password == '':
            return False
        else:
            return password


class Admin:
    def __init__(self):
        self.filereader = FileReader()
        self.password = self.filereader.getPassword(True)
        self.client = Client()
        self.loggedin_admin = False
        self.loggedin_client = True
        self.username = ""

    def add_client(self, ip, username, password):
        data = "client: " + ip + " permission: r " + "username: " + username + " password: " + password
        self.filereader.writeFile("..\\conf\\client.dat", data.encode('base64', 'strict'))

    def chmod(self, client_name, permission):
        f = open("..\\conf\\client.dat", "rb+")
        if permission.strip() != "r":
            if permission.strip() !="w":
                print "\nWrong permission flag"
                print "--Type help for instructions--\n"
                return
        data = f.readlines()
        string = ""
        for d in data:
            string +=d.decode('base64', 'strict')
        split = string.split()
        i = 0
        while i < len(split):
            if split[i] == client_name:
                split[i - 2] = permission
            i += 1
        f.close()
        f = open("..\\conf\\client.dat", "wb+")
        str = ""
        for d in split:
            str += d.encode('base64', 'strict')
        f.write(str)
        f.close()



    def rm(self, client_name):
        f = file("..\\conf\\client.dat", "rb+")
        data = f.readlines()
        string = ""
        listofdata = []
        i = 0
        while i < len(data):
            string = data[i].decode('base64', 'strict')
            if string.find(client_name) is not -1:
                del data[i]
                del data[i]
                break
            i += 1

        f.close()
        f = open("..\\conf\\client.dat", "wb")
        f.writelines(data)
        f.close()

    def show_client(self):
        f = open("..\\conf\\client.dat", "rb")
        data = f.readlines()
        password = raw_input("Enter password:>")
        print ""
        if password == self.password:
            os.system("color 2")
            for d in data:
                print d.decode('base64', 'strict'),
            print "\n"
        else:
            print "wrong password"
            print ""
            return
        raw_input("Press any key to clear the console:>")
        os.system("cls")
        os.system("color 7")
        print "\n" + self.username + " logged in", "--Authority-- " + "admin"
        print ""

    def login(self, username, password):
        if username == "admin" or username == "Admin":
            if self.password == password:
                self.loggedin_client = False
                self.loggedin_admin = True
                return True
        else:
            password_client = self.client.getPassword(username, "..\\conf\\client.dat")
            if password_client == password:
                self.loggedin_client = True
                self.loggedin_admin = False
                return True
            else:
                return False

    def listner(self):
        self.first()
        while True:
            if self.loggedin_admin:
                code = raw_input("admin:> ")
                if code.strip(" ") == "help":
                    self.help()
                elif code.strip().find("add client") is not -1:
                    splitted = code.split()
                    self.add_client(splitted[2].strip(), splitted[3].strip(), splitted[4].strip())
                elif code.find("delegate") is not -1:
                    pass
                elif code.find("rm") is not -1:
                    self.rm(code.split()[1].strip(" "))

                elif code.strip() == "clear":
                    os.system("cls")
                elif code.strip() == "commit":
                    self.filereader.commit()
                    break
                elif code.strip() == "exit":
                    break
                elif code.strip() == "show client":
                    self.show_client()
                elif code.find("chmod") != -1:
                    splitted = code.split()
                    self.chmod(splitted[1], splitted[2])
                else:
                    print ""
                    print "--Type help for instruction--"
                    print ""
        if code.strip() != "exit":
            os.system("cls")
            self.listner()

    def first(self):
        while True:
            username = raw_input("username:> ")
            password = raw_input("password:> ")
            if self.login(username, password):
                if self.loggedin_admin:
                    self.username = username
                    os.system("cls")
                    print "\n" + username + " logged in", "--Authority-- " + "admin"
                    print ""
                    break
                else:
                    os.system("cls")
                    self.username = username
                    print ""
                    print username + " logged in", "--Authority-- " + "client"
                    print ""
                    break
            else:
                # os.system("cls")
                print ""
                print "Username or Password incorrect"

    def help(self):
        print ""
        print "Type add client --ip-- --username-- --password-- to add client"
        print "Type chmod --client-- r/w to give permissions to a client"
        print "Type delegate --ip-- to give administrator permission to a client"
        print "Type rm --ip-- to remove a client"
        print "Type alter -c -n --clientname-- to change the client username"
        print "Type alter -c -p --clientname-- to change the client password"
        print "Type alter -p --password-- to change the admin password"
        print "Type commit to finalize the change"
        print "Type show client to view the clients"
        print "Type exit to close the console"
        print ""


a = Admin()
a.listner()
