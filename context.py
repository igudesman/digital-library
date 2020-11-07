from datetime import datetime

from bson import ObjectId
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


class FileDBModel:
    def __init__(self):
        self.__id: str = ""
        self.__name: str = ""
        self.__type: str = ""
        self.__path: str = ""
        self.__size: int = 0

    def from_dict(self, data: dict):
        self.__id = str(data["_id"])
        self.__name = data["name"]
        self.__path = data["path"]
        self.__type = data["type"]
        self.__size = data["size"]

    def to_response_dict(self) -> dict:
        data = dict()
        data["_id"] = self.__id
        data["name"] = self.__name
        data["type"] = self.__type
        data["size"] = self.__size
        return data

    def to_db_dict(self) -> dict:
        data = self.to_response_dict()
        data["path"] = self.__path
        return data

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value: int):
        self.__size = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value


class PostDBModel:

    def __init__(self):
        self.__id: str = ""
        self.__title: str = ""
        self.__description: str = ""
        self.__category: str = ""
        self.__tags: typing.List[str] = list()
        self.__attachments: typing.List[str] = list()
        self.__date: datetime = datetime.min
        self.__publisher: str = ""

    def from_dict(self, data: dict):
        self.__id = str(data["_id"])
        self.__title = data["title"]
        self.__description = data["description"]
        self.__category = data["category"]
        self.__tags = data["tags"]
        self.__attachments = data["attachments"]
        self.__date = data["date"]
        self.__publisher = data["publisher"]

    def to_dict(self) -> dict:
        data = dict()
        data["_id"] = self.__id
        data["title"] = self.__title
        data["description"] = self.__description
        data["category"] = self.__category
        data["date"] = self.__date
        data["publisher"] = self.__publisher
        data["tags"] = self.__tags
        data["attachments"] = self.__attachments
        return data

    @property
    def publisher(self):
        return self.__publisher

    @publisher.setter
    def publisher(self, value: str):
        self.__publisher = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value: datetime):
        self.__date = value

    @property
    def attachments(self):
        return self.__attachments

    @attachments.setter
    def attachments(self, value: typing.List[str]):
        self.__attachments = value

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, value: typing.List[str]):
        self.__tags = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value: str):
        self.__category = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value


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
        self.__users_collection.update_one({"user_name": user_name}, {"$set":{"password_hash": password_hash_new}})

    def delete_user(self, user_name: str):
        self.__users_collection.delete_one({"user_name": user_name})


class FileContext:

    def __init__(self, main_context: MainContext):
        self.__context = main_context
        self.__files_collection = self.__context.database.get_collection("files")

    def add_file(self, file_model: FileDBModel):
        data = file_model.to_db_dict()
        file_id = self.__files_collection.insert_one(data)
        return str(file_id.inserted_id)

    def find_file(self, file_id: str):
        found = self.__files_collection.find({"_id": ObjectId(file_id)})
        if found.count() != 1:
            return None
        file_data = found[0]
        file_model = FileDBModel()
        file_model.from_dict(file_data)
        return file_model


class ListContext:
    def __init__(self, context: MainContext):
        self.__context = context
        self.__wait_list_collection = self.__context.database.get_collection("wait_list")
        self.__main_list_collection = self.__context.database.get_collection("main_list")
        self.__search_str = ""
        self.__category = ""
        self.__tags = None

    def accept_post(self, post_id: str):
        post = self.find_post(post_id, "wait")
        self.delete_post(post_id, "wait")
        self.add_post(post, "main")

    def find_post(self, post_id: str, collection: str = "main"):
        if collection == "main":
            found_posts = self.__main_list_collection.find({"_id": ObjectId(post_id)})
        else:
            found_posts = self.__wait_list_collection.find({"_id": ObjectId(post_id)})
        if found_posts.count() == 0:
            return None
        post = PostDBModel()
        post.from_dict(found_posts[0])
        return post

    def delete_post(self, post_id: str, collection: str = "main"):
        if collection == "main":
            self.__main_list_collection.delete_one({"_id": ObjectId(post_id)})
        else:
            self.__wait_list_collection.delete_one({"_id": ObjectId(post_id)})

    def add_post(self, post_data: PostDBModel, collection: str = "wait"):
        if collection == "main":
            self.__main_list_collection.insert_one(post_data.to_dict())
        else:
            self.__wait_list_collection.insert_one(post_data.to_dict())

    def __filter(self, elem: dict) -> bool:
        title: str = elem["title"].lower()
        category: str = elem["category"].lower()
        tags: typing.List[str] = elem["tags"]
        if self.__search_str != "" and title.find(self.__search_str) == -1:
            return False
        if self.__category is not None and category != self.__category:
            return False
        if self.__tags is not None:
            for tag in self.__tags:
                if tag not in tags:
                    return False

        return True

    def search(self, collection: str = "main", search_string: str = "", category: typing.Optional[str] = None,
               tags: typing.List[str] = None, offset: int = 0, limit: int = 20):
        self.__search_str = search_string
        self.__category = category
        self.__tags = tags
        if collection == "wait":
            found = list(self.__wait_list_collection.find()[offset:offset + limit])
        else:
            found = list(self.__main_list_collection.find()[offset:offset + limit])
        filtered = filter(self.__filter, found)
        for post in filtered:
            model = PostDBModel()
            model.from_dict(post)
            yield model
