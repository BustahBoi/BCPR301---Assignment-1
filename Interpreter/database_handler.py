from database_local import DBLocal
from database_remote import DBRemote
from pickler import Pickler
from unpickler import Unpickler

# Wesley
class DatabaseHandler:
    def __init__(self):
        self.local = DBLocal()
        self.remote = DBRemote()
        self.local_connection = None
        self.remote_connection = None

    # A really, really, really bad decorator that can get fixed //Wesley
    def local_decorator(f):
        def wrapper(*args):
            db = args[0].local_connection
            args[0].local.connect(db)
            # if args[0].local_connection == ":memory:":
            args[0].local.create_table()
            r = f(*args)
            args[0].local.commit()
            args[0].local.close()
            return r
        return wrapper

    # Part 2 of really, really, badness //Wesley
    def remote_decorator(f):
        def wrapper(*args):
            db = args[0].remote_connection
            args[0].remote.connect(db["host"], db["user"], db["password"], db["db"])
            args[0].remote.create_table()
            r = f(*args)
            args[0].remote.commit()
            args[0].remote.close()
            return r
        return wrapper

    # Wesley
    def set_local(self, connection):
        self.local_connection = connection

    # Wesley
    def set_remote(self, host, user, password, db):
        self.remote_connection = {"host": host, "user": user, "password": password, "db": db}

    # Wesley
    @local_decorator
    def insert_local_dict(self, dictionary):
        """Insert values into both the local and remote"""
        pickled = Pickler.pickle_dictionary_values(dictionary)
        self.local.insert_dictionary(pickled)
        return "Data inserted into local database"
        # print(self.local.get_db())

    # Wesley
    @remote_decorator
    def insert_remote_dict(self, dictionary):
        """Insert values into both the local and remote"""
        pickled = Pickler.pickle_dictionary_values(dictionary)
        self.remote.insert_dictionary(pickled)
        return "Data inserted into local database"
        # print(self.remote.get_db())

    # Wesley
    @local_decorator
    def get_local(self):
        unpickle = Unpickler.unpickle_dictionary(self.local.get_db())
        return unpickle

    # Wesley
    @remote_decorator
    def get_remote(self):
        unpickle = Unpickler.unpickle_dictionary(self.remote.get_db())
        return unpickle

    # # Will do later
    # def db_sync_remote(self):
    #     """Will need to test remote first"""
    #     remote = self.get_remote()
    #     local = self.get_local()
    #     checked = dict()
    #     for record in remote.items():
    #         for employee in record[1]:
    #             for record_local in local.items():
    #                 for emp in record_local[1]:
    #                     if employee != emp:
    #                         checked[record[0]] = emp
    #     self.insert_remote_dict(checked)
    #
    # def db_sync_local(self):
    #     """Will need to test remote first"""
    #     remote = self.get_remote()
    #     local = self.get_local()
    #     checked = dict()
    #     for record in local.items():
    #         for employee in record[1]:
    #             for record_local in remote.items():
    #                 for emp in record_local[1]:
    #                     if employee != emp:
    #                         checked[record[0]] = emp
    #     self.insert_remote_dict(checked)
    # def local_method(self, function):
    #     """
    #
    #     :param function:
    #     :return:
    #     """
    #     self.local.connect()


# Tested, works
# a = DatabaseHandler()
# a.set_local(":memory:")
# a.set_remote("localhost", "root", "", "test")
# data = {0: {"1ID": "A23", "Gender": "Male", "Age": 22, "Sales": 2445, "BMI": "normal", "salary": 20,
#             "Birthday": "24/06/1995"},
#         1: {"IhD": "A2f3", "Gender": "Male", "Age": 23, "Sales": 2565, "BMI": "normal", "salary": 20,
#             "Birthday": "24/06/1995"},
#         2: {"IjD": "Aa23", "Gender": "Female", "Age": 25, "Sales": 25, "BMI": "normal", "salary": 20,
#             "Birthday": "24/06/1995"},
#         3: {"IgD": "A23", "Gender": "Female", "Age": 26, "Sales": 225, "BMI": "normal", "salary": 20,
#             "Birthday": "24/06/1995"}}
# a.insert_remote_dict(data)
# a.insert_local_dict(data)
# a.get_remote()
# a.get_local()

