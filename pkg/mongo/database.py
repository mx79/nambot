from pkg.mongo import _Mongo


class CnamBot(_Mongo):
    """
    Class that permits to enable connection to MongoDB instance of database named `cnambot`.
    """

    def __init__(self, uri: str):
        """Init connection to IMA cluster with the personalized init method inherited from _MongoIMA superclass.

        :param uri: The URI we want to pass to _Mongo object.
        :raise: PrivateObjectError if _Mongo object is accessed directly instead of its subclasses.
        :raise: EmptyUriError if the furnished URI is None.
        :raise: InvalidUriError if the furnished URI is not equal to the cluster URI of CnamBots project.
        """
        super().__init__(uri)
        self.database = self.client["cnambot"]
        self.collections = []

    # ======================================== immat methods ======================================== #
    def insert_one_immat(self, data):
        self.database["CAS_ASK_IMMAT"].insert_one(data)

    def insert_many_immat(self, data):
        self.database["CAS_ASK_IMMAT"].insert_many(data)

    def find_one_immat(self, query):
        return self.database["CAS_ASK_IMMAT"].find_one(query)

    def find_many_immat(self, query):
        return self.database["CAS_ASK_IMMAT"].find(query)

    def update_one_immat(self, query, update):
        self.database["CAS_ASK_IMMAT"].update_one(query, update)

    def update_many_immat(self, query, update):
        self.database["CAS_ASK_IMMAT"].update_many(query, update)

    def delete_one_immat(self, query):
        self.database["CAS_ASK_IMMAT"].delete_one(query)

    def delete_many_immat(self, query):
        self.database["CAS_ASK_IMMAT"].delete_many(query)

    # ======================================== marque_modele methods ======================================== #
    def insert_one_marque_modele(self, data):
        self.database["CAS_ASK_MARQUE_MODELE"].insert_one(data)

    def insert_many_marque_modele(self, data):
        self.database["CAS_ASK_MARQUE_MODELE"].insert_many(data)

    def find_one_marque_modele(self, query):
        return self.database["CAS_ASK_MARQUE_MODELE"].find_one(query)

    def find_many_marque_modele(self, query):
        return self.database["CAS_ASK_MARQUE_MODELE"].find(query)

    def update_one_marque_modele(self, query, update):
        self.database["CAS_ASK_MARQUE_MODELE"].update_one(query, update)

    def update_many_marque_modele(self, query, update):
        self.database["CAS_ASK_MARQUE_MODELE"].update_many(query, update)

    def delete_one_marque_modele(self, query):
        self.database["CAS_ASK_MARQUE_MODELE"].delete_one(query)

    def delete_many_marque_modele(self, query):
        self.database["CAS_ASK_MARQUE_MODELE"].delete_many(query)

    # ======================================== event methods ======================================== #

    def insert_one_event(self, data):
        self.database["CAS_ASK_EVENT"].insert_one(data)

    def insert_many_event(self, data):
        self.database["CAS_ASK_EVENT"].insert_many(data)

    def find_one_event(self, query):
        return self.database["CAS_ASK_EVENT"].find_one(query)

    def find_many_event(self, query):
        return self.database["CAS_ASK_EVENT"].find(query)

    def update_one_event(self, query, update):
        self.database["CAS_ASK_EVENT"].update_one(query, update)

    def update_many_event(self, query, update):
        self.database["CAS_ASK_EVENT"].update_many(query, update)

    def delete_one_event(self, query):
        self.database["CAS_ASK_EVENT"].delete_one(query)

    def delete_many_event(self, query):
        self.database["CAS_ASK_EVENT"].delete_many(query)

    # ================================== precision_probleme_vehicule methods ================================== #

    def insert_one_precision_probleme_vehicule(self, data):
        self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].insert_one(data)

    def precision_probleme_vehicule(self, data):
        self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].insert_many(data)

    def find_one_precision_probleme_vehicule(self, query):
        return self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].find_one(query)

    def find_many_precision_probleme_vehicule(self, query):
        return self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].find(query)

    def update_one_precision_probleme_vehicule(self, query, update):
        self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].update_one(query, update)

    def update_many_precision_probleme_vehicule(self, query, update):
        self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].update_many(query, update)

    def delete_one_precision_probleme_vehicule(self, query):
        self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].delete_one(query)

    def delete_many_precision_probleme_vehicule(self, query):
        self.database["CAS_ASK_PRECISION_PROBLEME_VEHICULE"].delete_many(query)

    def delete_many_garage_destination(self, query):
        self.database["CAS_ASK_GARAGE_DESTINATION"].delete_many(query)
