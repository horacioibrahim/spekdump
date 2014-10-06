# -*- coding=UTF-8 -*-


#app
import config


class SpekDumpDAO(object):


    def __init__(self, *args, **kwargs):

        # Constructor...
        host = kwargs.get("host", None)
        database = kwargs.get("database", None)
        collection = kwargs.get("collection", None)
        self._db = None
        self.db = {'host': host, 'database': database, 'collection': collection}


    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, attrs=None):
        if attrs and not isinstance(attrs, dict):
            raise TypeError("Argument attrs must be a dict "
                            "{host: X, database: y, collection: Z}")

        host = attrs.get("host", None)
        database = attrs.get("database", None)
        collection = attrs.get("collection", None)

        if host or database or collection:
            self._db = config.get_database(host=host, database=database,
                                           collection=collection)
        else:
            if not self._db:
                self._db = config.get_database()


    @db.deleter
    def db(self):
        del self._db

    def get_all_documents(self):
        return self.db.find({})

    def _make_filter(self, filters=[]):
        """
        Creates a filter in MongoDB for fields and values.
        _make_filter([(key, value)]) ->
                    {$and: [ {key: value}, {key:{$exists: True}} ] }

        Args:
            filters -> list of tuples (key, value)
        """
        dict_filter = {}

        if isinstance(filters, list) and filters:
            for elem in filters:
                if not isinstance(elem, tuple):
                    # TODO: to create Exceptions
                    raise TypeError(u'All elements must be tuple')
        else:
            raise TypeError(u'Filters must be a list')


        dict_filter['$and'] = []
        for f, t in filters:
            dict_filter['$and'].append({f: t})
            dict_filter['$and'].append({f: {'$exists': True}})

        return dict_filter

    def _clean_filter(self, filters, cursor, mode=0):
        """
        DEPRECATED: Because _make_filter now is  using '$and'

        The MongoDB returns queries from fields non-existent with query
        db.find({'NON-existent-field': None}). It'll return the documents
        where the field 'NON-existent-field' is None (or null like MongoDB)
        or the field NOT IS IN document. Because is need a workaround
        (for warnings).

        Args:
            filter: a dict possibly returned by _make_filter
            cursor: a cursor of a query
            mode:
                0 (warn) -> only report with output messages with warnings
                1 (strict) -> purges documents without the field
                2 (warn and strict) -> report and purge
        """
        documents = []
        warning_message = "\nWarning: The field {field} is not exists in the " \
                    "doc:\n {document}"

        for doc in cursor:
            for f, t in filters.items():
                if t is None:
                    # checking if field is contained...
                    if f not in doc:
                        if mode == 0:
                            print warning_message.format(field=f, document=doc)
                        if mode == 1:
                            continue # skip|purge or not put in array
                        if mode == 2:
                            print warning_message.format(field=f, document=doc)
                            continue # skip|purge

                    documents.append(doc)

        return documents

    def filter(self, filters, mode=0):
        """
        Makes a filter with base a list with (field, value)

        Args:
            filters: a list of tuples with the pair (field, term). e.g:
                [('field1', 'termX'), ('field2', 'termY')]
            mode (DEPRECATED see _clean_filter):
                0 (warn) -> only report with output messages with warnings
                1 (strict) -> purges documents without the field
                2 (warn and strict) -> report and purge

        Returns:
            a list of MongoDB's documents
        """
        dict_filter = self._make_filter(filters)
        docs = self.db.find(dict_filter)

        return docs

    def count_by(self, filters):
        """
        Returns the quantity of documents by specified filters

        Args:
           filters: a list of tuples with the pair (field, term). e.g:
                [('field1', 'termX'), ('field2', 'termY')]
        """
        docs_list = self.filter(filters) # count only strict matched
        counted = docs_list.count()

        return counted


    def save(self, document, id_field="_id"):
        """
        Uses update if not exist insert rather update the object

        Args:
            document -> a dictionary with MongoDB's syntax to save it
            id_field -> name of field it'll indexed. Default is _id
        """
        # TODO: support multiple indexes (unique with fields)

        collection = self.db

        try:
            _id = document[id_field]
            new_doc = document.copy() # It's need if reuse document. See tests.
            del new_doc[id_field]
        except KeyError, e:
            raise TypeError("The method save() required an arg id_field or the "
                            "key _id in document") # TODO: create exceptions

        try:
            collection.update({'_id': _id}, {'$set': new_doc},
                              upsert=True)
            return 0
        except:
            raise
