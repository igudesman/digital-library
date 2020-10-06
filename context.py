from pymongo import MongoClient
import typing


class UserDBModel:

    def __init__(self):
        self.__id: typing.Optional[str] = None
        self.__user_name: typing.Optional[str] = None
        self.__password_hash: typing.Optional[str] = None
        self.__email: typing.Optional[str] = None
        self.__role: typing.Optional[str] = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, value: str):
        self.__user_name = value

    @property
    def password_hash(self):
        return self.__password_hash

    @password_hash.setter
    def password_hash(self, value: str):
        self.__password_hash = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value: str):
        self.__email = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value: str):
        self.__role = value

    def to_dict(self) -> typing.Dict:
        meta = dict()
        meta["user_name"] = self.__user_name
        meta["password_hash"] = self.__password_hash
        meta["email"] = self.__email
        meta["role"] = self.__role

        return meta

    def from_dict(self, obj_dict: typing.Dict):
        self.__user_name = obj_dict["user_name"]
        self.__password_hash = obj_dict["password_hash"]
        self.__email = obj_dict["email"]
        self.__role = obj_dict["role"]
        self.__id = str(obj_dict["_id"])

class MainContext:

    def __init__(self):
        self.__client = MongoClient('localhost', 27017)
        self.__db = self.__client.get_database("digitallib")

    @property
    def database(self):
        return self.__db

class UserContext:

    def __init__(self, main_context: MainContext):
        self.__context = main_context
        self.__users_collection = self.__context.database.get_collection("users")

    def find_user(self, user_name: str) -> typing.Optional[UserDBModel]:
        found_users = self.__users_collection.find({"user_name": user_name})
        if found_users.count() == 0:
            return None
        user = found_users[0]
        user_model = UserDBModel()
        user_model.from_dict(user)
        return user_model

    def change_password(self, user_name: str, password_hash_new: str):
        self.__users_collection.update_one({"user_name": user_name}, {"password_hash": password_hash_new})

    def delete_user(self, user_name: str):
        self.__users_collection.delete_one({"user_name": user_name})

class FileContext:

    def __init__(self, main_context: MainContext):
        self.__context = main_context
        self.__files_collection = self.__context.database.get_collection("files")

