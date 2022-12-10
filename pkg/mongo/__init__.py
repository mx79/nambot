from typing import Mapping, Any
from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.database import Database

# Hashing method:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def compare_uri(plain_uri: str, hashed_uri: str) -> bool:
    """Verify uri between one not hashed and its hashed representation.

    :param plain_uri: URI to test, as plain string.
    :param hashed_uri: URI hashed.
    :rtype: bool
    :return: `True` if the URI matched the hash, else `False`.
    """
    return pwd_context.verify(plain_uri, hashed_uri)


class PrivateObjectError(Exception):
    """
    Specific exception class. It is raised when _Mongo object is instanced directly and not its subclasses.
    """

    def __init__(self):
        super().__init__(f"_Mongo object is not meant to be used directly, use its subclasses instead.")


class EmptyUriError(Exception):
    """
    Specific exception class. It is raised when an empty Mongo URI is given at any _Mongo subclasses init.
    """

    def __init__(self):
        super().__init__("The provided URI is None, verify if you environment variable are set and loaded.")


class InvalidUriError(Exception):
    """
    Specific exception class. It is raised when an invalid Mongo URI is given at any _MongoIMA subclasses init.
    """

    def __init__(self, uri: str):
        super().__init__(f"The following uri: {uri}, is not recognized as a CnamBot cluster URI !")


class UnknownCollectionNameError(Exception):
    """
    Specific exception class. It is raised when a wrong collection name is given to any of _MongoIMA core methods.
    """

    def __init__(self, collection, db):
        super().__init__(f"The collection: {collection}, is not present in the collection list of the database {db}.")


class _Mongo:
    """
    Private superclass of all Database object.
    It defines methods to be inherited and the behaviour that object like `AllConversation` should pursue.
    """
    uri: str
    client: MongoClient
    collections: list
    database: Database[Mapping[str, Any]]

    def __init__(self, uri: str):
        """Init function process is shared to all _Mongo subclasses.

        :param uri: The URI we want to pass to Mongo object.
        :raise: PrivateObjectError if _Mongo object is accessed directly instead of its subclasses.
        :raise: EmptyUriError if the furnished URI is None.
        :raise: InvalidUriError if the furnished URI is not equal to the cluster URI of CnamBots project.
        """
        if self.__class__.__name__ == "_Mongo":
            raise PrivateObjectError()
        if uri is None:
            raise EmptyUriError()
        if not compare_uri(uri, "$2b$12$vBH5FBHAGhlQX6BPcw8SPuyuFDoxe.Y7BMWA2uj8iVa3LPDtG6SFi"):
            raise InvalidUriError(uri)
        self.uri = uri
        self.client = MongoClient(uri)

    def __repr__(self):
        return "The `{0}` object has the following collections: {1}".format(self.__class__.__name__, self.collections)

    # ======================================== Any collection methods ======================================== #
    def insert_one(self, collection, data):
        if collection in self.collections:
            self.database[collection].insert_one(data)
        else:
            raise UnknownCollectionNameError(collection, self.database)

    def insert_many(self, collection, data):
        if collection in self.collections:
            self.database[collection].insert_many(data)
        else:
            raise UnknownCollectionNameError(collection, self.database)

    def find_one(self, collection, query):
        if collection in self.collections:
            return self.database[collection].find_one(query)
        else:
            raise UnknownCollectionNameError(collection, self.database)

    def find_many(self, collection, query):
        if collection in self.collections:
            return self.database[collection].find(query)
        else:
            raise UnknownCollectionNameError(collection, self.database)

    def update_one(self, collection, query, update):
        if collection in self.collections:
            self.database[collection].update_one(query, update)
        else:
            raise UnknownCollectionNameError(collection, self.database)

    def update_many(self, collection, query, update):
        if collection in self.collections:
            self.database[collection].update_many(query, update)
        else:
            raise UnknownCollectionNameError(collection, self.database)

    def delete_one(self, collection, query):
        if collection in self.collections:
            self.database[collection].delete_one(query)
        else:
            raise UnknownCollectionNameError(collection, self.database)

    def delete_many(self, collection, query):
        if collection in self.collections:
            self.database[collection].delete_many(query)
        else:
            raise UnknownCollectionNameError(collection, self.database)
